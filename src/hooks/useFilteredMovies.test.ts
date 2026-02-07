import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useFilteredMovies } from './useFilteredMovies';
import type { Movie } from '../types/movie';

// Test fixtures
const createMovie = (overrides: Partial<Movie> = {}): Movie => ({
  id: 'test-movie-2020',
  title: 'Test Movie',
  director: 'Test Director',
  year: 2020,
  recognitions: [],
  ...overrides,
});

const sampleMovies: Movie[] = [
  createMovie({
    id: 'parasite-2019',
    title: 'Parasite',
    director: 'Bong Joon-ho',
    year: 2019,
    recognitions: [
      { type: 'Cannes Palme d\'Or', year: 2019 },
      { type: 'Academy Award', year: 2020 },
    ],
  }),
  createMovie({
    id: 'portrait-2019',
    title: 'Portrait of a Lady on Fire',
    director: 'Céline Sciamma',
    year: 2019,
    recognitions: [
      { type: 'Cannes Best Screenplay', year: 2019 },
    ],
  }),
  createMovie({
    id: 'shoplifters-2018',
    title: 'Shoplifters',
    director: 'Hirokazu Kore-eda',
    year: 2018,
    recognitions: [
      { type: 'Cannes Palme d\'Or', year: 2018 },
    ],
  }),
  createMovie({
    id: 'roma-2018',
    title: 'Roma',
    director: 'Alfonso Cuarón',
    year: 2018,
    recognitions: [
      { type: 'Venice Golden Lion', year: 2018 },
    ],
  }),
];

describe('useFilteredMovies', () => {
  describe('with no filters and no search query', () => {
    it('should return all movies when filters and search are empty', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, [], '')
      );

      expect(result.current).toHaveLength(sampleMovies.length);
      expect(result.current).toEqual(sampleMovies);
    });

    it('should return empty array when movies array is empty', () => {
      const { result } = renderHook(() =>
        useFilteredMovies([], [], '')
      );

      expect(result.current).toHaveLength(0);
    });
  });

  describe('with recognition filters', () => {
    it('should filter movies by single recognition type', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, ['Cannes Palme d\'Or'], '')
      );

      expect(result.current).toHaveLength(2);
      expect(result.current.map((m) => m.id)).toEqual([
        'parasite-2019',
        'shoplifters-2018',
      ]);
    });

    it('should filter movies by multiple recognition types (OR logic within filters)', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, ['Cannes Palme d\'Or', 'Venice Golden Lion'], '')
      );

      expect(result.current).toHaveLength(3);
      expect(result.current.map((m) => m.id)).toEqual([
        'parasite-2019',
        'shoplifters-2018',
        'roma-2018',
      ]);
    });

    it('should return empty array when no movies match the filter', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, ['Non-existent Award'], '')
      );

      expect(result.current).toHaveLength(0);
    });

    it('should handle movies with no recognitions', () => {
      const moviesWithNoRecognitions = [
        createMovie({ id: 'no-awards', recognitions: [] }),
        ...sampleMovies,
      ];

      const { result } = renderHook(() =>
        useFilteredMovies(moviesWithNoRecognitions, ['Cannes Palme d\'Or'], '')
      );

      // Should not include the movie with no recognitions
      expect(result.current.find((m) => m.id === 'no-awards')).toBeUndefined();
    });
  });

  describe('with search query', () => {
    it('should filter movies by title (case-insensitive)', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, [], 'parasite')
      );

      expect(result.current).toHaveLength(1);
      expect(result.current[0].id).toBe('parasite-2019');
    });

    it('should filter movies by director (case-insensitive)', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, [], 'bong')
      );

      expect(result.current).toHaveLength(1);
      expect(result.current[0].id).toBe('parasite-2019');
    });

    it('should match partial title', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, [], 'portrait')
      );

      expect(result.current).toHaveLength(1);
      expect(result.current[0].id).toBe('portrait-2019');
    });

    it('should match partial director name', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, [], 'cuarón')
      );

      expect(result.current).toHaveLength(1);
      expect(result.current[0].id).toBe('roma-2018');
    });

    it('should return empty array when no movies match the search', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, [], 'nonexistent')
      );

      expect(result.current).toHaveLength(0);
    });

    it('should treat whitespace-only search as empty', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, [], '   ')
      );

      expect(result.current).toHaveLength(sampleMovies.length);
    });
  });

  describe('with both filters and search query (AND logic)', () => {
    it('should apply both recognition filter and search query', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, ['Cannes Palme d\'Or'], 'bong')
      );

      // Only Parasite matches both: has Palme d'Or AND director contains "bong"
      expect(result.current).toHaveLength(1);
      expect(result.current[0].id).toBe('parasite-2019');
    });

    it('should return empty when filter matches but search does not', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, ['Cannes Palme d\'Or'], 'cuarón')
      );

      // Cuarón directed Roma which has Venice Golden Lion, not Palme d'Or
      expect(result.current).toHaveLength(0);
    });

    it('should return empty when search matches but filter does not', () => {
      const { result } = renderHook(() =>
        useFilteredMovies(sampleMovies, ['Non-existent Award'], 'parasite')
      );

      expect(result.current).toHaveLength(0);
    });
  });

  describe('memoization', () => {
    it('should return same reference when inputs do not change', () => {
      const filters: string[] = [];
      const searchQuery = '';

      const { result, rerender } = renderHook(
        ({ movies, filters, searchQuery }) =>
          useFilteredMovies(movies, filters, searchQuery),
        { initialProps: { movies: sampleMovies, filters, searchQuery } }
      );

      const firstResult = result.current;

      // Rerender with same inputs
      rerender({ movies: sampleMovies, filters, searchQuery });

      expect(result.current).toBe(firstResult);
    });
  });
});
