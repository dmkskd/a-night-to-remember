import { describe, it, expect } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useMovie } from './useMovie';

describe('useMovie', () => {
  it('should initially be in loading state', () => {
    const { result } = renderHook(() => useMovie('parasite-2019'));
    
    // Initially should be loading
    expect(result.current.isLoading).toBe(true);
    expect(result.current.error).toBe(null);
    expect(result.current.movie).toBe(null);
  });

  it('should return a movie when given a valid ID', async () => {
    const { result } = renderHook(() => useMovie('parasite-2019'));
    
    // Wait for loading to complete
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    // Should have found the movie
    expect(result.current.movie).not.toBe(null);
    expect(result.current.movie?.id).toBe('parasite-2019');
    expect(result.current.movie?.title).toBe('Parasite');
    expect(result.current.error).toBe(null);
  });

  it('should return null when given an invalid ID', async () => {
    const { result } = renderHook(() => useMovie('non-existent-movie'));
    
    // Wait for loading to complete
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    // Should not have found a movie
    expect(result.current.movie).toBe(null);
    expect(result.current.error).toBe(null);
  });

  it('should return movie with required fields', async () => {
    const { result } = renderHook(() => useMovie('parasite-2019'));
    
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    const movie = result.current.movie;
    expect(movie).not.toBe(null);
    
    // Movie should have required fields (id, title, director, year)
    expect(movie?.id).toBeDefined();
    expect(typeof movie?.id).toBe('string');
    expect(movie?.title).toBeDefined();
    expect(typeof movie?.title).toBe('string');
    expect(movie?.director).toBeDefined();
    expect(typeof movie?.director).toBe('string');
    expect(movie?.year).toBeDefined();
    expect(typeof movie?.year).toBe('number');
  });

  it('should update movie when ID changes', async () => {
    const { result, rerender } = renderHook(
      ({ id }) => useMovie(id),
      { initialProps: { id: 'parasite-2019' } }
    );
    
    // Wait for initial load
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    expect(result.current.movie?.id).toBe('parasite-2019');
    
    // Change the ID
    rerender({ id: 'portrait-of-a-lady-on-fire-2019' });
    
    // Wait for the update
    await waitFor(() => {
      expect(result.current.movie?.id).toBe('portrait-of-a-lady-on-fire-2019');
    });
  });

  it('should return null for empty string ID', async () => {
    const { result } = renderHook(() => useMovie(''));
    
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    expect(result.current.movie).toBe(null);
    expect(result.current.error).toBe(null);
  });
});
