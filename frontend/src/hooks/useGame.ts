import { useCallback, useMemo, useState } from 'react';
import type { CreateGameRequest, GameRead, MoveResponse } from '../api/types';
import { createGame as apiCreateGame, postMove } from '../api/client';

export function useGame() {
  const [game, setGame] = useState<GameRead | null>(null);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startGame = useCallback(async (payload: CreateGameRequest) => {
    setCreating(true);
    setError(null);
    try {
      const res = await apiCreateGame(payload);
      setGame(res);
    } catch (e: any) {
      setError(e?.message ?? 'Failed to create game');
    } finally {
      setCreating(false);
    }
  }, []);

  const canPlay = useMemo(() => {
    if (!game) return false;
    if (game.status !== 'in_progress') return false;
    // Human can play when next_player is the human symbol
    return game.next_player === game.human_symbol;
  }, [game]);

  const play = useCallback(
    async (position: number) => {
      if (!game) return;
      if (!canPlay) return;
      setLoading(true);
      setError(null);
      try {
        const res: MoveResponse = await postMove(game.id, { position });
        setGame(res);
      } catch (e: any) {
        setError(e?.message ?? 'Failed to play');
      } finally {
        setLoading(false);
      }
    },
    [game, canPlay]
  );

  const reset = useCallback(() => {
    setGame(null);
    setError(null);
    setLoading(false);
    setCreating(false);
  }, []);

  return { game, startGame, play, canPlay, loading, creating, error, reset };
}
