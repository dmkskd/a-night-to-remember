import { Link } from 'react-router-dom'
import type { Album } from '../types/album'
import './AlbumCard.css'

interface AlbumCardProps {
  album: Album;
}

export function AlbumCard({ album }: AlbumCardProps) {
  return (
    <Link to={`/music/${album.id}`} className="album-card">
      <div className="album-card__cover">
        {album.cover_url ? (
          <img 
            src={album.cover_url} 
            alt={`${album.title} by ${album.artist}`}
            loading="lazy"
          />
        ) : (
          <div className="album-card__placeholder">
            <span className="album-card__placeholder-text">No Cover</span>
          </div>
        )}
      </div>
      <div className="album-card__info">
        <div className="album-card__title-row">
          <h3 className="album-card__title">{album.title}</h3>
          {album.rating && (
            <span className="album-card__rating">
              <span className="album-card__rating-star">★</span>
              {album.rating.toFixed(1)}
            </span>
          )}
        </div>
        <p className="album-card__artist">{album.artist}</p>
        <p className="album-card__year">{album.year}</p>
        {album.genres && album.genres.length > 0 && (
          <div className="album-card__genres">
            {album.genres.slice(0, 2).map(g => (
              <span key={g} className="album-card__genre">{g}</span>
            ))}
          </div>
        )}
        {album.spotify_url && (
          <div className="album-card__streaming">
            <span className="album-card__spotify" title="Available on Spotify">🎧</span>
          </div>
        )}
      </div>
    </Link>
  )
}
