import type { Movie, ProvidersLookup } from '../types/movie';
import moviesData from '../data/movies.json';

/**
 * Custom hook for loading and accessing the movie catalog.
 * Loads movies from the static JSON file.
 * 
 * @returns Object containing movies array, providers lookup, loading state, and error state
 * 
 * Validates: Requirements 1.1, 1.4
 */
export function useMovies(): {
  movies: Movie[];
  providers: ProvidersLookup;
  isLoading: boolean;
  error: Error | null;
} {
  // Data is static, no need for async loading
  const movies = moviesData.movies as Movie[];
  const providers = (moviesData as { providers?: ProvidersLookup }).providers || {};
  
  return { movies, providers, isLoading: false, error: null };
}
