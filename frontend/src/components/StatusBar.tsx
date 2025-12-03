import React from 'react';
import type { GameRead } from '../api/types';

export interface StatusBarProps {
  game: GameRead | null;
  loading: Boolean | null;
  error?: string | null;
}

export const StatusBar: React.FC<StatusBarProps> = ({ game, error, loading}) => {
  if (error) return <div className="status error">{error}</div>;
  if (!game) return <div className="status">Create a game to start playing.</div>;

  if (game.status === 'x_won' || game.status === 'o_won') {
    const winner = game.status === 'x_won' ? 'x' : 'o';
    return <div className="status win">Winner: {winner}</div>;
  }
  if (game.status === 'draw') {
    return <div className="status draw">Draw!</div>;
  }

  return (
    <div className="status in-progress">
      {loading ? <div className="hint">Waiting for move…</div> : <div> Next player: <strong>{game.next_player}</strong></div>}
    </div>
  );
};

export default StatusBar;
