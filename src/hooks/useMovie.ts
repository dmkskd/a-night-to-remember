import { useMemo } from 'react';
import type { Movie } from '../types/movie';
import { useMovies } from './useMovies';

/**
 * Custom hook for getting a single movie by ID.
 * Internally uses useMovies to load the catalog and finds the specific movie.
 * 
 * @param id - The unique identifier of the movie to retrieve
 * @returns Object containing the movie (or null if not found), loading state, and error state
 * 
 * Validates: Requirements 2.1
 */
export function useMovie(id: string): {
  movie: Movie | null;
  isLoading: boolean;
  error: Error | null;
} {
  const { movies, isLoading, error } = useMovies();

  const movie = useMemo(() => {
    if (isLoading || error) {
      return null;
    }
    return movies.find((m) => m.id === id) ?? null;
  }, [movies, id, isLoading, error]);

  return { movie, isLoading, error };
}
