import { useState, useMemo, useEffect } from 'react';
import { useMovies } from '../hooks/useMovies';
import { useFilteredMovies } from '../hooks/useFilteredMovies';
import { FilterDropdown } from '../components/FilterDropdown';
import { GroupedFilterDropdown } from '../components/GroupedFilterDropdown';
import { RatingSlider } from '../components/RatingSlider';
import { SearchInput } from '../components/SearchInput';
import { MovieGrid } from '../components/MovieGrid';
import moviesData from '../data/movies.json';
import './MovieCatalog.css';

// Define which recognition types are festivals vs critics' picks
const FESTIVAL_AWARDS = [
  "Cannes Palme d'Or",
  "Cannes Grand Prix",
  "Cannes Best Director",
  "Cannes Jury Prize",
  "Berlin Golden Bear",
  "Venice Golden Lion",
  "TIFF People's Choice",
  "Sundance Grand Jury Prize",
  "Sundance World Cinema Prize",
  "Tokyo Grand Prix",
  "Busan New Currents",
  "Hong Kong Best Film",
  "Annecy Cristal d'Or",
];

const CRITICS_PICKS = [
  "Sight & Sound Top 10",
  "Film Comment Top 10",
  "Kinema Junpo Best Foreign Film",
  "Indiewire Critics Poll",
  "Cinema Scope Top 10",
  "Cahiers du Cinéma Top 10",
  "German Film Critics",
  "Fotogramas (Spain)",
  "Korean Film Critics (KAFCA)",
];

// Available streaming regions
const STREAMING_REGIONS = [
  { code: 'US', name: 'US' },
  { code: 'GB', name: 'UK' },
  { code: 'CA', name: 'CA' },
  { code: 'AU', name: 'AU' },
  { code: 'DE', name: 'DE' },
  { code: 'FR', name: 'FR' },
  { code: 'IT', name: 'IT' },
  { code: 'ES', name: 'ES' },
  { code: 'JP', name: 'JP' },
  { code: 'KR', name: 'KR' },
];

/**
 * MovieCatalog page component.
 * Main page displaying the movie grid with filter and search controls.
 * Composes FilterBar, SearchInput, and MovieGrid components.
 * 
 * Validates: Requirements 1.1, 1.3, 3.3, 4.3
 */
export function MovieCatalog() {
  // State for active filters and search query
  const [awardsFilters, setAwardsFilters] = useState<string[]>([]);
  const [streamingFilters, setStreamingFilters] = useState<string[]>([]);
  const [streamingRegion, setStreamingRegion] = useState<string>('GB');
  const [countryFilters, setCountryFilters] = useState<string[]>([]);

  // Auto-detect user's country on mount
  useEffect(() => {
    const detectCountry = async () => {
      try {
        const response = await fetch('https://ipapi.co/country_code/');
        if (response.ok) {
          const countryCode = await response.text();
          // Map common codes and check if we support this region
          const supported = STREAMING_REGIONS.find(r => r.code === countryCode);
          if (supported) {
            setStreamingRegion(countryCode);
          }
        }
      } catch {
        // Silently fail, keep default GB
      }
    };
    detectCountry();
  }, []);
  const [decadeFilters, setDecadeFilters] = useState<string[]>([]);
  const [genreFilters, setGenreFilters] = useState<string[]>([]);
  const [minRating, setMinRating] = useState<number>(0);
  const [searchQuery, setSearchQuery] = useState<string>('');

  // Load movies from the data source
  const { movies, providers, isLoading, error } = useMovies();

  // Filter available recognition types into festivals and critics
  const availableFestivals = moviesData.recognitionTypes.filter(r => FESTIVAL_AWARDS.includes(r));
  const availableCritics = moviesData.recognitionTypes.filter(r => CRITICS_PICKS.includes(r));

  // Get unique streaming services from movies for selected region (subscription only)
  const availableStreamingServices = useMemo(() => {
    const services = new Set<string>();
    movies.forEach(movie => {
      const regionRefs = movie.streaming?.[streamingRegion] || [];
      regionRefs.forEach(ref => {
        if (ref.type === 'subscription') {
          const provider = providers[ref.id];
          if (provider) {
            services.add(provider.name);
          }
        }
      });
    });
    return Array.from(services).sort();
  }, [movies, providers, streamingRegion]);

  // Get unique countries from movies
  const availableCountries = useMemo(() => {
    const countries = new Set<string>();
    movies.forEach(movie => {
      if (movie.country) {
        countries.add(movie.country);
      }
    });
    return Array.from(countries).sort();
  }, [movies]);

  // Get available decades from movies
  const availableDecades = useMemo(() => {
    const decades = new Set<string>();
    movies.forEach(movie => {
      if (movie.year) {
        const decade = `${Math.floor(movie.year / 10) * 10}s`;
        decades.add(decade);
      }
    });
    return Array.from(decades).sort().reverse();
  }, [movies]);

  // Get unique genres from movies
  const availableGenres = useMemo(() => {
    const genres = new Set<string>();
    movies.forEach(movie => {
      movie.genres?.forEach(genre => genres.add(genre));
    });
    return Array.from(genres).sort();
  }, [movies]);

  // Compute counts for each filter option
  const awardsCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    [...availableFestivals, ...availableCritics].forEach(award => {
      counts[award] = movies.filter(movie =>
        movie.recognitions?.some(r => r.type === award)
      ).length;
    });
    return counts;
  }, [movies, availableFestivals, availableCritics]);

  const streamingCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    availableStreamingServices.forEach(service => {
      counts[service] = movies.filter(movie => {
        const regionRefs = movie.streaming?.[streamingRegion] || [];
        return regionRefs.some(ref => {
          const provider = providers[ref.id];
          return provider?.name === service;
        });
      }).length;
    });
    return counts;
  }, [movies, providers, availableStreamingServices, streamingRegion]);

  const countryCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    availableCountries.forEach(country => {
      counts[country] = movies.filter(movie => movie.country === country).length;
    });
    return counts;
  }, [movies, availableCountries]);

  const decadeCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    availableDecades.forEach(decade => {
      const decadeStart = parseInt(decade);
      counts[decade] = movies.filter(movie => {
        if (!movie.year) return false;
        const movieDecade = Math.floor(movie.year / 10) * 10;
        return movieDecade === decadeStart;
      }).length;
    });
    return counts;
  }, [movies, availableDecades]);

  const genreCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    availableGenres.forEach(genre => {
      counts[genre] = movies.filter(movie =>
        movie.genres?.includes(genre)
      ).length;
    });
    return counts;
  }, [movies, availableGenres]);

  // Apply filters and search to the movie list
  const filteredMovies = useFilteredMovies(
    movies, 
    awardsFilters, 
    searchQuery, 
    streamingFilters,
    streamingRegion,
    providers,
    countryFilters,
    decadeFilters,
    genreFilters,
    minRating
  );

  // Handle loading state
  if (isLoading) {
    return (
      <div className="movie-catalog">
        <div className="movie-catalog__loading">
          <p>Loading movies...</p>
        </div>
      </div>
    );
  }

  // Handle error state
  if (error) {
    return (
      <div className="movie-catalog">
        <div className="movie-catalog__error">
          <p>Error loading movies: {error.message}</p>
          <button 
            type="button" 
            onClick={() => window.location.reload()}
            className="movie-catalog__retry-button"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  // Check if filters or search are active
  const hasActiveFiltersOrSearch = awardsFilters.length > 0 || streamingFilters.length > 0 || countryFilters.length > 0 || decadeFilters.length > 0 || genreFilters.length > 0 || minRating > 0 || searchQuery.trim() !== '';

  const clearAllFilters = () => {
    setAwardsFilters([]);
    setStreamingFilters([]);
    setCountryFilters([]);
    setDecadeFilters([]);
    setGenreFilters([]);
    setMinRating(0);
    setSearchQuery('');
  };

  return (
    <div className="movie-catalog">
      <header className="movie-catalog__header">
        <h1 className="movie-catalog__title">A Night To Remember</h1>
      </header>

      <div className="movie-catalog__controls">
        <div className="movie-catalog__filters">
          <GroupedFilterDropdown
            label="Awards"
            groups={[
              { label: "Festivals", options: availableFestivals },
              { label: "Critics' Picks", options: availableCritics },
            ]}
            selected={awardsFilters}
            onChange={setAwardsFilters}
            counts={awardsCounts}
          />
          <div className="movie-catalog__streaming-group">
            {availableStreamingServices.length > 0 && (
              <FilterDropdown
                label="Streaming"
                options={availableStreamingServices}
                selected={streamingFilters}
                onChange={setStreamingFilters}
                counts={streamingCounts}
              />
            )}
          </div>
          <FilterDropdown
            label="Country"
            options={availableCountries}
            selected={countryFilters}
            onChange={setCountryFilters}
            counts={countryCounts}
          />
          <FilterDropdown
            label="Decade"
            options={availableDecades}
            selected={decadeFilters}
            onChange={setDecadeFilters}
            counts={decadeCounts}
          />
          {availableGenres.length > 0 && (
            <FilterDropdown
              label="Genre"
              options={availableGenres}
              selected={genreFilters}
              onChange={setGenreFilters}
              counts={genreCounts}
            />
          )}
          <RatingSlider value={minRating} onChange={setMinRating} />
          {hasActiveFiltersOrSearch && (
            <button
              type="button"
              className="movie-catalog__clear-all"
              onClick={clearAllFilters}
            >
              Clear All
            </button>
          )}
        </div>
        <div className="movie-catalog__search">
          <select
            className="movie-catalog__region-select"
            value={streamingRegion}
            onChange={(e) => {
              setStreamingRegion(e.target.value);
              setStreamingFilters([]); // Clear streaming filters when region changes
            }}
            title="Streaming region"
          >
            {STREAMING_REGIONS.map(r => (
              <option key={r.code} value={r.code}>{r.name}</option>
            ))}
          </select>
          <SearchInput value={searchQuery} onChange={setSearchQuery} />
        </div>
      </div>

      <main className="movie-catalog__content">
        {filteredMovies.length === 0 && hasActiveFiltersOrSearch ? (
          <div className="movie-catalog__empty">
            <p>No movies match your current filters or search.</p>
            <button
              type="button"
              onClick={clearAllFilters}
              className="movie-catalog__clear-button"
            >
              Clear all filters
            </button>
          </div>
        ) : filteredMovies.length === 0 ? (
          <div className="movie-catalog__empty">
            <p>No movies are currently available.</p>
          </div>
        ) : (
          <MovieGrid 
            movies={filteredMovies} 
            providers={providers}
            streamingRegion={streamingRegion}
          />
        )}
      </main>
    </div>
  );
}

export default MovieCatalog;
