import { useState, useMemo, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { StoryCard } from '../components/StoryCard'
import { FilterDropdown } from '../components/FilterDropdown'
import { SearchInput } from '../components/SearchInput'
import type { Story } from '../types/story'
import storiesData from '../data/stories.json'
import './StoriesCatalog.css'

const stories = (storiesData as { stories: Story[] }).stories
const recognitionTypes = (storiesData as { recognitionTypes: string[] }).recognitionTypes || []
const allGenres = (storiesData as { genres: string[] }).genres || []
const allThemes = (storiesData as { themes: string[] }).themes || []

/**
 * StoriesCatalog page - browse short stories catalog with filters.
 */
export function StoriesCatalog({ showTitle = true }: { showTitle?: boolean }) {
  const [searchParams, setSearchParams] = useSearchParams()
  
  const [searchQuery, setSearchQueryState] = useState<string>(() => {
    return searchParams.get('q') || ''
  })
  
  const setSearchQuery = (query: string) => {
    setSearchQueryState(query)
    const newParams = new URLSearchParams(searchParams)
    if (query) {
      newParams.set('q', query)
    } else {
      newParams.delete('q')
    }
    setSearchParams(newParams)
  }

  const [awardsFilters, setAwardsFilters] = useState<string[]>([])
  const [genreFilters, setGenreFilters] = useState<string[]>(() => {
    const genreParam = searchParams.get('genre')
    return genreParam ? [genreParam] : []
  })
  const [themeFilters, setThemeFilters] = useState<string[]>([])
  const [onlineOnly, setOnlineOnly] = useState<boolean>(false)
  
  // Sync genre filter from URL
  useEffect(() => {
    const genreParam = searchParams.get('genre')
    if (genreParam && !genreFilters.includes(genreParam)) {
      setGenreFilters([genreParam])
    }
  }, [searchParams])

  // Compute counts
  const awardsCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    recognitionTypes.forEach(type => {
      counts[type] = stories.filter(story =>
        story.recognitions?.some(r => r.type === type)
      ).length
    })
    return counts
  }, [])

  const genreCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    allGenres.forEach(genre => {
      counts[genre] = stories.filter(story =>
        story.genres?.includes(genre)
      ).length
    })
    return counts
  }, [])

  const themeCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    allThemes.forEach(theme => {
      counts[theme] = stories.filter(story =>
        story.themes?.includes(theme)
      ).length
    })
    return counts
  }, [])

  // Filter stories
  const filteredStories = useMemo(() => {
    let result = stories

    // Awards filter
    if (awardsFilters.length > 0) {
      result = result.filter(story =>
        story.recognitions?.some(r => awardsFilters.includes(r.type))
      )
    }

    // Genre filter
    if (genreFilters.length > 0) {
      result = result.filter(story =>
        story.genres?.some(g => genreFilters.includes(g))
      )
    }

    // Theme filter
    if (themeFilters.length > 0) {
      result = result.filter(story =>
        story.themes?.some(t => themeFilters.includes(t))
      )
    }

    // Online only filter
    if (onlineOnly) {
      result = result.filter(story => story.read_url)
    }

    // Search filter
    const q = searchQuery.trim().toLowerCase()
    if (q) {
      result = result.filter(story =>
        story.title.toLowerCase().includes(q) ||
        story.author.toLowerCase().includes(q) ||
        story.themes?.some(t => t.toLowerCase().includes(q)) ||
        story.collection?.toLowerCase().includes(q)
      )
    }

    return result
  }, [awardsFilters, genreFilters, themeFilters, onlineOnly, searchQuery])

  const hasActiveFilters = awardsFilters.length > 0 || genreFilters.length > 0 || themeFilters.length > 0 || onlineOnly || searchQuery.trim() !== ''

  const clearAllFilters = () => {
    setAwardsFilters([])
    setGenreFilters([])
    setThemeFilters([])
    setOnlineOnly(false)
    setSearchQueryState('')
    setSearchParams({})
  }

  return (
    <div className="stories-catalog">
      {showTitle && (
        <header className="stories-catalog__header">
          <h1 className="stories-catalog__title">A Night To Remember</h1>
          <p className="stories-catalog__subtitle">Essential Short Stories</p>
        </header>
      )}
      
      <div className="stories-catalog__controls">
        <div className="stories-catalog__filters">
          <FilterDropdown
            label="Awards"
            options={recognitionTypes}
            selected={awardsFilters}
            onChange={setAwardsFilters}
            counts={awardsCounts}
          />
          <FilterDropdown
            label="Genre"
            options={allGenres}
            selected={genreFilters}
            onChange={setGenreFilters}
            counts={genreCounts}
          />
          <FilterDropdown
            label="Theme"
            options={allThemes}
            selected={themeFilters}
            onChange={setThemeFilters}
            counts={themeCounts}
          />
          <button
            type="button"
            className={`stories-catalog__online-toggle ${onlineOnly ? 'stories-catalog__online-toggle--active' : ''}`}
            onClick={() => setOnlineOnly(!onlineOnly)}
          >
            Free Online
          </button>
          {hasActiveFilters && (
            <button
              type="button"
              className="stories-catalog__clear-all"
              onClick={clearAllFilters}
            >
              Clear All
            </button>
          )}
        </div>
        <div className="stories-catalog__search">
          <SearchInput 
            value={searchQuery}
            onChange={setSearchQuery}
            placeholder="Search stories, authors, themes..."
          />
        </div>
      </div>

      <div className="stories-catalog__grid">
        {filteredStories.map(story => (
          <StoryCard key={story.id} story={story} />
        ))}
      </div>

      {filteredStories.length === 0 && hasActiveFilters && (
        <div className="stories-catalog__empty">
          <p>No stories match your current filters.</p>
          <button type="button" onClick={clearAllFilters} className="stories-catalog__clear-button">
            Clear all filters
          </button>
        </div>
      )}
    </div>
  )
}

export default StoriesCatalog
