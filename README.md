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

The `just` commands are pass-through wrappers - all arguments are forwarded directly to the Python pipelines.

#### Command Equivalents

| just | uv (direct) |
|------|-------------|
| `just movies` | `cd data-pipeline/movies && uv run python pipeline.py` |
| `just movies --force` | `cd data-pipeline/movies && uv run python pipeline.py --force` |
| `just movies --limit 10` | `cd data-pipeline/movies && uv run python pipeline.py --limit 10` |
| `just music` | `cd data-pipeline && uv run python -m music.pipeline` |
| `just music --force-refresh` | `cd data-pipeline && uv run python -m music.pipeline --force-refresh` |
| `just stories` | `cd data-pipeline && uv run python -m stories.pipeline` |
| `just stories --dry-run` | `cd data-pipeline && uv run python -m stories.pipeline --dry-run` |
| `just data-install` | `cd data-pipeline && uv sync` |

#### Pipeline CLI Options

**Movies** (`just movies [OPTIONS]`):
| Option | Description |
|--------|-------------|
| `--skip-enrich` | Skip TMDB API enrichment (faster) |
| `--force` | Ignore cache, re-fetch all from TMDB |
| `--dry-run` | Output to test file instead of `src/data/movies.json` |
| `--limit N` | Process only N movies |
| `--min-year YYYY` | Minimum year filter (default: 2000) |

**Music** (`just music [OPTIONS]`):
| Option | Description |
|--------|-------------|
| `--skip-enrich` | Skip Spotify API enrichment |
| `--force-refresh` | Ignore cache, re-fetch all from Spotify |
| `--dry-run` | Output to test file instead of `src/data/albums.json` |
| `--limit N` | Process only N albums |

**Stories** (`just stories [OPTIONS]`):
| Option | Description |
|--------|-------------|
| `--dry-run` | Output to test file instead of `src/data/stories.json` |
| `--limit N` | Process only N stories |

#### Caching

- **Movies**: TMDB cache in `data-pipeline/movies/enrichers/` — bypass with `--force`
- **Music**: Spotify cache in `data-pipeline/music/.spotify_cache.json` — bypass with `--force-refresh`
- **Stories**: No external API, no cache

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
