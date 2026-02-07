export interface AlbumRecognition {
  type: string;
  year: number;
  details?: string;
}

export interface AlbumTrack {
  number: number;
  name: string;
  duration_ms: number;
}

export interface Album {
  id: string;
  title: string;
  artist: string;
  year: number;
  rating?: number;
  cover_url?: string;
  spotify_url?: string;
  spotify_id?: string;
  genres?: string[];  // Broad categories for filtering
  detailed_genres?: string[];  // All genres for detail view
  label?: string;
  recognitions?: AlbumRecognition[];
  tracks?: AlbumTrack[];
}
