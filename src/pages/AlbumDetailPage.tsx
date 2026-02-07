import { Link, useParams } from 'react-router-dom';
import { AlbumDetail } from '../components/AlbumDetail';
import type { Album } from '../types/album';
import albumsData from '../data/albums.json';
import './AlbumDetailPage.css';

const albums = (albumsData as { albums: Album[] }).albums;

/**
 * AlbumDetailPage component.
 * Page component that displays detailed information about a single album.
 */
export function AlbumDetailPage() {
  const { id } = useParams<{ id: string }>();
  
  const album = albums.find(a => a.id === id);

  if (!album) {
    return (
      <div className="album-detail-page">
        <div className="album-detail-page__not-found">
          <h2>Album Not Found</h2>
          <p>The album you're looking for doesn't exist or has been removed.</p>
          <Link to="/music" className="album-detail-page__back-link">
            ← Back to catalog
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="album-detail-page">
      <nav className="album-detail-page__nav">
        <Link to="/music" className="album-detail-page__back-link">
          ← Back to catalog
        </Link>
      </nav>
      <main className="album-detail-page__content">
        <AlbumDetail album={album} allAlbums={albums} />
      </main>
    </div>
  );
}

export default AlbumDetailPage;
