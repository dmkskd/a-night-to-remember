import { Routes, Route, NavLink, Navigate } from 'react-router-dom'
import { MovieCatalog } from './pages/MovieCatalog'
import { MovieDetailPage } from './pages/MovieDetailPage'
import { MusicCatalog } from './pages/MusicCatalog'
import { AlbumDetailPage } from './pages/AlbumDetailPage'
import { StoriesCatalog } from './pages/StoriesCatalog'
import { StoryDetailPage } from './pages/StoryDetailPage'
import { FEATURES } from './config'
import './App.css'

/**
 * App component - Root component with navigation and routing.
 * 
 * Routes:
 * - "/" - MovieCatalog page (browse all movies)
 * - "/movie/:id" - MovieDetailPage (view single movie details)
 * - "/music" - MusicCatalog page (browse all albums)
 * - "/music/:id" - AlbumDetailPage (view single album details)
 * - "/stories" - StoriesCatalog page (browse all short stories)
 * - "/stories/:id" - StoryDetailPage (view single story details)
 */
function App() {
  const enabledFeatures = [FEATURES.movies, FEATURES.music, FEATURES.stories].filter(Boolean).length
  const showNav = enabledFeatures > 1

  return (
    <div className="app">
      {showNav && (
        <header className="app__header">
          <h1 className="app__title">A Night To Remember</h1>
          <nav className="app__nav">
            {FEATURES.movies && (
              <NavLink to="/" className={({ isActive }) => `app__nav-link ${isActive ? 'app__nav-link--active' : ''}`} end>
                Movies
              </NavLink>
            )}
            {FEATURES.music && (
              <NavLink to="/music" className={({ isActive }) => `app__nav-link ${isActive ? 'app__nav-link--active' : ''}`}>
                Music
              </NavLink>
            )}
            {FEATURES.stories && (
              <NavLink to="/stories" className={({ isActive }) => `app__nav-link ${isActive ? 'app__nav-link--active' : ''}`}>
                Stories
              </NavLink>
            )}
          </nav>
        </header>
      )}
      <Routes>
        {FEATURES.movies && (
          <>
            <Route path="/" element={<MovieCatalog showTitle={!showNav} />} />
            <Route path="/movie/:id" element={<MovieDetailPage />} />
          </>
        )}
        {FEATURES.music && (
          <>
            <Route path="/music" element={<MusicCatalog showTitle={!showNav} />} />
            <Route path="/music/:id" element={<AlbumDetailPage />} />
          </>
        )}
        {FEATURES.stories && (
          <>
            <Route path="/stories" element={<StoriesCatalog showTitle={!showNav} />} />
            <Route path="/stories/:id" element={<StoryDetailPage />} />
          </>
        )}
        {/* Redirect to first available feature if accessing disabled route */}
        <Route path="*" element={<Navigate to={FEATURES.movies ? "/" : FEATURES.music ? "/music" : "/stories"} replace />} />
      </Routes>
    </div>
  )
}

export default App
