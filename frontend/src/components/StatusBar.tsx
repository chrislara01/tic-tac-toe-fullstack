import React, { memo } from 'react';
import type { GameRead } from '../api/types';
import { useGameStatus } from '../hooks/useGameStatus';

export interface StatusBarProps {
  game: GameRead;
  loading?: boolean | null;
  error?: string | null;
}

export const StatusBar: React.FC<StatusBarProps> = ({ game, error, loading }) => {
  const { className, variant, message, winner, nextPlayer } = useGameStatus(game, {
    loading: !!loading,
    error: error ?? undefined,
  });

  let content: React.ReactNode = message;
  if (variant === 'win' && winner) {
    content = (
      <>
        Winner: <strong>{winner}</strong>
      </>
    );
  } else if (variant === 'in_progress' && nextPlayer && !loading) {
    content = (
      <>
        Next player: <strong>{nextPlayer}</strong>
      </>
    );
  }

  return (
    <div className={className} aria-live="polite">
      {content}
    </div>
  );
};

export default memo(StatusBar);
