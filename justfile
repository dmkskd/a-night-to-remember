# Art-House Movies - Development Commands
# Run `just` to see all available commands

# Default recipe: show available commands
default:
    @just --list

# ─────────────────────────────────────────────────────────────────
# WEB DEVELOPMENT
# ─────────────────────────────────────────────────────────────────

# Start development server (npm run dev)
[group('web')]
dev:
    npm run dev

# Build for production - single HTML file (npm run build)
[group('web')]
build:
    npm run build

# Preview production build locally (npm run preview)
[group('web')]
preview:
    npm run preview

# ─────────────────────────────────────────────────────────────────
# TESTING & QUALITY
# ─────────────────────────────────────────────────────────────────

# Run tests once (npm test -- --run)
[group('test')]
test:
    npm test -- --run

# Run tests in watch mode (npm test)
[group('test')]
test-watch:
    npm test

# Run linter (npm run lint)
[group('test')]
lint:
    npm run lint

# Run all checks: lint + test + build
[group('test')]
check: lint test build

# ─────────────────────────────────────────────────────────────────
# DATA PIPELINE - MOVIES
# ─────────────────────────────────────────────────────────────────

# Run full movies pipeline: fetch → enrich → export (uv run python pipeline.py)
[group('data')]
movies-build:
    cd data-pipeline/movies && uv run python pipeline.py

# Run movies pipeline without TMDB enrichment - faster (uv run python pipeline.py --skip-enrich)
[group('data')]
movies-fetch:
    cd data-pipeline/movies && uv run python pipeline.py --skip-enrich

# Run movies pipeline with limited movies for testing (uv run python pipeline.py --limit N)
[group('data')]
movies-test limit="10":
    cd data-pipeline/movies && uv run python pipeline.py --limit {{limit}}

# ─────────────────────────────────────────────────────────────────
# DATA PIPELINE - MUSIC
# ─────────────────────────────────────────────────────────────────

# Run full music pipeline: fetch → enrich with Spotify → export (uv run python pipeline.py)
[group('data')]
music-build:
    cd data-pipeline && uv run python -m music.pipeline

# Run music pipeline without Spotify enrichment - faster (uv run python pipeline.py --skip-enrich)
[group('data')]
music-fetch:
    cd data-pipeline && uv run python -m music.pipeline --skip-enrich

# Run music pipeline with limited albums for testing (uv run python pipeline.py --limit N)
[group('data')]
music-test limit="10":
    cd data-pipeline && uv run python -m music.pipeline --limit {{limit}}

# ─────────────────────────────────────────────────────────────────
# DATA PIPELINE - STORIES
# ─────────────────────────────────────────────────────────────────

# Run stories pipeline: fetch → export (uv run python pipeline.py)
[group('data')]
stories-build:
    cd data-pipeline && uv run python -m stories.pipeline

# Run stories pipeline with limited stories for testing
[group('data')]
stories-test limit="10":
    cd data-pipeline && uv run python -m stories.pipeline --limit {{limit}}

# Install data pipeline dependencies (uv sync)
[group('data')]
data-install:
    cd data-pipeline && uv sync

# ─────────────────────────────────────────────────────────────────
# FULL WORKFLOWS
# ─────────────────────────────────────────────────────────────────

# Rebuild everything: movies data + web build
[group('workflow')]
all: movies-build build

# Quick rebuild: fetch movies (no enrich) + web build
[group('workflow')]
quick: movies-fetch build

# ─────────────────────────────────────────────────────────────────
# SETUP & MAINTENANCE
# ─────────────────────────────────────────────────────────────────

# Install all dependencies: frontend + data pipeline (npm install + uv sync)
[group('setup')]
install:
    npm install
    cd data-pipeline && uv sync

# Clean build artifacts
[group('setup')]
clean:
    rm -rf dist node_modules/.vite

# Full rebuild: clean, install, build
[group('setup')]
rebuild: clean install build
