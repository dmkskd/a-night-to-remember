import { describe, it, expect } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useMovies } from './useMovies';

describe('useMovies', () => {
  it('should initially be in loading state', () => {
    const { result } = renderHook(() => useMovies());
    
    // Initially should be loading
    expect(result.current.isLoading).toBe(true);
    expect(result.current.error).toBe(null);
  });

  it('should load movies from static JSON file', async () => {
    const { result } = renderHook(() => useMovies());
    
    // Wait for loading to complete
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    // Should have loaded movies
    expect(result.current.movies.length).toBeGreaterThan(0);
    expect(result.current.error).toBe(null);
  });

  it('should return movies with required fields', async () => {
    const { result } = renderHook(() => useMovies());
    
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    // Each movie should have required fields (id, title, director, year)
    result.current.movies.forEach((movie) => {
      expect(movie.id).toBeDefined();
      expect(typeof movie.id).toBe('string');
      expect(movie.title).toBeDefined();
      expect(typeof movie.title).toBe('string');
      expect(movie.director).toBeDefined();
      expect(typeof movie.director).toBe('string');
      expect(movie.year).toBeDefined();
      expect(typeof movie.year).toBe('number');
    });
  });

  it('should return movies with recognitions array', async () => {
    const { result } = renderHook(() => useMovies());
    
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    // Each movie should have recognitions array
    result.current.movies.forEach((movie) => {
      expect(Array.isArray(movie.recognitions)).toBe(true);
    });
  });

  it('should return error as null when loading succeeds', async () => {
    const { result } = renderHook(() => useMovies());
    
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    expect(result.current.error).toBe(null);
  });
});
