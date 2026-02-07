# Art-House Movie Catalog

A curated catalog of award-winning art-house films from major international film festivals and critics' picks.

## Features

- Browse films from Cannes, Berlin, Venice, Tokyo, Hong Kong, Busan, Sundance, Toronto, and Annecy
- Filter by awards (festivals & critics' picks), streaming service, country, decade, genre, and rating
- Multi-region streaming availability (US, UK, CA, AU, DE, FR, IT, ES, JP, KR)
- Auto-detects user's country for streaming info
- Search by title, director, or cast
- View detailed movie information with TMDB data
- Builds to a single HTML file for easy sharing

## Quick Start

```bash
# Install dependencies
just install

# Start dev server
just dev

# Build everything (data + web)
just all
```

## Commands

Run `just` to see all commands grouped by category.

### Web Development

| Command | Description | Underlying |
|---------|-------------|------------|
| `just dev` | Start development server | `npm run dev` |
| `just build` | Build for production (single HTML) | `npm run build` |
| `just preview` | Preview production build locally | `npm run preview` |

### Testing & Quality

| Command | Description | Underlying |
|---------|-------------|------------|
| `just test` | Run tests once | `npm test -- --run` |
| `just test-watch` | Run tests in watch mode | `npm test` |
| `just lint` | Run linter | `npm run lint` |
| `just check` | Run all checks | lint + test + build |

### Data Pipeline

| Command | Description | Underlying |
|---------|-------------|------------|
| `just data-build` | Full pipeline: fetch → enrich → export | `uv run python pipeline.py` |
| `just data-fetch` | Quick fetch (no TMDB enrichment) | `uv run python pipeline.py --skip-enrich` |
| `just data-test N` | Test with N movies (default: 10) | `uv run python pipeline.py --limit N` |
| `just data-install` | Install pipeline dependencies | `uv sync` |

### Full Workflows

| Command | Description |
|---------|-------------|
| `just all` | Rebuild everything: data pipeline + web build |
| `just quick` | Quick rebuild: fetch (no enrich) + web build |

### Setup & Maintenance

| Command | Description | Underlying |
|---------|-------------|------------|
| `just install` | Install all dependencies | `npm install` + `uv sync` |
| `just clean` | Clean build artifacts | removes dist/ |
| `just rebuild` | Full rebuild | clean + install + build |

## Data Sources

### Festivals
- Cannes (Palme d'Or, Grand Prix, Best Director, Jury Prize)
- Berlin (Golden Bear)
- Venice (Golden Lion)
- Toronto (People's Choice)
- Sundance (Grand Jury Prize, World Cinema Prize)
- Tokyo (Grand Prix)
- Busan (New Currents)
- Hong Kong (Best Film)
- Annecy (Cristal d'Or - animation)

### Critics' Picks
- Sight & Sound Top 10 (UK)
- Film Comment Top 10 (US)
- Indiewire Critics Poll (US)
- Cinema Scope Top 10 (Canada)
- Cahiers du Cinéma Top 10 (France)
- Kinema Junpo Best Foreign Film (Japan)
- German Film Critics (Germany)
- Fotogramas (Spain)
- Korean Film Critics KAFCA (Korea)

### Directors
- 50+ acclaimed art-house directors including animation masters

## Environment Setup

Create `data-pipeline/.env`:

```
TMDB_API_KEY=your_api_key_here
```

Get a free API key at [themoviedb.org](https://www.themoviedb.org/settings/api).

## Tech Stack

- React + TypeScript + Vite
- vite-plugin-singlefile (single HTML output)
- Python + uv (data pipeline)
- TMDB API (movie metadata & streaming)
- Wikidata SPARQL (festival winners)
