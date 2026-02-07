export interface StoryRecognition {
  type: string;
  year: number;
  details?: string;
}

export interface Story {
  id: string;
  title: string;
  author: string;
  year: number;
  country?: string;
  collection?: string;
  genres?: string[];
  themes?: string[];
  recognitions?: StoryRecognition[];
  read_url?: string;
  source?: string;
  buy_url?: string;
}
