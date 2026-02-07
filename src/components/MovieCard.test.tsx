import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { MovieCard } from './MovieCard';
import type { Movie } from '../types/movie';

// Helper to create a movie with default values
const createMovie = (overrides: Partial<Movie> = {}): Movie => ({
  id: 'test-movie-2020',
  title: 'Test Movie',
  director: 'Test Director',
  year: 2020,
  recognitions: [],
  ...overrides,
});

// Helper to render MovieCard with router context
const renderMovieCard = (movie: Movie) => {
  return render(
    <MemoryRouter>
      <MovieCard movie={movie} />
    </MemoryRouter>
  );
};

describe('MovieCard', () => {
  describe('displays required information', () => {
    it('should display movie title', () => {
      const movie = createMovie({ title: 'Parasite' });
      renderMovieCard(movie);

      expect(screen.getByText('Parasite')).toBeInTheDocument();
    });

    it('should display movie director', () => {
      const movie = createMovie({ director: 'Bong Joon-ho' });
      renderMovieCard(movie);

      expect(screen.getByText('Bong Joon-ho')).toBeInTheDocument();
    });

    it('should display movie year', () => {
      const movie = createMovie({ year: 2019 });
      renderMovieCard(movie);

      expect(screen.getByText('2019')).toBeInTheDocument();
    });

    it('should display all required fields together', () => {
      const movie = createMovie({
        title: 'Portrait of a Lady on Fire',
        director: 'Céline Sciamma',
        year: 2019,
      });
      renderMovieCard(movie);

      expect(screen.getByText('Portrait of a Lady on Fire')).toBeInTheDocument();
      expect(screen.getByText('Céline Sciamma')).toBeInTheDocument();
      expect(screen.getByText('2019')).toBeInTheDocument();
    });
  });

  describe('poster image handling', () => {
    it('should display poster image when posterUrl is provided', () => {
      const movie = createMovie({
        title: 'Test Movie',
        posterUrl: 'https://example.com/poster.jpg',
      });
      renderMovieCard(movie);

      const img = screen.getByRole('img', { name: /test movie poster/i });
      expect(img).toHaveAttribute('src', 'https://example.com/poster.jpg');
    });

    it('should display placeholder when posterUrl is missing', () => {
      const movie = createMovie({
        title: 'Test Movie',
        posterUrl: undefined,
      });
      renderMovieCard(movie);

      const img = screen.getByRole('img', { name: /test movie poster/i });
      expect(img).toHaveAttribute('src', expect.stringContaining('placeholder'));
    });

    it('should have alt text with movie title', () => {
      const movie = createMovie({ title: 'Shoplifters' });
      renderMovieCard(movie);

      const img = screen.getByRole('img');
      expect(img).toHaveAttribute('alt', 'Shoplifters poster');
    });
  });

  describe('navigation', () => {
    it('should be a link to the movie detail page', () => {
      const movie = createMovie({ id: 'parasite-2019' });
      renderMovieCard(movie);

      const link = screen.getByRole('link');
      expect(link).toHaveAttribute('href', '/movie/parasite-2019');
    });

    it('should use the movie id in the link path', () => {
      const movie = createMovie({ id: 'portrait-lady-fire-2019' });
      renderMovieCard(movie);

      const link = screen.getByRole('link');
      expect(link).toHaveAttribute('href', '/movie/portrait-lady-fire-2019');
    });
  });

  describe('renders correctly with minimal data', () => {
    it('should render with only required fields', () => {
      const minimalMovie: Movie = {
        id: 'minimal-2020',
        title: 'Minimal Movie',
        director: 'Minimal Director',
        year: 2020,
        recognitions: [],
      };
      renderMovieCard(minimalMovie);

      expect(screen.getByText('Minimal Movie')).toBeInTheDocument();
      expect(screen.getByText('Minimal Director')).toBeInTheDocument();
      expect(screen.getByText('2020')).toBeInTheDocument();
      expect(screen.getByRole('link')).toHaveAttribute('href', '/movie/minimal-2020');
    });
  });

  describe('renders correctly with full data', () => {
    it('should render with all fields populated', () => {
      const fullMovie: Movie = {
        id: 'full-movie-2019',
        title: 'Full Movie',
        director: 'Full Director',
        year: 2019,
        synopsis: 'A complete movie with all fields',
        posterUrl: 'https://example.com/full-poster.jpg',
        country: 'France',
        runtime: 120,
        cast: ['Actor 1', 'Actor 2'],
        genres: ['Drama', 'Romance'],
        recognitions: [{ type: 'Cannes Palme d\'Or', year: 2019 }],
        tags: ['art-house', 'slow cinema'],
      };
      renderMovieCard(fullMovie);

      // MovieCard only displays title, director, year, and poster
      expect(screen.getByText('Full Movie')).toBeInTheDocument();
      expect(screen.getByText('Full Director')).toBeInTheDocument();
      expect(screen.getByText('2019')).toBeInTheDocument();
      
      const img = screen.getByRole('img');
      expect(img).toHaveAttribute('src', 'https://example.com/full-poster.jpg');
    });
  });
});
