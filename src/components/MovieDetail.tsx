import { useState } from 'react';
import type { Movie, StreamingProvider, ProvidersLookup } from '../types/movie';
import './MovieDetail.css';

interface MovieDetailProps {
  /** The movie data to display */
  movie: Movie;
  /** Providers lookup table */
  providers: ProvidersLookup;
}

/** Placeholder image for movies without a poster */
const PLACEHOLDER_POSTER = 'https://via.placeholder.com/400x600?text=No+Poster';

/** Available streaming regions */
const STREAMING_REGIONS = [
  { code: 'US', name: 'United States' },
  { code: 'GB', name: 'United Kingdom' },
  { code: 'CA', name: 'Canada' },
  { code: 'AU', name: 'Australia' },
  { code: 'DE', name: 'Germany' },
  { code: 'FR', name: 'France' },
  { code: 'IT', name: 'Italy' },
  { code: 'ES', name: 'Spain' },
  { code: 'JP', name: 'Japan' },
  { code: 'KR', name: 'South Korea' },
];

/**
 * MovieDetail component displays comprehensive information about a single movie.
 * Shows all available movie metadata including recognitions, genres, and tags.
 * Handles missing optional fields gracefully by omitting sections for missing data.
 * 
 * @param movie - The movie data to display
 */
export function MovieDetail({ movie, providers }: MovieDetailProps) {
  const [selectedRegion, setSelectedRegion] = useState('US');
  
  const {
    title,
    director,
    year,
    synopsis,
    posterUrl,
    country,
    runtime,
    cast,
    genres,
    recognitions,
    tags,
    streaming,
    rating,
  } = movie;

  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    e.currentTarget.src = PLACEHOLDER_POSTER;
  };

  /**
   * Formats runtime in minutes to a human-readable string
   */
  const formatRuntime = (minutes: number): string => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours === 0) {
      return `${mins}min`;
    }
    if (mins === 0) {
      return `${hours}h`;
    }
    return `${hours}h ${mins}min`;
  };

  // Get streaming providers for selected region (resolve from lookup)
  const regionRefs = streaming?.[selectedRegion] || [];
  const regionProviders: (StreamingProvider & { type: 'subscription' | 'rent' | 'buy' })[] = regionRefs
    .map(ref => {
      const provider = providers[ref.id];
      return provider ? { ...provider, type: ref.type } : null;
    })
    .filter((p): p is (StreamingProvider & { type: 'subscription' | 'rent' | 'buy' }) => p !== null);
  
  const subscriptionProviders = regionProviders.filter(p => p.type === 'subscription');
  const rentProviders = regionProviders.filter(p => p.type === 'rent');
  const buyProviders = regionProviders.filter(p => p.type === 'buy');
  
  // Check which regions have streaming available
  const availableRegions = streaming ? Object.keys(streaming) : [];
  const hasAnyStreaming = availableRegions.length > 0;

  return (
    <article className="movie-detail">
      <div className="movie-detail__header">
        <div className="movie-detail__poster-container">
          <img
            src={posterUrl || PLACEHOLDER_POSTER}
            alt={`${title} poster`}
            className="movie-detail__poster"
            onError={handleImageError}
          />
        </div>
        
        <div className="movie-detail__main-info">
          <h1 className="movie-detail__title">{title}</h1>
          <p className="movie-detail__director">Directed by {director}</p>
          <p className="movie-detail__year">{year}</p>
          
          {(country || runtime || rating) && (
            <div className="movie-detail__meta">
              {rating && (
                <span className="movie-detail__rating">
                  <span className="movie-detail__rating-star">★</span>
                  {rating.toFixed(1)}
                </span>
              )}
              {rating && (country || runtime) && <span className="movie-detail__separator">•</span>}
              {country && <span className="movie-detail__country">{country}</span>}
              {country && runtime && <span className="movie-detail__separator">•</span>}
              {runtime && <span className="movie-detail__runtime">{formatRuntime(runtime)}</span>}
            </div>
          )}
          
          {synopsis && (
            <div className="movie-detail__synopsis">
              <h2 className="movie-detail__section-title">Synopsis</h2>
              <p className="movie-detail__synopsis-text">{synopsis}</p>
            </div>
          )}
        </div>
      </div>
      
      <div className="movie-detail__body">
        {cast && cast.length > 0 && (
          <section className="movie-detail__section">
            <h2 className="movie-detail__section-title">Cast</h2>
            <ul className="movie-detail__cast-list">
              {cast.map((actor, index) => (
                <li key={index} className="movie-detail__cast-item">{actor}</li>
              ))}
            </ul>
          </section>
        )}
        
        {genres && genres.length > 0 && (
          <section className="movie-detail__section">
            <h2 className="movie-detail__section-title">Genres</h2>
            <div className="movie-detail__genres">
              {genres.map((genre, index) => (
                <span key={index} className="movie-detail__genre-tag">{genre}</span>
              ))}
            </div>
          </section>
        )}
        
        {recognitions && recognitions.length > 0 && (
          <section className="movie-detail__section">
            <h2 className="movie-detail__section-title">Recognitions</h2>
            <ul className="movie-detail__recognitions-list">
              {recognitions.map((recognition, index) => (
                <li key={index} className="movie-detail__recognition-item">
                  <span className="movie-detail__recognition-type">{recognition.type}</span>
                  <span className="movie-detail__recognition-year">({recognition.year})</span>
                  {recognition.details && (
                    <span className="movie-detail__recognition-details"> — {recognition.details}</span>
                  )}
                </li>
              ))}
            </ul>
          </section>
        )}
        
        {tags && tags.length > 0 && (
          <section className="movie-detail__section">
            <h2 className="movie-detail__section-title">Tags</h2>
            <div className="movie-detail__tags">
              {tags.map((tag, index) => (
                <span key={index} className="movie-detail__tag">{tag}</span>
              ))}
            </div>
          </section>
        )}

        {hasAnyStreaming && (
          <section className="movie-detail__section">
            <div className="movie-detail__streaming-header">
              <h2 className="movie-detail__section-title">Where to Watch</h2>
              <select
                className="movie-detail__region-select"
                value={selectedRegion}
                onChange={(e) => setSelectedRegion(e.target.value)}
              >
                {STREAMING_REGIONS.map(r => (
                  <option key={r.code} value={r.code}>
                    {r.name} {availableRegions.includes(r.code) ? '' : '(unavailable)'}
                  </option>
                ))}
              </select>
            </div>
            {regionProviders.length > 0 ? (
              <div className="movie-detail__streaming">
                {subscriptionProviders.length > 0 && (
                  <div className="movie-detail__streaming-group">
                    <h3 className="movie-detail__streaming-label">Stream</h3>
                    <div className="movie-detail__streaming-providers">
                      {subscriptionProviders.map((provider, index) => (
                        <div key={index} className="movie-detail__provider">
                          <img
                            src={provider.logo}
                            alt={provider.name}
                            className="movie-detail__provider-logo"
                          />
                          <span className="movie-detail__provider-name">{provider.name}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {rentProviders.length > 0 && (
                  <div className="movie-detail__streaming-group">
                    <h3 className="movie-detail__streaming-label">Rent</h3>
                    <div className="movie-detail__streaming-providers">
                      {rentProviders.map((provider, index) => (
                        <div key={index} className="movie-detail__provider">
                          <img
                            src={provider.logo}
                            alt={provider.name}
                            className="movie-detail__provider-logo"
                          />
                          <span className="movie-detail__provider-name">{provider.name}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {buyProviders.length > 0 && (
                  <div className="movie-detail__streaming-group">
                    <h3 className="movie-detail__streaming-label">Buy</h3>
                    <div className="movie-detail__streaming-providers">
                      {buyProviders.map((provider, index) => (
                        <div key={index} className="movie-detail__provider">
                          <img
                            src={provider.logo}
                            alt={provider.name}
                            className="movie-detail__provider-logo"
                          />
                          <span className="movie-detail__provider-name">{provider.name}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <p className="movie-detail__no-streaming">Not available in this region</p>
            )}
          </section>
        )}
      </div>
    </article>
  );
}

export default MovieDetail;
