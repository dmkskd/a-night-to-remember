import { Link, useNavigate } from 'react-router-dom'
import type { Story } from '../types/story'
import './StoryDetail.css'

interface StoryDetailProps {
  story: Story;
}

export function StoryDetail({ story }: StoryDetailProps) {
  const navigate = useNavigate()

  return (
    <div className="story-detail">
      <button className="story-detail__back" onClick={() => navigate('/stories')}>
        ← Back to catalog
      </button>

      <div className="story-detail__header">
        <div className="story-detail__main-info">
          <h1 className="story-detail__title">{story.title}</h1>
          <p className="story-detail__author">
            by <Link to={`/stories?q=${encodeURIComponent(story.author)}`} className="story-detail__link">{story.author}</Link>
          </p>
          <p className="story-detail__year">{story.year}</p>
          {story.country && (
            <p className="story-detail__country">{story.country}</p>
          )}
          {story.collection && (
            <p className="story-detail__collection">from "{story.collection}"</p>
          )}
        </div>
      </div>

      <div className="story-detail__body">
        {story.genres && story.genres.length > 0 && (
          <section className="story-detail__section">
            <h2 className="story-detail__section-title">Genres</h2>
            <div className="story-detail__genres">
              {story.genres.map(genre => (
                <Link
                  key={genre}
                  to={`/stories?genre=${encodeURIComponent(genre)}`}
                  className="story-detail__genre"
                >
                  {genre}
                </Link>
              ))}
            </div>
          </section>
        )}

        {story.recognitions && story.recognitions.length > 0 && (
          <section className="story-detail__section">
            <h2 className="story-detail__section-title">Recognitions</h2>
            <ul className="story-detail__recognitions">
              {story.recognitions.map((rec, i) => (
                <li key={i} className="story-detail__recognition">
                  <span className="story-detail__recognition-type">{rec.type}</span>
                  {rec.details && (
                    <span className="story-detail__recognition-details"> — {rec.details}</span>
                  )}
                  <span className="story-detail__recognition-year"> ({rec.year})</span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {story.themes && story.themes.length > 0 && (
          <section className="story-detail__section">
            <h2 className="story-detail__section-title">Themes</h2>
            <div className="story-detail__themes">
              {story.themes.map(theme => (
                <span key={theme} className="story-detail__theme">{theme}</span>
              ))}
            </div>
          </section>
        )}

        <section className="story-detail__section">
          <h2 className="story-detail__section-title">Read</h2>
          <div className="story-detail__links">
            {story.read_url && (
              <a
                href={story.read_url}
                target="_blank"
                rel="noopener noreferrer"
                className="story-detail__read-link story-detail__read-link--primary"
              >
                Read Free Online {story.source && `(${story.source})`}
              </a>
            )}
            {story.collection && (
              <a
                href={`https://www.amazon.com/s?k=${encodeURIComponent(story.collection + ' ' + story.author)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="story-detail__read-link"
              >
                Find Collection on Amazon
              </a>
            )}
            <a
              href={`https://www.goodreads.com/search?q=${encodeURIComponent(story.title + ' ' + story.author)}`}
              target="_blank"
              rel="noopener noreferrer"
              className="story-detail__read-link"
            >
              View on Goodreads
            </a>
          </div>
        </section>
      </div>
    </div>
  )
}
