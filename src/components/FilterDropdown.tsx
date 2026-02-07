import { useState, useRef, useEffect } from 'react';
import './FilterDropdown.css';

interface FilterDropdownProps {
  label: string;
  options: string[];
  selected: string[];
  onChange: (selected: string[]) => void;
  counts?: Record<string, number>;
}

/**
 * Collapsible filter dropdown component.
 * Shows a button with the filter category name, expands on click to show options.
 */
export function FilterDropdown({ label, options, selected, onChange, counts }: FilterDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const toggleOption = (option: string) => {
    if (selected.includes(option)) {
      onChange(selected.filter(s => s !== option));
    } else {
      onChange([...selected, option]);
    }
  };

  const clearAll = () => {
    onChange([]);
  };

  const activeCount = selected.length;

  return (
    <div 
      ref={dropdownRef}
      className={`filter-dropdown ${isOpen ? 'filter-dropdown--open' : ''}`}
    >
      <button
        type="button"
        className={`filter-dropdown__trigger ${activeCount > 0 ? 'filter-dropdown__trigger--active' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className="filter-dropdown__label">{label}</span>
        {activeCount > 0 && (
          <span className="filter-dropdown__count">{activeCount}</span>
        )}
        <span className="filter-dropdown__arrow">{isOpen ? '▲' : '▼'}</span>
      </button>
      
      {isOpen && (
        <div className="filter-dropdown__panel">
          <div className="filter-dropdown__options">
            {options.map(option => (
              <button
                key={option}
                type="button"
                className={`filter-dropdown__option ${selected.includes(option) ? 'filter-dropdown__option--selected' : ''}`}
                onClick={() => toggleOption(option)}
              >
                <span>{option}</span>
                {counts && counts[option] !== undefined && (
                  <span className="filter-dropdown__option-count">{counts[option]}</span>
                )}
              </button>
            ))}
          </div>
          {activeCount > 0 && (
            <button
              type="button"
              className="filter-dropdown__clear"
              onClick={clearAll}
            >
              Clear {label}
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default FilterDropdown;
