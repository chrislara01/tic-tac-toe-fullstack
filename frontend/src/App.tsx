import './App.css'
import { GameOptions } from './components/GameOptions'
import { Board } from './components/Board'
import { StatusBar } from './components/StatusBar'
import { useGame } from './hooks/useGame'

function App() {
  const { game, startGame, play, canPlay, loading, creating, error, reset } = useGame()

  return (
    <>
      <div className="container">
        <header>
          <h1>Tic-Tac-Toe</h1>
          <p className="subtitle">Single player vs AI</p>
        </header>

        <StatusBar game={game} error={error} loading={loading}/>

        {!game && (
          <GameOptions onStart={startGame} creating={creating} />
        )}

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
                <button className="secondary" onClick={reset} disabled={creating || loading}>New Game</button>
              </div>
            </div>
          </div>
        )}
      </div>

      <footer>
        <small>Desarrollado por Christian Lara 👨🏻‍💻</small>
      </footer>
    </>
  )
}

export default App
