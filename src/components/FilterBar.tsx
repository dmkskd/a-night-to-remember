import './FilterBar.css';

interface FilterBarProps {
  /** List of recognition types to show as filter buttons */
  availableFilters: string[];
  /** Currently selected filters */
  activeFilters: string[];
  /** Callback when filters change */
  onFilterChange: (filters: string[]) => void;
}

/**
 * FilterBar component displays recognition filter controls.
 * Allows multi-select filtering with toggle buttons for each recognition type.
 * Includes a "Clear All" button to reset all filters.
 * 
 * @param availableFilters - Array of recognition types to display as filter options
 * @param activeFilters - Array of currently active filter values
 * @param onFilterChange - Callback invoked with updated filters array when selection changes
 */
export function FilterBar({ availableFilters, activeFilters, onFilterChange }: FilterBarProps) {
  /**
   * Toggles a filter on or off.
   * If the filter is currently active, removes it from the list.
   * If the filter is not active, adds it to the list.
   */
  const handleFilterToggle = (filter: string) => {
    if (activeFilters.includes(filter)) {
      onFilterChange(activeFilters.filter((f) => f !== filter));
    } else {
      onFilterChange([...activeFilters, filter]);
    }
  };

  /**
   * Clears all active filters by calling onFilterChange with an empty array.
   */
  const handleClearAll = () => {
    onFilterChange([]);
  };

  return (
    <div className="filter-bar">
      <div className="filter-bar__filters">
        {availableFilters.map((filter) => {
          const isActive = activeFilters.includes(filter);
          return (
            <button
              key={filter}
              type="button"
              className={`filter-bar__button ${isActive ? 'filter-bar__button--active' : ''}`}
              onClick={() => handleFilterToggle(filter)}
              aria-pressed={isActive}
            >
              {filter}
            </button>
          );
        })}
      </div>
      {activeFilters.length > 0 && (
        <button
          type="button"
          className="filter-bar__clear-button"
          onClick={handleClearAll}
        >
          Clear All
        </button>
      )}
    </div>
  );
}

export default FilterBar;
