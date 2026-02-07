"""Stories available to read online for free."""

# Stories with free online access (New Yorker, Tor.com, Clarkesworld, etc.)
ONLINE_STORIES = [
    # Recent acclaimed stories (2024-2025)
    {
        "title": "The Year Without Sunshine",
        "author": "Naomi Kritzer",
        "year": 2024,
        "url": "https://uncannymagazine.com/article/the-year-without-sunshine/",
        "source": "Uncanny Magazine",
        "themes": ["climate", "community", "survival"],
    },
    {
        "title": "How to Raise a Kraken in Your Bathtub",
        "author": "P. Djèlí Clark",
        "year": 2023,
        "url": "https://uncannymagazine.com/article/how-to-raise-a-kraken-in-your-bathtub/",
        "source": "Uncanny Magazine",
        "themes": ["mythology", "family", "responsibility"],
    },
    {
        "title": "Better Living Through Algorithms",
        "author": "Naomi Kritzer",
        "year": 2022,
        "url": "https://clarkesworldmagazine.com/kritzer_05_22/",
        "source": "Clarkesworld",
        "themes": ["AI", "dating", "technology"],
    },
    {
        "title": "Rabbit Test",
        "author": "Samantha Shannon",
        "year": 2022,
        "url": "https://uncannymagazine.com/article/rabbit-test/",
        "source": "Uncanny Magazine",
        "themes": ["reproductive rights", "dystopia", "resistance"],
    },
    # New Yorker (many classics available)
    {
        "title": "Cat Person",
        "author": "Kristen Roupenian",
        "year": 2017,
        "url": "https://www.newyorker.com/magazine/2017/12/11/cat-person",
        "source": "The New Yorker",
        "themes": ["dating", "gender", "communication"],
    },
    {
        "title": "The Lottery",
        "author": "Shirley Jackson",
        "year": 1948,
        "url": "https://www.newyorker.com/magazine/1948/06/26/the-lottery",
        "source": "The New Yorker",
        "themes": ["tradition", "violence", "conformity"],
    },
    
    # Tor.com (free sci-fi/fantasy)
    {
        "title": "The Paper Menagerie",
        "author": "Ken Liu",
        "year": 2011,
        "url": "https://io9.gizmodo.com/read-ken-lius-amazing-story-that-swept-the-hugo-} nebula-5958919",
        "source": "io9",
        "themes": ["immigration", "family", "magic"],
    },
    {
        "title": "Exhalation",
        "author": "Ted Chiang",
        "year": 2008,
        "url": "https://www.lightspeedmagazine.com/fiction/exhalation/",
        "source": "Lightspeed Magazine",
        "themes": ["entropy", "consciousness", "mortality"],
    },
    {
        "title": "Cat Pictures Please",
        "author": "Naomi Kritzer",
        "year": 2015,
        "url": "https://clarkesworldmagazine.com/kritzer_01_15/",
        "source": "Clarkesworld",
        "themes": ["AI", "ethics", "cats"],
    },
    
    # Clarkesworld Magazine
    {
        "title": "The Water That Falls on You from Nowhere",
        "author": "John Chu",
        "year": 2013,
        "url": "https://www.tor.com/2013/02/20/the-water-that-falls-on-you-from-nowhere/",
        "source": "Tor.com",
        "themes": ["family", "truth", "coming out"],
    },
    {
        "title": "Welcome to Your Authentic Indian Experience™",
        "author": "Rebecca Roanhorse",
        "year": 2017,
        "url": "https://www.apex-magazine.com/short-fiction/welcome-to-your-authentic-indian-experience/",
        "source": "Apex Magazine",
        "themes": ["identity", "colonialism", "VR"],
    },
    
    # Granta
    {
        "title": "Barn Burning",
        "author": "Haruki Murakami",
        "year": 1983,
        "url": "https://granta.com/barn-burning/",
        "source": "Granta",
        "themes": ["class", "mystery", "obsession"],
    },
    
    # Project Gutenberg (public domain classics)
    {
        "title": "The Metamorphosis",
        "author": "Franz Kafka",
        "year": 1915,
        "url": "https://www.gutenberg.org/ebooks/5200",
        "source": "Project Gutenberg",
        "themes": ["alienation", "family", "transformation"],
    },
    {
        "title": "The Tell-Tale Heart",
        "author": "Edgar Allan Poe",
        "year": 1843,
        "url": "https://www.gutenberg.org/ebooks/2148",
        "source": "Project Gutenberg",
        "themes": ["guilt", "madness", "murder"],
    },
    {
        "title": "The Yellow Wallpaper",
        "author": "Charlotte Perkins Gilman",
        "year": 1892,
        "url": "https://www.gutenberg.org/ebooks/1952",
        "source": "Project Gutenberg",
        "themes": ["mental health", "feminism", "confinement"],
    },
    {
        "title": "An Occurrence at Owl Creek Bridge",
        "author": "Ambrose Bierce",
        "year": 1890,
        "url": "https://www.gutenberg.org/ebooks/375",
        "source": "Project Gutenberg",
        "themes": ["war", "death", "perception"],
    },
    {
        "title": "The Lady with the Dog",
        "author": "Anton Chekhov",
        "year": 1899,
        "url": "https://www.gutenberg.org/ebooks/13415",
        "source": "Project Gutenberg",
        "themes": ["love", "adultery", "ennui"],
    },
]


def fetch_online_stories() -> list[dict]:
    """Return stories available to read online for free."""
    print("Fetching Online Stories...")
    stories = []
    for item in ONLINE_STORIES:
        stories.append({
            "title": item["title"],
            "author": item["author"],
            "year": item["year"],
            "read_url": item["url"],
            "source": item["source"],
            "genres": ["Literary Fiction"] if item["source"] in ["The New Yorker", "Granta", "Project Gutenberg"] else ["Science Fiction"],
            "themes": item.get("themes", []),
            "recognitions": [{"type": "Free Online", "year": item["year"], "details": item["source"]}],
        })
    print(f"  Found {len(stories)} stories")
    return stories
