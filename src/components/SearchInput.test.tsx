import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { SearchInput } from './SearchInput';

describe('SearchInput', () => {
  describe('renders correctly', () => {
    it('should render a text input with placeholder', () => {
      const onChange = vi.fn();
      render(<SearchInput value="" onChange={onChange} />);

      const input = screen.getByRole('textbox');
      expect(input).toBeInTheDocument();
      expect(input).toHaveAttribute('placeholder', 'Search by title or director...');
    });

    it('should render with the provided value', () => {
      const onChange = vi.fn();
      render(<SearchInput value="Parasite" onChange={onChange} />);

      const input = screen.getByRole('textbox');
      expect(input).toHaveValue('Parasite');
    });

    it('should have accessible label', () => {
      const onChange = vi.fn();
      render(<SearchInput value="" onChange={onChange} />);

      const input = screen.getByLabelText('Search movies by title or director');
      expect(input).toBeInTheDocument();
    });
  });

  describe('clear button visibility', () => {
    it('should not show clear button when value is empty', () => {
      const onChange = vi.fn();
      render(<SearchInput value="" onChange={onChange} />);

      const clearButton = screen.queryByRole('button', { name: 'Clear search' });
      expect(clearButton).not.toBeInTheDocument();
    });

    it('should show clear button when value is not empty', () => {
      const onChange = vi.fn();
      render(<SearchInput value="test" onChange={onChange} />);

      const clearButton = screen.getByRole('button', { name: 'Clear search' });
      expect(clearButton).toBeInTheDocument();
    });

    it('should show clear button for single character input', () => {
      const onChange = vi.fn();
      render(<SearchInput value="a" onChange={onChange} />);

      const clearButton = screen.getByRole('button', { name: 'Clear search' });
      expect(clearButton).toBeInTheDocument();
    });
  });

  describe('onChange callback', () => {
    it('should call onChange when input value changes', () => {
      const onChange = vi.fn();
      render(<SearchInput value="" onChange={onChange} />);

      const input = screen.getByRole('textbox');
      fireEvent.change(input, { target: { value: 'Bong Joon-ho' } });

      expect(onChange).toHaveBeenCalledWith('Bong Joon-ho');
    });

    it('should call onChange with empty string when clear button is clicked', () => {
      const onChange = vi.fn();
      render(<SearchInput value="test query" onChange={onChange} />);

      const clearButton = screen.getByRole('button', { name: 'Clear search' });
      fireEvent.click(clearButton);

      expect(onChange).toHaveBeenCalledWith('');
    });
  });

  describe('user interactions', () => {
    it('should allow typing in the input', () => {
      const onChange = vi.fn();
      render(<SearchInput value="" onChange={onChange} />);

      const input = screen.getByRole('textbox');
      fireEvent.change(input, { target: { value: 'Wong Kar-wai' } });

      expect(onChange).toHaveBeenCalledTimes(1);
      expect(onChange).toHaveBeenCalledWith('Wong Kar-wai');
    });

    it('should handle multiple input changes', () => {
      const onChange = vi.fn();
      const { rerender } = render(<SearchInput value="" onChange={onChange} />);

      const input = screen.getByRole('textbox');
      
      fireEvent.change(input, { target: { value: 'P' } });
      expect(onChange).toHaveBeenLastCalledWith('P');

      rerender(<SearchInput value="P" onChange={onChange} />);
      fireEvent.change(input, { target: { value: 'Pa' } });
      expect(onChange).toHaveBeenLastCalledWith('Pa');

      rerender(<SearchInput value="Pa" onChange={onChange} />);
      fireEvent.change(input, { target: { value: 'Parasite' } });
      expect(onChange).toHaveBeenLastCalledWith('Parasite');
    });
  });
});
