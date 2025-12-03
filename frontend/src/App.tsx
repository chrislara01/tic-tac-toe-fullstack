import '@/App.css'
import { Routes, Route } from 'react-router-dom'
import HomePage from '@/pages/HomePage'
import GamePage from '@/pages/GamePage'

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/game/:id" element={<GamePage />} />
      </Routes>
      <footer>
        <small>Desarrollado por Christian Lara 👨🏻‍💻</small>
      </footer>
    </>
  )
}

export default App
