import React from 'react';
import { INDEX_TO_POSITION } from '../api/types';

export interface BoardProps {
  board: string; // 9-char string in numpad order "789456123"
  disabled?: boolean;
  onPlay?: (position: number) => void; // numpad position 1..9
}

export const Board: React.FC<BoardProps> = ({ board, disabled = false, onPlay }) => {
  const cells = board.split('');

  function handleClick(index: number) {
    if (disabled) return;
    const symbol = cells[index];
    if (symbol !== ' ') return; // cannot play on occupied cell
    const position = INDEX_TO_POSITION[index];
    onPlay?.(position);
  }

  return (
    <div className="board">
      {cells.map((symbol, idx) => (
        <button
          key={idx}
          className={`cell ${symbol === ' ' ? 'empty' : symbol}`}
          onClick={() => handleClick(idx)}
          disabled={disabled || symbol !== ' '}
          aria-label={`cell ${idx}`}
        >
          {symbol === ' ' ? '' : symbol}
        </button>
      ))}
    </div>
  );
};

export default Board;
