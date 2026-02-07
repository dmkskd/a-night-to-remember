import { Link, useParams } from 'react-router-dom';
import { useMovie } from '../hooks/useMovie';
import { useMovies } from '../hooks/useMovies';
import { MovieDetail } from '../components/MovieDetail';
import './MovieDetailPage.css';

/**
 * MovieDetailPage component.
 * Page component that displays detailed information about a single movie.
 * Gets the movie ID from route params and uses the useMovie hook to load data.
 * Handles loading, not found, and error states.
 * 
 * Validates: Requirements 2.1
 */
export function MovieDetailPage() {
  // Get movie ID from route params
  const { id } = useParams<{ id: string }>();

  // Load movie data using the hook
  const { movie, isLoading, error } = useMovie(id || '');
  const { movies, providers } = useMovies();

  // Handle loading state
  if (isLoading) {
    return (
      <div className="movie-detail-page">
        <div className="movie-detail-page__loading">
          <p>Loading movie details...</p>
        </div>
      </div>
    );
  }

  // Handle error state
  if (error) {
    return (
      <div className="movie-detail-page">
        <div className="movie-detail-page__error">
          <p>Error loading movie: {error.message}</p>
          <Link to="/" className="movie-detail-page__back-link">
            ← Back to catalog
          </Link>
        </div>
      </div>
    );
  }

  // Handle not found state (movie is null after loading)
  if (!movie) {
    return (
      <div className="movie-detail-page">
        <div className="movie-detail-page__not-found">
          <h2>Movie Not Found</h2>
          <p>The movie you're looking for doesn't exist or has been removed.</p>
          <Link to="/" className="movie-detail-page__back-link">
            ← Back to catalog
          </Link>
        </div>
      </div>
    );
  }

  // Display movie details
  return (
    <div className="movie-detail-page">
      <nav className="movie-detail-page__nav">
        <Link to="/" className="movie-detail-page__back-link">
          ← Back to catalog
        </Link>
      </nav>
      <main className="movie-detail-page__content">
        <MovieDetail movie={movie} providers={providers} allMovies={movies} />
      </main>
    </div>
  );
}

export default MovieDetailPage;
