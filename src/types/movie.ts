/**
 * Recognition interface representing awards and festival selections
 * for art-house movies.
 */
export interface Recognition {
  /** Type of recognition (e.g., "Cannes Palme d'Or", "Cahiers du Cinéma Top 10") */
  type: string;
  /** Year the recognition was received */
  year: number;
  /** Additional info (e.g., "Winner", "Nominee") */
  details?: string;
}

/**
 * Streaming provider reference (used in movie data)
 */
export interface StreamingRef {
  /** Provider ID (references providers lookup) */
  id: string;
  /** Type: subscription, rent, or buy */
  type: 'subscription' | 'rent' | 'buy';
}

/**
 * Streaming provider info (in providers lookup)
 */
export interface StreamingProvider {
  /** Provider name (e.g., "Netflix", "MUBI") */
  name: string;
  /** Logo URL */
  logo: string;
}

/**
 * Streaming availability by region
 * Keys are ISO 3166-1 country codes (US, GB, DE, etc.)
 */
export type StreamingByRegion = Record<string, StreamingRef[]>;

/**
 * Providers lookup table
 */
export type ProvidersLookup = Record<string, StreamingProvider>;

/**
 * Review link from a prestigious source
 */
export interface Review {
  /** Source name (e.g., "Sight & Sound", "Cahiers du Cinéma") */
  source: string;
  /** URL to the review */
  url: string;
}

/**
 * Movie interface representing a single movie entry in the catalog.
 * Contains required fields for identification and optional fields
 * for additional metadata.
 */
export interface Movie {
  /** Unique identifier (e.g., "parasite-2019") */
  id: string;
  /** Movie title */
  title: string;
  /** Director name */
  director: string;
  /** Release year */
  year: number;
  /** Plot summary */
  synopsis?: string;
  /** URL to poster image */
  posterUrl?: string;
  /** Country of origin */
  country?: string;
  /** Runtime in minutes */
  runtime?: number;
  /** Main cast members */
  cast?: string[];
  /** Genre classifications */
  genres?: string[];
  /** Awards and selections */
  recognitions: Recognition[];
  /** Thematic labels (e.g., "slow cinema", "existential") */
  tags?: string[];
  /** Streaming availability by region (keyed by country code) */
  streaming?: StreamingByRegion;
  /** Links to reviews from prestigious sources */
  reviews?: Review[];
  /** TMDB rating (0-10 scale) */
  rating?: number;
}
