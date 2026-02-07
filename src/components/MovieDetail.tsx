import { useState } from 'react';
import { Link } from 'react-router-dom';
import type { Movie, StreamingProvider, ProvidersLookup } from '../types/movie';
import './MovieDetail.css';

interface MovieDetailProps {
  /** The movie data to display */
  movie: Movie;
  /** Providers lookup table */
  providers: ProvidersLookup;
  /** All movies for finding similar ones */
  allMovies?: Movie[];
}

/** Data URL for a simple gray placeholder - no external request needed */
const PLACEHOLDER_POSTER = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="600" viewBox="0 0 400 600"%3E%3Crect fill="%232a2a2a" width="400" height="600"/%3E%3Ctext fill="%23666" font-family="sans-serif" font-size="20" x="50%25" y="50%25" text-anchor="middle"%3ENo Poster%3C/text%3E%3C/svg%3E';

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
 * Generate a search URL for a streaming service
 */
function getProviderSearchUrl(providerName: string, movieTitle: string): string | null {
  const query = encodeURIComponent(movieTitle);
  const providerLower = providerName.toLowerCase();
  
  // Map provider names to their search URLs
  if (providerLower.includes('netflix')) {
    return `https://www.netflix.com/search?q=${query}`;
  }
  if (providerLower.includes('amazon') || providerLower.includes('prime')) {
    return `https://www.amazon.com/s?k=${query}&i=instant-video`;
  }
  if (providerLower.includes('disney')) {
    return `https://www.disneyplus.com/search?q=${query}`;
  }
  if (providerLower.includes('hulu')) {
    return `https://www.hulu.com/search?q=${query}`;
  }
  if (providerLower.includes('max') || providerLower === 'hbo max') {
    return `https://www.max.com/search?q=${query}`;
  }
  if (providerLower.includes('apple')) {
    return `https://tv.apple.com/search?term=${query}`;
  }
  if (providerLower.includes('paramount')) {
    return `https://www.paramountplus.com/search/?q=${query}`;
  }
  if (providerLower.includes('peacock')) {
    return `https://www.peacocktv.com/search?q=${query}`;
  }
  if (providerLower.includes('mubi')) {
    return `https://mubi.com/search?query=${query}`;
  }
  if (providerLower.includes('criterion')) {
    return `https://www.criterionchannel.com/search?q=${query}`;
  }
  if (providerLower.includes('youtube')) {
    return `https://www.youtube.com/results?search_query=${query}+full+movie`;
  }
  if (providerLower.includes('vudu') || providerLower.includes('fandango')) {
    return `https://www.vudu.com/content/movies/search?searchString=${query}`;
  }
  if (providerLower.includes('google play')) {
    return `https://play.google.com/store/search?q=${query}&c=movies`;
  }
  
  // Fallback: Google search for the service + movie
  return `https://www.google.com/search?q=${query}+${encodeURIComponent(providerName)}`;
}

/**
 * MovieDetail component displays comprehensive information about a single movie.
 * Shows all available movie metadata including recognitions, genres, and tags.
 * Handles missing optional fields gracefully by omitting sections for missing data.
 * 
 * @param movie - The movie data to display
 */
export function MovieDetail({ movie, providers, allMovies = [] }: MovieDetailProps) {
  const [selectedRegion, setSelectedRegion] = useState(() => {
    return localStorage.getItem('streamingRegion') || 'GB';
  });
  
  // Persist region changes to localStorage
  const handleRegionChange = (region: string) => {
    setSelectedRegion(region);
    localStorage.setItem('streamingRegion', region);
  };
  
  const {
    id,
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

  // Find similar movies: same director first, then same cast
  const similarMovies = (() => {
    const byDirector = allMovies.filter(m => m.id !== id && m.director === director);
    const byCast = allMovies.filter(m => {
      if (m.id === id || m.director === director) return false;
      return cast?.some(actor => m.cast?.includes(actor));
    });
    return [...byDirector, ...byCast].slice(0, 6);
  })();

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
          <div className="movie-detail__title-row">
            <h1 className="movie-detail__title">{title}</h1>
            {rating && (
              <span className="movie-detail__title-rating">
                <span className="movie-detail__rating-star">★</span>
                {rating.toFixed(1)}
              </span>
            )}
          </div>
          <p className="movie-detail__director">
            Directed by{' '}
            <Link to={`/?q=${encodeURIComponent(director)}`} className="movie-detail__link">
              {director}
            </Link>
          </p>
          <p className="movie-detail__year">{year}</p>
          
          {(country || runtime) && (
            <div className="movie-detail__meta">
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
                <li key={index} className="movie-detail__cast-item">
                  <Link to={`/?q=${encodeURIComponent(actor)}`} className="movie-detail__link">
                    {actor}
                  </Link>
                </li>
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
                onChange={(e) => handleRegionChange(e.target.value)}
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
                      {subscriptionProviders.map((provider, index) => {
                        const searchUrl = getProviderSearchUrl(provider.name, title);
                        return (
                          <a
                            key={index}
                            href={searchUrl || '#'}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="movie-detail__provider movie-detail__provider--link"
                            title={`Search on ${provider.name}`}
                          >
                            <img
                              src={provider.logo}
                              alt={provider.name}
                              className="movie-detail__provider-logo"
                            />
                            <span className="movie-detail__provider-name">{provider.name}</span>
                          </a>
                        );
                      })}
                    </div>
                  </div>
                )}
                {rentProviders.length > 0 && (
                  <div className="movie-detail__streaming-group">
                    <h3 className="movie-detail__streaming-label">Rent</h3>
                    <div className="movie-detail__streaming-providers">
                      {rentProviders.map((provider, index) => {
                        const searchUrl = getProviderSearchUrl(provider.name, title);
                        return (
                          <a
                            key={index}
                            href={searchUrl || '#'}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="movie-detail__provider movie-detail__provider--link"
                            title={`Search on ${provider.name}`}
                          >
                            <img
                              src={provider.logo}
                              alt={provider.name}
                              className="movie-detail__provider-logo"
                            />
                            <span className="movie-detail__provider-name">{provider.name}</span>
                          </a>
                        );
                      })}
                    </div>
                  </div>
                )}
                {buyProviders.length > 0 && (
                  <div className="movie-detail__streaming-group">
                    <h3 className="movie-detail__streaming-label">Buy</h3>
                    <div className="movie-detail__streaming-providers">
                      {buyProviders.map((provider, index) => {
                        const searchUrl = getProviderSearchUrl(provider.name, title);
                        return (
                          <a
                            key={index}
                            href={searchUrl || '#'}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="movie-detail__provider movie-detail__provider--link"
                            title={`Search on ${provider.name}`}
                          >
                            <img
                              src={provider.logo}
                              alt={provider.name}
                              className="movie-detail__provider-logo"
                            />
                            <span className="movie-detail__provider-name">{provider.name}</span>
                          </a>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <p className="movie-detail__no-streaming">Not available in this region</p>
            )}
          </section>
        )}

        {similarMovies.length > 0 && (
          <section className="movie-detail__section">
            <h2 className="movie-detail__section-title">Similar Movies</h2>
            <div className="movie-detail__similar">
              {similarMovies.map(m => (
                <Link key={m.id} to={`/movie/${m.id}`} className="movie-detail__similar-card">
                  <img
                    src={m.posterUrl || PLACEHOLDER_POSTER}
                    alt={m.title}
                    className="movie-detail__similar-poster"
                    onError={(e) => { e.currentTarget.src = PLACEHOLDER_POSTER; }}
                  />
                  <div className="movie-detail__similar-info">
                    <div className="movie-detail__similar-title-row">
                      <span className="movie-detail__similar-title">{m.title}</span>
                      {m.rating && (
                        <span className="movie-detail__similar-rating">
                          <span className="movie-detail__similar-rating-star">★</span>
                          {m.rating.toFixed(1)}
                        </span>
                      )}
                    </div>
                    <span className="movie-detail__similar-meta">{m.director} • {m.year}</span>
                  </div>
                </Link>
              ))}
            </div>
          </section>
        )}
      </div>
    </article>
  );
}

export default MovieDetail;
