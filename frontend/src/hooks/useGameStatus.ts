import { useMemo } from 'react';
import type { GameRead } from '../api/types';

type Options = {
  loading?: boolean;
  error?: string;
};

export function useGameStatus(game: GameRead, opts: Options = {}) {
  const { loading = false, error } = opts;

  const result = useMemo(() => {
    // Base class
    let cls = 'status';
    let variant: 'error' | 'win' | 'draw' | 'in_progress' = 'in_progress';
    let message = '';
    let winner: 'x' | 'o' | undefined;
    let nextPlayer: 'x' | 'o' | undefined;

    if (error) {
      variant = 'error';
      cls += ' error';
      message = error;
      return { className: cls, variant, message, winner, nextPlayer, loading } as const;
    }

    if (game.status === 'x_won' || game.status === 'o_won') {
      variant = 'win';
      cls += ' win';
      winner = game.status === 'x_won' ? 'x' : 'o';
      message = `Winner: ${winner.toUpperCase()}`;
      return { className: cls, variant, message, winner, nextPlayer, loading } as const;
    }

    if (game.status === 'draw') {
      variant = 'draw';
      cls += ' draw';
      message = 'Draw!';
      return { className: cls, variant, message, winner, nextPlayer, loading } as const;
    }

    // In progress
    variant = 'in_progress';
    cls += ' in-progress';
    nextPlayer = game.next_player;
    message = loading ? `Waiting for ${nextPlayer.toUpperCase()} to play…` : `Next player: ${nextPlayer.toUpperCase()}`;
    return { className: cls, variant, message, winner, nextPlayer, loading } as const;
  }, [error, game.status, game.next_player, loading]);

  return result;
}
