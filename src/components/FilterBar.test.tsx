import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { FilterBar } from './FilterBar';

describe('FilterBar', () => {
  const availableFilters = [
    'Cannes Palme d\'Or',
    'Cannes Grand Prix',
    'Cahiers du Cinéma Top 10',
  ];

  describe('renders filter buttons', () => {
    it('should render a button for each available filter', () => {
      const onFilterChange = vi.fn();
      render(
        <FilterBar
          availableFilters={availableFilters}
          activeFilters={[]}
          onFilterChange={onFilterChange}
        />
      );

      expect(screen.getByRole('button', { name: 'Cannes Palme d\'Or' })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Cannes Grand Prix' })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Cahiers du Cinéma Top 10' })).toBeInTheDocument();
    });

    it('should render no filter buttons when availableFilters is empty', () => {
      const onFilterChange = vi.fn();
      render(
        <FilterBar
          availableFilters={[]}
          activeFilters={[]}
          onFilterChange={onFilterChange}
        />
      );

      // Only the container should exist, no buttons
      const buttons = screen.queryAllByRole('button');
      expect(buttons).toHaveLength(0);
    });
  });

  describe('visually indicates active filters', () => {
    it('should mark active filters with aria-pressed true', () => {
      const onFilterChange = vi.fn();
      render(
        <FilterBar
          availableFilters={availableFilters}
          activeFilters={['Cannes Palme d\'Or']}
          onFilterChange={onFilterChange}
        />
      );

      const activeButton = screen.getByRole('button', { name: 'Cannes Palme d\'Or' });
      const inactiveButton = screen.getByRole('button', { name: 'Cannes Grand Prix' });

      expect(activeButton).toHaveAttribute('aria-pressed', 'true');
      expect(inactiveButton).toHaveAttribute('aria-pressed', 'false');
    });

    it('should apply active class to active filter buttons', () => {
      const onFilterChange = vi.fn();
      render(
        <FilterBar
          availableFilters={availableFilters}
          activeFilters={['Cannes Grand Prix']}
          onFilterChange={onFilterChange}
        />
      );

      const activeButton = screen.getByRole('button', { name: 'Cannes Grand Prix' });
      expect(activeButton).toHaveClass('filter-bar__button--active');
    });

    it('should support multiple active filters', () => {
      const onFilterChange = vi.fn();
      render(
        <FilterBar
          availableFilters={availableFilters}
          activeFilters={['Cannes Palme d\'Or', 'Cahiers du Cinéma Top 10']}
          onFilterChange={onFilterChange}
        />
      );

      const button1 = screen.getByRole('button', { name: 'Cannes Palme d\'Or' });
      const button2 = screen.getByRole('button', { name: 'Cahiers du Cinéma Top 10' });
      const button3 = screen.getByRole('button', { name: 'Cannes Grand Prix' });

      expect(button1).toHaveAttribute('aria-pressed', 'true');
      expect(button2).toHaveAttribute('aria-pressed', 'true');
      expect(button3).toHaveAttribute('aria-pressed', 'false');
    });
  });

  describe('toggle filter on click', () => {
    it('should add filter when clicking inactive filter', () => {
      const onFilterChange = vi.fn();
      render(
        <FilterBar
          availableFilters={availableFilters}
          activeFilters={[]}
          onFilterChange={onFilterChange}
        />
      );

      const button = screen.getByRole('button', { name: 'Cannes Palme d\'Or' });
      fireEvent.click(button);

      expect(onFilterChange).toHaveBeenCalledWith(['Cannes Palme d\'Or']);
    });

    it('should remove filter when clicking active filter', () => {
      const onFilterChange = vi.fn();
      render(
        <FilterBar
          availableFilters={availableFilters}
          activeFilters={['Cannes Palme d\'Or', 'Cannes Grand Prix']}
          onFilterChange={onFilterChange}
        />
      );

      const button = screen.getByRole('button', { name: 'Cannes Palme d\'Or' });
      fireEvent.click(button);

      expect(onFilterChange).toHaveBeenCalledWith(['Cannes Grand Prix']);
    });

    it('should add to existing filters when clicking new filter', () => {
      const onFilterChange = vi.fn();
      render(
        <FilterBar
          availableFilters={availableFilters}
          activeFilters={['Cannes Palme d\'Or']}
          onFilterChange={onFilterChange}
        />
      );

      const button = screen.getByRole('button', { name: 'Cannes Grand Prix' });
      fireEvent.click(button);

      expect(onFilterChange).toHaveBeenCalledWith(['Cannes Palme d\'Or', 'Cannes Grand Prix']);
    });
  });

  describe('clear all button', () => {
    it('should show Clear All button when filters are active', () => {
      const onFilterChange = vi.fn();
      render(
        <FilterBar
          availableFilters={availableFilters}
          activeFilters={['Cannes Palme d\'Or']}
          onFilterChange={onFilterChange}
        />
      );

      expect(screen.getByRole('button', { name: 'Clear All' })).toBeInTheDocument();
    });

    it('should not show Clear All button when no filters are active', () => {
      const onFilterChange = vi.fn();
      render(
        <FilterBar
          availableFilters={availableFilters}
          activeFilters={[]}
          onFilterChange={onFilterChange}
        />
      );

      expect(screen.queryByRole('button', { name: 'Clear All' })).not.toBeInTheDocument();
    });

    it('should call onFilterChange with empty array when Clear All is clicked', () => {
      const onFilterChange = vi.fn();
      render(
        <FilterBar
          availableFilters={availableFilters}
          activeFilters={['Cannes Palme d\'Or', 'Cannes Grand Prix']}
          onFilterChange={onFilterChange}
        />
      );

      const clearButton = screen.getByRole('button', { name: 'Clear All' });
      fireEvent.click(clearButton);

      expect(onFilterChange).toHaveBeenCalledWith([]);
    });
  });
});
