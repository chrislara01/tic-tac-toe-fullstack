import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GameOptions } from '../components/GameOptions';
import type { CreateGameRequest } from '../api/types';
import { createGame } from '../api/client';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onStart = async (payload: CreateGameRequest) => {
    setCreating(true);
    setError(null);
    try {
      const game = await createGame(payload);
      navigate(`/game/${game.id}`, { state: { game } });
    } catch (e: any) {
      setError(e?.message ?? 'Failed to create game');
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Tic-Tac-Toe</h1>
        <p className="subtitle">Single player tic tac toe game</p>
      </header>
      {error && <div className="status error">{error}</div>}
      <GameOptions onStart={onStart} creating={creating} />
    </div>
  );
};

export default HomePage;
