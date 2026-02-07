import { Link } from 'react-router-dom'
import type { Story } from '../types/story'
import './StoryCard.css'

interface StoryCardProps {
  story: Story;
}

export function StoryCard({ story }: StoryCardProps) {
  return (
    <Link to={`/stories/${story.id}`} className="story-card">
      <div className="story-card__content">
        <h3 className="story-card__title">{story.title}</h3>
        <p className="story-card__author">{story.author}</p>
        <p className="story-card__year">{story.year}</p>
        {story.collection && (
          <p className="story-card__collection">from "{story.collection}"</p>
        )}
        {story.genres && story.genres.length > 0 && (
          <div className="story-card__genres">
            {story.genres.slice(0, 2).map(g => (
              <span key={g} className="story-card__genre">{g}</span>
            ))}
          </div>
        )}
        {story.themes && story.themes.length > 0 && (
          <div className="story-card__themes">
            {story.themes.slice(0, 3).map(t => (
              <span key={t} className="story-card__theme">{t}</span>
            ))}
          </div>
        )}
        <div className="story-card__footer">
          {story.read_url && (
            <span className="story-card__online" title="Read online free">Free</span>
          )}
          {story.country && (
            <span className="story-card__country">{story.country}</span>
          )}
        </div>
      </div>
    </Link>
  )
}
