import React, { useState } from 'react';
import type { CreateGameRequest, Difficulty, Player } from '../api/types';

export interface GameOptionsProps {
  onStart: (payload: CreateGameRequest) => void;
  creating?: boolean;
}

export const GameOptions: React.FC<GameOptionsProps> = ({ onStart, creating = false }) => {
  const [difficulty, setDifficulty] = useState<Difficulty>('easy');
  const [firstPlayer, setFirstPlayer] = useState<'human' | 'computer'>('human');
  const [humanSymbol, setHumanSymbol] = useState<Player>('x');

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onStart({ difficulty, first_player: firstPlayer, human_symbol: humanSymbol });
  }

  return (
    <form className="options" onSubmit={handleSubmit}>
      <div className="row">
        <label>
          Difficulty
          <select value={difficulty} onChange={(e) => setDifficulty(e.target.value as Difficulty)}>
            <option value="easy">Easy (Aleatory)</option>
            <option value="medium">Medium (Heuristic)</option>
            <option value="hard">Hard (Gemini)</option>
          </select>
        </label>
        <label>
          First Player
          <select value={firstPlayer} onChange={(e) => setFirstPlayer(e.target.value as 'human' | 'computer')}>
            <option value="human">Human</option>
            <option value="computer">Computer</option>
          </select>
        </label>
        <label>
          Your Symbol
          <select value={humanSymbol} onChange={(e) => setHumanSymbol(e.target.value as Player)}>
            <option value="x">X</option>
            <option value="o">O</option>
          </select>
        </label>
      </div>
      <button className="start-game__button" type="submit" disabled={creating}>
        {creating ? 'Starting…' : 'Start Game'}
      </button>
    </form>
  );
};

export default GameOptions;
