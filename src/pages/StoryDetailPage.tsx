import { useParams, Navigate } from 'react-router-dom'
import { StoryDetail } from '../components/StoryDetail'
import type { Story } from '../types/story'
import storiesData from '../data/stories.json'
import './StoryDetailPage.css'

const stories = (storiesData as { stories: Story[] }).stories

/**
 * StoryDetailPage - displays full details for a single story.
 */
export function StoryDetailPage() {
  const { id } = useParams<{ id: string }>()
  
  const story = stories.find(s => s.id === id)
  
  if (!story) {
    return <Navigate to="/stories" replace />
  }
  
  return (
    <div className="story-detail-page">
      <StoryDetail story={story} />
    </div>
  )
}

export default StoryDetailPage
