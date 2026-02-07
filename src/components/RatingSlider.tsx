import { useState, useRef, useEffect } from 'react';
import './RatingSlider.css';

interface RatingSliderProps {
  value: number;
  onChange: (value: number) => void;
}

/**
 * Rating slider component styled as a dropdown.
 */
export function RatingSlider({ value, onChange }: RatingSliderProps) {
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

  const isActive = value > 0;

  return (
    <div 
      ref={dropdownRef}
      className={`rating-slider ${isOpen ? 'rating-slider--open' : ''}`}
    >
      <button
        type="button"
        className={`rating-slider__trigger ${isActive ? 'rating-slider__trigger--active' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className="rating-slider__label">Rating</span>
        {isActive && (
          <span className="rating-slider__badge">{value}+</span>
        )}
        <span className="rating-slider__arrow">{isOpen ? '▲' : '▼'}</span>
      </button>
      
      {isOpen && (
        <div className="rating-slider__panel">
          <div className="rating-slider__content">
            <div className="rating-slider__display">
              <span className="rating-slider__star">★</span>
              <span className="rating-slider__value">{value > 0 ? `${value}+` : 'Any'}</span>
            </div>
            <input
              type="range"
              min="0"
              max="9"
              step="0.5"
              value={value}
              onChange={(e) => onChange(parseFloat(e.target.value))}
              className="rating-slider__input"
            />
          </div>
          {isActive && (
            <button
              type="button"
              className="rating-slider__clear"
              onClick={() => onChange(0)}
            >
              Clear Rating
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default RatingSlider;
