"""Classic short stories - literary and sci-fi essentials."""

# Literary Fiction Classics
LITERARY_CLASSICS = [
    # Chekhov
    {"title": "The Lady with the Dog", "author": "Anton Chekhov", "year": 1899, "country": "Russia"},
    {"title": "The Bet", "author": "Anton Chekhov", "year": 1889, "country": "Russia"},
    {"title": "Ward No. 6", "author": "Anton Chekhov", "year": 1892, "country": "Russia"},
    
    # Kafka
    {"title": "The Metamorphosis", "author": "Franz Kafka", "year": 1915, "country": "Czech Republic"},
    {"title": "A Hunger Artist", "author": "Franz Kafka", "year": 1922, "country": "Czech Republic"},
    {"title": "In the Penal Colony", "author": "Franz Kafka", "year": 1919, "country": "Czech Republic"},
    
    # Joyce
    {"title": "The Dead", "author": "James Joyce", "year": 1914, "country": "Ireland", "collection": "Dubliners"},
    {"title": "Araby", "author": "James Joyce", "year": 1914, "country": "Ireland", "collection": "Dubliners"},
    {"title": "Eveline", "author": "James Joyce", "year": 1914, "country": "Ireland", "collection": "Dubliners"},
    
    # Hemingway
    {"title": "Hills Like White Elephants", "author": "Ernest Hemingway", "year": 1927, "country": "USA"},
    {"title": "A Clean, Well-Lighted Place", "author": "Ernest Hemingway", "year": 1933, "country": "USA"},
    {"title": "The Snows of Kilimanjaro", "author": "Ernest Hemingway", "year": 1936, "country": "USA"},
    
    # Carver
    {"title": "What We Talk About When We Talk About Love", "author": "Raymond Carver", "year": 1981, "country": "USA"},
    {"title": "Cathedral", "author": "Raymond Carver", "year": 1983, "country": "USA"},
    {"title": "A Small, Good Thing", "author": "Raymond Carver", "year": 1983, "country": "USA"},
    
    # Salinger
    {"title": "A Perfect Day for Bananafish", "author": "J.D. Salinger", "year": 1948, "country": "USA", "collection": "Nine Stories"},
    {"title": "For Esmé—with Love and Squalor", "author": "J.D. Salinger", "year": 1950, "country": "USA", "collection": "Nine Stories"},
    
    # Poe
    {"title": "The Tell-Tale Heart", "author": "Edgar Allan Poe", "year": 1843, "country": "USA"},
    {"title": "The Fall of the House of Usher", "author": "Edgar Allan Poe", "year": 1839, "country": "USA"},
    {"title": "The Cask of Amontillado", "author": "Edgar Allan Poe", "year": 1846, "country": "USA"},
    
    # Tolstoy
    {"title": "The Death of Ivan Ilyich", "author": "Leo Tolstoy", "year": 1886, "country": "Russia"},
    {"title": "Master and Man", "author": "Leo Tolstoy", "year": 1895, "country": "Russia"},
    
    # Maupassant
    {"title": "The Necklace", "author": "Guy de Maupassant", "year": 1884, "country": "France"},
    {"title": "Boule de Suif", "author": "Guy de Maupassant", "year": 1880, "country": "France"},
]

# Science Fiction Classics - Philosophy in disguise
SCIFI_CLASSICS = [
    # Ted Chiang - the master
    {"title": "Story of Your Life", "author": "Ted Chiang", "year": 1998, "country": "USA", "collection": "Stories of Your Life and Others", "themes": ["linguistics", "determinism", "time"]},
    {"title": "Exhalation", "author": "Ted Chiang", "year": 2008, "country": "USA", "collection": "Exhalation: Stories", "themes": ["entropy", "consciousness"]},
    {"title": "The Lifecycle of Software Objects", "author": "Ted Chiang", "year": 2010, "country": "USA", "themes": ["AI", "consciousness", "parenting"]},
    {"title": "Tower of Babylon", "author": "Ted Chiang", "year": 1990, "country": "USA", "themes": ["cosmology", "faith"]},
    {"title": "Hell Is the Absence of God", "author": "Ted Chiang", "year": 2001, "country": "USA", "themes": ["theodicy", "faith"]},
    {"title": "Understand", "author": "Ted Chiang", "year": 1991, "country": "USA", "themes": ["intelligence", "consciousness"]},
    {"title": "Anxiety Is the Dizziness of Freedom", "author": "Ted Chiang", "year": 2019, "country": "USA", "themes": ["free will", "parallel universes"]},
    
    # Philip K. Dick
    {"title": "The Minority Report", "author": "Philip K. Dick", "year": 1956, "country": "USA", "themes": ["free will", "precognition"]},
    {"title": "We Can Remember It for You Wholesale", "author": "Philip K. Dick", "year": 1966, "country": "USA", "themes": ["memory", "identity"]},
    {"title": "The Electric Ant", "author": "Philip K. Dick", "year": 1969, "country": "USA", "themes": ["reality", "consciousness"]},
    
    # Asimov
    {"title": "The Last Question", "author": "Isaac Asimov", "year": 1956, "country": "USA", "themes": ["entropy", "cosmology", "AI"]},
    {"title": "Nightfall", "author": "Isaac Asimov", "year": 1941, "country": "USA", "themes": ["civilization", "psychology"]},
    {"title": "The Bicentennial Man", "author": "Isaac Asimov", "year": 1976, "country": "USA", "themes": ["AI", "humanity"]},
    
    # Le Guin
    {"title": "The Ones Who Walk Away from Omelas", "author": "Ursula K. Le Guin", "year": 1973, "country": "USA", "themes": ["ethics", "utilitarianism"]},
    {"title": "The Day Before the Revolution", "author": "Ursula K. Le Guin", "year": 1974, "country": "USA", "themes": ["anarchism", "revolution"]},
    
    # Bradbury
    {"title": "A Sound of Thunder", "author": "Ray Bradbury", "year": 1952, "country": "USA", "themes": ["time travel", "butterfly effect"]},
    {"title": "There Will Come Soft Rains", "author": "Ray Bradbury", "year": 1950, "country": "USA", "themes": ["nuclear war", "automation"]},
    {"title": "The Veldt", "author": "Ray Bradbury", "year": 1950, "country": "USA", "themes": ["technology", "parenting"]},
    
    # Clarke
    {"title": "The Nine Billion Names of God", "author": "Arthur C. Clarke", "year": 1953, "country": "UK", "themes": ["religion", "technology"]},
    {"title": "The Star", "author": "Arthur C. Clarke", "year": 1955, "country": "UK", "themes": ["faith", "theodicy"]},
]


def fetch_literary_classics() -> list[dict]:
    """Return classic literary short stories."""
    print("Fetching Literary Classics...")
    stories = []
    for item in LITERARY_CLASSICS:
        stories.append({
            "title": item["title"],
            "author": item["author"],
            "year": item["year"],
            "country": item.get("country", ""),
            "collection": item.get("collection"),
            "genres": ["Literary Fiction"],
            "recognitions": [{"type": "Literary Classic", "year": item["year"], "details": "Essential"}],
        })
    print(f"  Found {len(stories)} stories")
    return stories


def fetch_scifi_classics() -> list[dict]:
    """Return classic science fiction short stories."""
    print("Fetching Sci-Fi Classics...")
    stories = []
    for item in SCIFI_CLASSICS:
        stories.append({
            "title": item["title"],
            "author": item["author"],
            "year": item["year"],
            "country": item.get("country", ""),
            "collection": item.get("collection"),
            "genres": ["Science Fiction"],
            "themes": item.get("themes", []),
            "recognitions": [{"type": "Sci-Fi Classic", "year": item["year"], "details": "Essential"}],
        })
    print(f"  Found {len(stories)} stories")
    return stories
