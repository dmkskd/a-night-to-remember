import { Link } from 'react-router-dom';
import type { Movie, ProvidersLookup } from '../types/movie';
import './MovieCard.css';

interface MovieCardProps {
  movie: Movie;
  providers?: ProvidersLookup;
  streamingRegion?: string;
}

/**
 * MovieCard component displays a single movie in the catalog grid.
 * Shows poster, title, director, and year.
 * The entire card is clickable and navigates to the movie detail page.
 * 
 * @param movie - The movie data to display
 */
export function MovieCard({ movie, providers = {}, streamingRegion = 'US' }: MovieCardProps) {
  const { id, title, director, year, posterUrl, streaming, country, rating } = movie;

  // Get first 3 subscription streaming providers for the card
  const regionRefs = streaming?.[streamingRegion] || [];
  const subscriptionProviders = regionRefs
    .filter(ref => ref.type === 'subscription')
    .slice(0, 3)
    .map(ref => providers[ref.id])
    .filter(Boolean);

  return (
    <Link to={`/movie/${id}`} className="movie-card">
      <div className="movie-card__poster-container">
        {posterUrl ? (
          <img
            src={posterUrl}
            alt={`${title} poster`}
            className="movie-card__poster"
          />
        ) : (
          <div className="movie-card__placeholder">
            <span className="movie-card__placeholder-text">No Poster</span>
          </div>
        )}
        {rating && (
          <div className="movie-card__rating">
            <span className="movie-card__rating-star">★</span>
            <span className="movie-card__rating-value">{rating.toFixed(1)}</span>
          </div>
        )}
      </div>
      <div className="movie-card__info">
        <h3 className="movie-card__title">{title}</h3>
        <p className="movie-card__director">{director}</p>
        <div className="movie-card__meta-row">
          <span className="movie-card__meta">
            {year}{country && ` · ${country}`}
          </span>
          {subscriptionProviders.length > 0 && (
            <div className="movie-card__streaming">
              {subscriptionProviders.map((provider, index) => (
                <img
                  key={index}
                  src={provider.logo}
                  alt={provider.name}
                  title={provider.name}
                  className="movie-card__streaming-logo"
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </Link>
  );
}

export default MovieCard;
