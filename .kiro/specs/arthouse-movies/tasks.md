# Implementation Plan: Art-House Movie Recommendations MVP

## Overview

This plan implements a React/TypeScript single-page application for browsing curated art-house movies. The implementation follows a bottom-up approach: data models first, then hooks, then UI components, and finally wiring everything together with routing.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Initialize React project with TypeScript using Vite
  - Install dependencies: react-router-dom
  - Create folder structure: src/components, src/hooks, src/types, src/data
  - _Requirements: 1.4, 6.1_

- [ ] 2. Define data models and create sample data
  - [x] 2.1 Create TypeScript interfaces for Movie and Recognition
    - Define Movie interface with required and optional fields
    - Define Recognition interface with type, year, and optional details
    - Export types from src/types/movie.ts
    - _Requirements: 6.1, 6.2, 6.4_
  
  - [x] 2.2 Create sample movies.json with curated art-house films
    - Include 10-15 sample movies from Cannes winners and Cahiers du Cinéma lists
    - Populate all fields including recognitions and tags
    - Place in src/data/movies.json
    - _Requirements: 1.4, 6.3_

- [ ] 3. Implement custom hooks for data access
  - [x] 3.1 Implement useMovies hook
    - Load movies from static JSON file
    - Return movies array, isLoading, and error states
    - _Requirements: 1.1, 1.4_
  
  - [x] 3.2 Implement useMovie hook
    - Accept movie ID parameter
    - Return single movie or null if not found
    - _Requirements: 2.1_
  
  - [x] 3.3 Implement useFilteredMovies hook
    - Accept movies array, filters array, and search query
    - Return filtered movies based on recognition type and title/director search
    - _Requirements: 3.1, 4.1_

- [x] 4. Checkpoint - Verify data layer works
  - Ensure hooks load and filter data correctly, ask the user if questions arise.

- [ ] 5. Implement UI components
  - [x] 5.1 Create MovieCard component
    - Display poster, title, director, year
    - Make entire card clickable for navigation
    - Handle missing poster with placeholder
    - _Requirements: 1.2_
  
  - [x] 5.2 Create MovieGrid component
    - Render grid of MovieCard components
    - Implement responsive layout (CSS Grid)
    - _Requirements: 5.1, 5.2_
  
  - [x] 5.3 Create FilterBar component
    - Display available recognition types as filter buttons
    - Support multi-select filtering
    - Include clear filters button
    - _Requirements: 3.1, 3.2_
  
  - [x] 5.4 Create SearchInput component
    - Text input for search queries
    - Clear button when query is not empty
    - _Requirements: 4.1, 4.2_
  
  - [x] 5.5 Create MovieDetail component
    - Display all movie information
    - Show recognitions list
    - Show genre and thematic tags
    - Handle missing optional fields gracefully
    - _Requirements: 2.2, 2.3, 2.4, 2.5_

- [x] 6. Checkpoint - Verify components render correctly
  - Ensure components display properly, ask the user if questions arise.

- [ ] 7. Create page components and routing
  - [x] 7.1 Create MovieCatalog page
    - Compose FilterBar, SearchInput, and MovieGrid
    - Wire up filter and search state
    - Display empty state message when no movies match
    - _Requirements: 1.1, 1.3, 3.3, 4.3_
  
  - [x] 7.2 Create MovieDetailPage
    - Get movie ID from route params
    - Display MovieDetail component
    - Show not found message for invalid IDs
    - _Requirements: 2.1_
  
  - [x] 7.3 Set up React Router
    - Configure routes: / for catalog, /movie/:id for detail
    - Add navigation between pages
    - _Requirements: 2.1_

- [ ] 8. Add styling and responsive layout
  - [x] 8.1 Create global styles and CSS variables
    - Define color palette suitable for art-house aesthetic
    - Set up typography
    - _Requirements: 5.1, 5.2_
  
  - [x] 8.2 Implement responsive grid layout
    - Multi-column on desktop (3-4 columns)
    - Single column on mobile
    - Use CSS Grid with media queries
    - _Requirements: 5.1, 5.2, 5.3_

- [ ] 9. Final integration
  - [x] 9.1 Wire App component with routing
    - Import and configure all routes
    - Add header/navigation component
    - _Requirements: 1.1, 2.1_

- [x] 10. Final checkpoint
  - Verify the application runs correctly, ask the user if questions arise.

## Notes

- Sample movie data should include real art-house films for authenticity
- Poster images can use TMDB image URLs or placeholder images initially
- The data curation scripts (Requirement 7) are not included in this plan as they are optional tooling
