import './SearchInput.css';

interface SearchInputProps {
  /** Current search query value */
  value: string;
  /** Callback when query changes */
  onChange: (query: string) => void;
  /** Placeholder text */
  placeholder?: string;
}

/**
 * SearchInput component provides a text input for searching movies.
 * Displays a clear button (X) when the input has text.
 * 
 * @param value - Current search query string
 * @param onChange - Callback invoked with the new query when input changes
 */
export function SearchInput({ value, onChange, placeholder = "Search by title or director..." }: SearchInputProps) {
  /**
   * Handles input change events and calls onChange with the new value.
   */
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.value);
  };

  /**
   * Clears the search query by calling onChange with an empty string.
   */
  const handleClear = () => {
    onChange('');
  };

  return (
    <div className="search-input">
      <input
        type="text"
        className="search-input__field"
        value={value}
        onChange={handleInputChange}
        placeholder={placeholder}
        aria-label="Search"
      />
      {value && (
        <button
          type="button"
          className="search-input__clear-button"
          onClick={handleClear}
          aria-label="Clear search"
        >
          ×
        </button>
      )}
    </div>
  );
}

export default SearchInput;
