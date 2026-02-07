import { useState, useMemo, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { AlbumCard } from '../components/AlbumCard'
import { FilterDropdown } from '../components/FilterDropdown'
import { SearchInput } from '../components/SearchInput'
import type { Album } from '../types/album'
import albumsData from '../data/albums.json'
import './MusicCatalog.css'

const albums = (albumsData as { albums: Album[] }).albums
const recognitionTypes = (albumsData as { recognitionTypes: string[] }).recognitionTypes || []

/**
 * MusicCatalog page - browse albums catalog with filters.
 */
export function MusicCatalog({ showTitle = true }: { showTitle?: boolean }) {
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
  const [decadeFilters, setDecadeFilters] = useState<string[]>([])
  const [genreFilters, setGenreFilters] = useState<string[]>(() => {
    const genreParam = searchParams.get('genre')
    return genreParam ? [genreParam] : []
  })
  
  // Sync genre filter from URL
  useEffect(() => {
    const genreParam = searchParams.get('genre')
    if (genreParam && !genreFilters.includes(genreParam)) {
      setGenreFilters([genreParam])
    }
  }, [searchParams])

  // Get available decades
  const availableDecades = useMemo(() => {
    const decades = new Set<string>()
    albums.forEach(album => {
      if (album.year) {
        const decade = `${Math.floor(album.year / 10) * 10}s`
        decades.add(decade)
      }
    })
    return Array.from(decades).sort().reverse()
  }, [])

  // Get available genres (both broad and detailed for filtering)
  const availableGenres = useMemo(() => {
    const genres = new Map<string, number>()
    albums.forEach(album => {
      // Include both broad and detailed genres
      album.genres?.forEach(g => genres.set(g, (genres.get(g) || 0) + 1))
      album.detailed_genres?.forEach(g => genres.set(g, (genres.get(g) || 0) + 1))
    })
    // Sort by count descending, then alphabetically
    return Array.from(genres.entries())
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .map(([genre]) => genre)
  }, [])

  // Compute counts
  const awardsCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    recognitionTypes.forEach(type => {
      counts[type] = albums.filter(album =>
        album.recognitions?.some(r => r.type === type)
      ).length
    })
    return counts
  }, [])

  const decadeCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    availableDecades.forEach(decade => {
      const decadeStart = parseInt(decade)
      counts[decade] = albums.filter(album => {
        if (!album.year) return false
        const albumDecade = Math.floor(album.year / 10) * 10
        return albumDecade === decadeStart
      }).length
    })
    return counts
  }, [availableDecades])

  const genreCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    availableGenres.forEach(genre => {
      counts[genre] = albums.filter(album =>
        album.genres?.includes(genre) || album.detailed_genres?.includes(genre)
      ).length
    })
    return counts
  }, [availableGenres])

  // Filter albums
  const filteredAlbums = useMemo(() => {
    let result = albums

    // Awards filter
    if (awardsFilters.length > 0) {
      result = result.filter(album =>
        album.recognitions?.some(r => awardsFilters.includes(r.type))
      )
    }

    // Decade filter
    if (decadeFilters.length > 0) {
      result = result.filter(album => {
        if (!album.year) return false
        const decade = `${Math.floor(album.year / 10) * 10}s`
        return decadeFilters.includes(decade)
      })
    }

    // Genre filter - check both broad and detailed genres
    if (genreFilters.length > 0) {
      result = result.filter(album =>
        album.genres?.some(g => genreFilters.includes(g)) ||
        album.detailed_genres?.some(g => genreFilters.includes(g))
      )
    }

    // Search filter - also search detailed genres
    const q = searchQuery.trim().toLowerCase()
    if (q) {
      result = result.filter(album =>
        album.title.toLowerCase().includes(q) ||
        album.artist.toLowerCase().includes(q) ||
        album.genres?.some(g => g.toLowerCase().includes(q)) ||
        album.detailed_genres?.some(g => g.toLowerCase().includes(q))
      )
    }

    return result
  }, [awardsFilters, decadeFilters, genreFilters, searchQuery])

  const hasActiveFilters = awardsFilters.length > 0 || decadeFilters.length > 0 || genreFilters.length > 0 || searchQuery.trim() !== ''

  const clearAllFilters = () => {
    setAwardsFilters([])
    setDecadeFilters([])
    setGenreFilters([])
    setSearchQueryState('')
    setSearchParams({})
  }

  return (
    <div className="music-catalog">
      {showTitle && (
        <header className="music-catalog__header">
          <h1 className="music-catalog__title">A Night To Remember</h1>
          <p className="music-catalog__subtitle">Essential Albums</p>
        </header>
      )}
      
      <div className="music-catalog__controls">
        <div className="music-catalog__filters">
          <FilterDropdown
            label="Awards"
            options={recognitionTypes}
            selected={awardsFilters}
            onChange={setAwardsFilters}
            counts={awardsCounts}
          />
          <FilterDropdown
            label="Decade"
            options={availableDecades}
            selected={decadeFilters}
            onChange={setDecadeFilters}
            counts={decadeCounts}
          />
          {availableGenres.length > 0 && (
            <FilterDropdown
              label="Genre"
              options={availableGenres}
              selected={genreFilters}
              onChange={setGenreFilters}
              counts={genreCounts}
            />
          )}
          {hasActiveFilters && (
            <button
              type="button"
              className="music-catalog__clear-all"
              onClick={clearAllFilters}
            >
              Clear All
            </button>
          )}
        </div>
        <div className="music-catalog__search">
          <SearchInput 
            value={searchQuery}
            onChange={setSearchQuery}
            placeholder="Search albums, artists..."
          />
        </div>
      </div>

      <div className="music-catalog__grid">
        {filteredAlbums.map(album => (
          <AlbumCard key={album.id} album={album} />
        ))}
      </div>

      {filteredAlbums.length === 0 && hasActiveFilters && (
        <div className="music-catalog__empty">
          <p>No albums match your current filters.</p>
          <button type="button" onClick={clearAllFilters} className="music-catalog__clear-button">
            Clear all filters
          </button>
        </div>
      )}
    </div>
  )
}

export default MusicCatalog
