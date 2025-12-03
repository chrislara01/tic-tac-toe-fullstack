import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { Board } from '../components/Board';
import { StatusBar } from '../components/StatusBar';
import { useGameById } from '../hooks/useGameById';

const GamePage: React.FC = () => {
  const params = useParams();
  const gameId = params.id as string | undefined;

  if (!gameId) {
    return (
      <div className="container">
        <div className="status error">Invalid game id</div>
        <Link className="secondary" to="/">Go Home</Link>
      </div>
    );
  }

  const { game, loading, error, canPlay, play } = useGameById(gameId);

  return (
    <div className="container">
      <header>
        <h1>Tic-Tac-Toe</h1>
        <p className="subtitle">Single player vs AI</p>
      </header>

      {game && <StatusBar game={game} error={error ?? undefined} loading={loading} />}
      {!game && error && <div className="status error">{error}</div>}

      {game && (
        <div className="game">
          <Board board={game.board} disabled={!canPlay || loading} onPlay={play} />
          <div className="panel">
            <div className="info">
              <div>
                <strong>You:</strong> {game.human_symbol} &nbsp; <strong>AI:</strong> {game.computer_symbol}
              </div>
              <div>
                <strong>Difficulty:</strong> {game.difficulty}
              </div>
            </div>
            <div className="actions">
              <Link className="secondary" to="/">New Game</Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GamePage;
