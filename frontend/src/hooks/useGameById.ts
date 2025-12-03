import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import type { GameRead, MoveResponse, Player } from '@/api/types';
import { getGame, postMove } from '@/api/client';
import { POSITION_TO_INDEX } from '@/api/types';

function applyMoveToBoard(board: string, position: number, symbol: Player): string {
  const idx = POSITION_TO_INDEX[position];
  if (idx === undefined) return board;
  const cells = board.split('');
  if (cells[idx] !== ' ') return board;
  cells[idx] = symbol;
  return cells.join('');
}

type Options = { initialGame?: GameRead | null };

export function useGameById(gameId: string, opts: Options = {}) {
  const [game, setGame] = useState<GameRead | null>(opts.initialGame ?? null);
  const [loading, setLoading] = useState(false); // for play action
  const [initialLoading, setInitialLoading] = useState(!opts.initialGame);
  const [error, setError] = useState<string | null>(null);

  // keep a ref to revert state on optimistic errors
  const lastStable = useRef<GameRead | null>(opts.initialGame ?? null);

  const load = useCallback(async () => {
    setInitialLoading(true);
    setError(null);
    try {
      const res = await getGame(gameId);
      setGame((current) => {
        if (!current) {
          lastStable.current = res;
          return res;
        }
        const curMoves = current.moves?.length ?? 0;
        const resMoves = res.moves?.length ?? 0;
        const curUpdated = Date.parse(current.updated_at);
        const resUpdated = Date.parse(res.updated_at);

        // If server response appears older than current local state, ignore it
        const isResOlderByTime = !Number.isNaN(curUpdated) && !Number.isNaN(resUpdated) && resUpdated < curUpdated;
        const isResOlderByMoves = resMoves < curMoves;
        if (isResOlderByTime || isResOlderByMoves) {
          return current;
        }
        lastStable.current = res;
        return res;
      });
    } catch (e: any) {
      setError(e?.message ?? 'Failed to load game');
    } finally {
      setInitialLoading(false);
    }
  }, [gameId]);

  useEffect(() => {
    load();
  }, [load]);

  const canPlay = useMemo(() => {
    if (!game) return false;
    if (game.status !== 'in_progress') return false;
    return game.next_player === game.human_symbol;
  }, [game]);

  const play = useCallback(
    async (position: number) => {
      if (!game || !canPlay || loading) return;
      setLoading(true);
      setError(null);

      // optimistic update
      const prev = game;
      const optimistic: GameRead = {
        ...game,
        board: applyMoveToBoard(game.board, position, game.human_symbol),
        moves: [...game.moves, position],
        next_player: game.computer_symbol,
      };
      setGame(optimistic);

      try {
        const res: MoveResponse = await postMove(game.id, { position });
        setGame((current) => {
          // If for any reason the response is older (fewer moves or older updated_at), keep current
          if (!current) {
            lastStable.current = res;
            return res;
          }
          const curMoves = current.moves?.length ?? 0;
          const resMoves = res.moves?.length ?? 0;
          const curUpdated = Date.parse(current.updated_at);
          const resUpdated = Date.parse(res.updated_at);
          const resIsOlderByMoves = resMoves < curMoves;
          const resIsOlderByTime = !Number.isNaN(curUpdated) && !Number.isNaN(resUpdated) && resUpdated < curUpdated;
          if (resIsOlderByMoves || resIsOlderByTime) {
            return current;
          }
          lastStable.current = res;
          return res;
        });
      } catch (e: any) {
        // revert on error
        setGame(prev);
        setError(e?.message ?? 'Failed to play');
      } finally {
        setLoading(false);
      }
    },
    [game, canPlay, loading]
  );

  return { game, loading: loading || initialLoading, error, canPlay, play, reload: load };
}
