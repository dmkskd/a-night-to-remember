import { Link } from 'react-router-dom'
import type { Album } from '../types/album'
import './AlbumDetail.css'

interface AlbumDetailProps {
  album: Album;
  allAlbums?: Album[];
}

const PLACEHOLDER_COVER = 'https://via.placeholder.com/400x400?text=No+Cover';

/**
 * Generate streaming service URLs for an album
 */
function getStreamingServices(artist: string, album: string, spotifyUrl?: string) {
  const query = encodeURIComponent(`${artist} ${album}`);
  
  return [
    {
      name: 'Spotify',
      url: spotifyUrl || `https://open.spotify.com/search/${query}`,
      logo: 'https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Green.png',
      color: '#1DB954',
    },
    {
      name: 'Apple Music',
      url: `https://music.apple.com/search?term=${query}`,
      logo: 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Apple_Music_icon.svg/2048px-Apple_Music_icon.svg.png',
      color: '#FA243C',
    },
    {
      name: 'YouTube Music',
      url: `https://music.youtube.com/search?q=${query}`,
      logo: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Youtube_Music_icon.svg/2048px-Youtube_Music_icon.svg.png',
      color: '#FF0000',
    },
    {
      name: 'Amazon Music',
      url: `https://music.amazon.com/search/${query}`,
      logo: 'https://d5fx445wy2wpk.cloudfront.net/static/logo.svg',
      color: '#00A8E1',
    },
    {
      name: 'Deezer',
      url: `https://www.deezer.com/search/${query}`,
      logo: 'https://e-cdns-files.dzcdn.net/cache/slash/images/common/logos/deezer_light.838bc2c1e7c93809.png',
      color: '#A238FF',
    },
  ];
}

/**
 * Format duration from milliseconds to mm:ss
 */
function formatDuration(ms: number): string {
  const minutes = Math.floor(ms / 60000);
  const seconds = Math.floor((ms % 60000) / 1000);
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

export function AlbumDetail({ album, allAlbums = [] }: AlbumDetailProps) {
  const streamingServices = getStreamingServices(album.artist, album.title, album.spotify_url);
  
  // Find similar albums: same artist first, then same genre
  const similarAlbums = (() => {
    const byArtist = allAlbums.filter(a => a.id !== album.id && a.artist === album.artist);
    const byGenre = allAlbums.filter(a => {
      if (a.id === album.id || a.artist === album.artist) return false;
      return album.genres?.some(g => a.genres?.includes(g));
    });
    return [...byArtist, ...byGenre].slice(0, 6);
  })();

  return (
    <article className="album-detail">
      <div className="album-detail__header">
        <div className="album-detail__cover-container">
          <img
            src={album.cover_url || PLACEHOLDER_COVER}
            alt={`${album.title} by ${album.artist}`}
            className="album-detail__cover"
            onError={(e) => { e.currentTarget.src = PLACEHOLDER_COVER; }}
          />
        </div>
        
        <div className="album-detail__main-info">
          <div className="album-detail__title-row">
            <h1 className="album-detail__title">{album.title}</h1>
            {album.rating && (
              <span className="album-detail__rating">
                <span className="album-detail__rating-star">★</span>
                {album.rating.toFixed(1)}
              </span>
            )}
          </div>
          <p className="album-detail__artist">
            <Link to={`/music?q=${encodeURIComponent(album.artist)}`} className="album-detail__link">
              {album.artist}
            </Link>
          </p>
          <p className="album-detail__year">{album.year}</p>
          
          {album.label && (
            <p className="album-detail__label">{album.label}</p>
          )}
        </div>
      </div>

      <div className="album-detail__body">
        {/* Genres - show broad categories first, then detailed */}
        {((album.genres && album.genres.length > 0) || (album.detailed_genres && album.detailed_genres.length > 0)) && (
          <section className="album-detail__section">
            <h2 className="album-detail__section-title">Genres</h2>
            <div className="album-detail__genres">
              {/* Broad categories first (clickable) */}
              {album.genres?.map(genre => (
                <Link 
                  key={genre} 
                  to={`/music?genre=${encodeURIComponent(genre)}`}
                  className="album-detail__genre album-detail__genre--broad"
                >
                  {genre}
                </Link>
              ))}
              {/* Detailed genres (clickable) */}
              {album.detailed_genres?.filter(g => !album.genres?.includes(g)).map(genre => (
                <Link 
                  key={genre} 
                  to={`/music?genre=${encodeURIComponent(genre)}`}
                  className="album-detail__genre album-detail__genre--detailed"
                >
                  {genre}
                </Link>
              ))}
            </div>
          </section>
        )}

        {/* Recognitions */}
        {album.recognitions && album.recognitions.length > 0 && (
          <section className="album-detail__section">
            <h2 className="album-detail__section-title">Recognitions</h2>
            <ul className="album-detail__recognitions">
              {album.recognitions.map((rec, index) => (
                <li key={index} className="album-detail__recognition">
                  <span className="album-detail__recognition-type">{rec.type}</span>
                  <span className="album-detail__recognition-year">({rec.year})</span>
                  {rec.details && (
                    <span className="album-detail__recognition-details"> — {rec.details}</span>
                  )}
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* Listen On (streaming services) */}
        <section className="album-detail__section">
          <h2 className="album-detail__section-title">Listen On</h2>
          <div className="album-detail__streaming">
            {streamingServices.map(service => (
              <a 
                key={service.name}
                href={service.url} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="album-detail__service"
              >
                <img 
                  src={service.logo} 
                  alt={service.name}
                  className="album-detail__service-logo"
                  onError={(e) => { e.currentTarget.style.display = 'none'; }}
                />
                <span className="album-detail__service-name">{service.name}</span>
              </a>
            ))}
          </div>
        </section>

        {/* Track List */}
        {album.tracks && album.tracks.length > 0 && (
          <section className="album-detail__section">
            <h2 className="album-detail__section-title">Tracks</h2>
            <ol className="album-detail__tracks">
              {album.tracks.map(track => (
                <li key={track.number} className="album-detail__track">
                  <span className="album-detail__track-number">{track.number}</span>
                  <span className="album-detail__track-name">{track.name}</span>
                  <span className="album-detail__track-duration">{formatDuration(track.duration_ms)}</span>
                </li>
              ))}
            </ol>
          </section>
        )}

        {/* Similar Albums */}
        {similarAlbums.length > 0 && (
          <section className="album-detail__section">
            <h2 className="album-detail__section-title">Similar Albums</h2>
            <div className="album-detail__similar">
              {similarAlbums.map(a => (
                <Link key={a.id} to={`/music/${a.id}`} className="album-detail__similar-card">
                  <img
                    src={a.cover_url || PLACEHOLDER_COVER}
                    alt={a.title}
                    className="album-detail__similar-cover"
                    onError={(e) => { e.currentTarget.src = PLACEHOLDER_COVER; }}
                  />
                  <div className="album-detail__similar-info">
                    <div className="album-detail__similar-title-row">
                      <span className="album-detail__similar-title">{a.title}</span>
                      {a.rating && (
                        <span className="album-detail__similar-rating">
                          <span className="album-detail__similar-rating-star">★</span>
                          {a.rating.toFixed(1)}
                        </span>
                      )}
                    </div>
                    <span className="album-detail__similar-meta">{a.artist} • {a.year}</span>
                  </div>
                </Link>
              ))}
            </div>
          </section>
        )}
      </div>
    </article>
  );
}

export default AlbumDetail;
