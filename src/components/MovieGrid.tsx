import type { Movie, ProvidersLookup } from '../types/movie';
import { MovieCard } from './MovieCard';
import './MovieGrid.css';

interface MovieGridProps {
  /** Array of movies to display in the grid */
  movies: Movie[];
  /** Providers lookup table */
  providers?: ProvidersLookup;
  /** Selected streaming region */
  streamingRegion?: string;
}

/**
 * MovieGrid component displays a responsive grid of MovieCard components.
 * Uses CSS Grid for layout with multi-column on desktop and single column on mobile.
 * 
 * @param movies - Array of movies to render in the grid
 */
export function MovieGrid({ movies, providers = {}, streamingRegion = 'US' }: MovieGridProps) {
  if (movies.length === 0) {
    return (
      <div className="movie-grid__empty">
        <p>No movies found.</p>
      </div>
    );
  }

  return (
    <div className="movie-grid">
      {movies.map((movie) => (
        <MovieCard 
          key={movie.id} 
          movie={movie} 
          providers={providers}
          streamingRegion={streamingRegion}
        />
      ))}
    </div>
  );
}

export default MovieGrid;
