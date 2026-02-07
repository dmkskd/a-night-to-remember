import { useState, useRef, useEffect } from 'react';
import './FilterDropdown.css';

interface FilterGroup {
  label: string;
  options: string[];
}

interface GroupedFilterDropdownProps {
  label: string;
  groups: FilterGroup[];
  selected: string[];
  onChange: (selected: string[]) => void;
  counts?: Record<string, number>;
}

/**
 * Grouped filter dropdown - single button that expands to show
 * multiple categories with section headers.
 */
export function GroupedFilterDropdown({ 
  label, 
  groups, 
  selected, 
  onChange, 
  counts 
}: GroupedFilterDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

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
        <div className="filter-dropdown__panel filter-dropdown__panel--grouped">
          <div className="filter-dropdown__columns">
            {groups.map((group) => (
              <div key={group.label} className="filter-dropdown__group">
                <h4 className="filter-dropdown__group-label">{group.label}</h4>
                <div className="filter-dropdown__options">
                  {group.options.map(option => (
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
              </div>
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

export default GroupedFilterDropdown;
