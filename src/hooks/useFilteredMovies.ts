import { useMemo } from 'react';
import type { Movie, ProvidersLookup } from '../types/movie';

/**
 * Custom hook for filtering movies based on recognition types, streaming services, country, decade, and search query.
 * Applies all filters together using AND logic.
 * 
 * @param movies - Array of movies to filter
 * @param filters - Array of recognition types to filter by (empty array means no filter)
 * @param searchQuery - Search query to match against title or director (empty string means no filter)
 * @param streamingFilters - Array of streaming service names to filter by (empty array means no filter)
 * @param streamingRegion - Region code for streaming availability (e.g., 'US', 'GB')
 * @param providers - Providers lookup table
 * @param countryFilters - Array of countries to filter by (empty array means no filter)
 * @param decadeFilters - Array of decades to filter by (empty array means no filter)
 * @returns Filtered array of movies
 * 
 * Validates: Requirements 3.1, 4.1
 */
export function useFilteredMovies(
  movies: Movie[],
  filters: string[],
  searchQuery: string,
  streamingFilters: string[] = [],
  streamingRegion: string = 'US',
  providers: ProvidersLookup = {},
  countryFilters: string[] = [],
  decadeFilters: string[] = [],
  genreFilters: string[] = [],
  minRating: number = 0
): Movie[] {
  return useMemo(() => {
    let result = movies;

    // Apply recognition filter if filters array is not empty
    // Only include movies that have at least one recognition matching any of the filter types
    if (filters.length > 0) {
      result = result.filter((movie) =>
        movie.recognitions?.some((recognition) =>
          filters.includes(recognition.type)
        )
      );
    }

    // Apply streaming filter if streamingFilters array is not empty
    // Only include movies available on at least one of the selected streaming services in the selected region
    if (streamingFilters.length > 0) {
      result = result.filter((movie) => {
        const regionRefs = movie.streaming?.[streamingRegion] || [];
        return regionRefs.some((ref) => {
          const provider = providers[ref.id];
          return provider && streamingFilters.includes(provider.name);
        });
      });
    }

    // Apply country filter if countryFilters array is not empty
    if (countryFilters.length > 0) {
      result = result.filter((movie) =>
        movie.country && countryFilters.includes(movie.country)
      );
    }

    // Apply decade filter if decadeFilters array is not empty
    if (decadeFilters.length > 0) {
      result = result.filter((movie) => {
        if (!movie.year) return false;
        const decade = `${Math.floor(movie.year / 10) * 10}s`;
        return decadeFilters.includes(decade);
      });
    }

    // Apply genre filter if genreFilters array is not empty
    if (genreFilters.length > 0) {
      result = result.filter((movie) =>
        movie.genres?.some((genre) => genreFilters.includes(genre))
      );
    }

    // Apply minimum rating filter
    if (minRating > 0) {
      result = result.filter((movie) =>
        movie.rating && movie.rating >= minRating
      );
    }

    // Apply search filter if searchQuery is not empty
    // Match against title OR director (case-insensitive)
    const trimmedQuery = searchQuery.trim().toLowerCase();
    if (trimmedQuery) {
      result = result.filter((movie) => {
        const titleMatch = movie.title.toLowerCase().includes(trimmedQuery);
        const directorMatch = movie.director.toLowerCase().includes(trimmedQuery);
        return titleMatch || directorMatch;
      });
    }

    return result;
  }, [movies, filters, searchQuery, streamingFilters, streamingRegion, providers, countryFilters, decadeFilters, genreFilters, minRating]);
}
