import { Routes, Route } from 'react-router-dom'
import { MovieCatalog } from './pages/MovieCatalog'
import { MovieDetailPage } from './pages/MovieDetailPage'
import './App.css'

/**
 * App component - Root component with routing between catalog and detail views.
 * 
 * Routes:
 * - "/" - MovieCatalog page (browse all movies)
 * - "/movie/:id" - MovieDetailPage (view single movie details)
 * 
 * Validates: Requirements 2.1
 */
function App() {
  return (
    <Routes>
      <Route path="/" element={<MovieCatalog />} />
      <Route path="/movie/:id" element={<MovieDetailPage />} />
    </Routes>
  )
}

export default App
