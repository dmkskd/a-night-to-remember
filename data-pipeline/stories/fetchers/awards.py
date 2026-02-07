"""Award-winning short stories - Hugo, Nebula, O. Henry, etc."""

# Hugo Award for Best Short Story (Sci-Fi/Fantasy)
HUGO_WINNERS = [
    {"title": "The Year Without Sunshine", "author": "Naomi Kritzer", "year": 2025},
    {"title": "How to Raise a Kraken in Your Bathtub", "author": "P. Djèlí Clark", "year": 2024},
    {"title": "Better Living Through Algorithms", "author": "Naomi Kritzer", "year": 2023},
    {"title": "Exhalation", "author": "Ted Chiang", "year": 2009, "collection": "Exhalation: Stories"},
    {"title": "The Paper Menagerie", "author": "Ken Liu", "year": 2012, "collection": "The Paper Menagerie and Other Stories"},
    {"title": "The Water That Falls on You from Nowhere", "author": "John Chu", "year": 2014},
    {"title": "Cat Pictures Please", "author": "Naomi Kritzer", "year": 2016},
    {"title": "Welcome to Your Authentic Indian Experience™", "author": "Rebecca Roanhorse", "year": 2018},
    {"title": "A Guide for Working Breeds", "author": "Vina Jie-Min Prasad", "year": 2019},
    {"title": "Metal Like Blood in the Dark", "author": "T. Kingfisher", "year": 2021},
    {"title": "The Pill", "author": "Meg Elison", "year": 2022},
    {"title": "Flowers for Algernon", "author": "Daniel Keyes", "year": 1960, "collection": "Flowers for Algernon (novel)"},
    {"title": "I Have No Mouth, and I Must Scream", "author": "Harlan Ellison", "year": 1968, "collection": "I Have No Mouth, and I Must Scream"},
    {"title": "The Ones Who Walk Away from Omelas", "author": "Ursula K. Le Guin", "year": 1974, "collection": "The Wind's Twelve Quarters"},
    {"title": "Jeffty Is Five", "author": "Harlan Ellison", "year": 1978},
    {"title": "Speech Sounds", "author": "Octavia E. Butler", "year": 1984},
    {"title": "Tangents", "author": "Greg Bear", "year": 1987},
    {"title": "Bears Discover Fire", "author": "Terry Bisson", "year": 1991},
]

# Nebula Award for Best Short Story
NEBULA_WINNERS = [
    {"title": "How to Raise a Kraken in Your Bathtub", "author": "P. Djèlí Clark", "year": 2024},
    {"title": "Better Living Through Algorithms", "author": "Naomi Kritzer", "year": 2023},
    {"title": "Story of Your Life", "author": "Ted Chiang", "year": 1999, "collection": "Stories of Your Life and Others"},
    {"title": "The Husband Stitch", "author": "Carmen Maria Machado", "year": 2015, "collection": "Her Body and Other Parties"},
    {"title": "Seasons of Glass and Iron", "author": "Amal El-Mohtar", "year": 2017},
    {"title": "The Secret Lives of the Nine Negro Teeth of George Washington", "author": "P. Djèlí Clark", "year": 2019},
    {"title": "A Guide for Working Breeds", "author": "Vina Jie-Min Prasad", "year": 2020},
    {"title": "Where Oaken Hearts Do Gather", "author": "Sarah Pinsker", "year": 2022},
    {"title": "The Silk Dragon: Translations from a Childhood", "author": "Aliette de Bodard", "year": 2023},
]

# O. Henry Prize (Literary Fiction)
OHENRY_WINNERS = [
    {"title": "The Lottery", "author": "Shirley Jackson", "year": 1949, "collection": "The Lottery and Other Stories"},
    {"title": "A Good Man Is Hard to Find", "author": "Flannery O'Connor", "year": 1955, "collection": "A Good Man Is Hard to Find"},
    {"title": "Everything That Rises Must Converge", "author": "Flannery O'Connor", "year": 1965, "collection": "Everything That Rises Must Converge"},
    {"title": "Where Are You Going, Where Have You Been?", "author": "Joyce Carol Oates", "year": 1967},
    {"title": "Cathedral", "author": "Raymond Carver", "year": 1983, "collection": "Cathedral"},
    {"title": "The Things They Carried", "author": "Tim O'Brien", "year": 1990, "collection": "The Things They Carried"},
    {"title": "Interpreter of Maladies", "author": "Jhumpa Lahiri", "year": 1999, "collection": "Interpreter of Maladies"},
    {"title": "Runaway", "author": "Alice Munro", "year": 2004, "collection": "Runaway"},
]


def fetch_hugo_winners() -> list[dict]:
    """Return Hugo Award winning short stories."""
    print("Fetching Hugo Award winners...")
    stories = []
    for item in HUGO_WINNERS:
        stories.append({
            "title": item["title"],
            "author": item["author"],
            "year": item["year"],
            "collection": item.get("collection"),
            "genres": ["Science Fiction", "Fantasy"],
            "recognitions": [{"type": "Hugo Award", "year": item["year"], "details": "Winner"}],
        })
    print(f"  Found {len(stories)} stories")
    return stories


def fetch_nebula_winners() -> list[dict]:
    """Return Nebula Award winning short stories."""
    print("Fetching Nebula Award winners...")
    stories = []
    for item in NEBULA_WINNERS:
        stories.append({
            "title": item["title"],
            "author": item["author"],
            "year": item["year"],
            "collection": item.get("collection"),
            "genres": ["Science Fiction", "Fantasy"],
            "recognitions": [{"type": "Nebula Award", "year": item["year"], "details": "Winner"}],
        })
    print(f"  Found {len(stories)} stories")
    return stories


def fetch_ohenry_winners() -> list[dict]:
    """Return O. Henry Prize winning short stories."""
    print("Fetching O. Henry Prize winners...")
    stories = []
    for item in OHENRY_WINNERS:
        stories.append({
            "title": item["title"],
            "author": item["author"],
            "year": item["year"],
            "collection": item.get("collection"),
            "genres": ["Literary Fiction"],
            "recognitions": [{"type": "O. Henry Prize", "year": item["year"], "details": "Winner"}],
        })
    print(f"  Found {len(stories)} stories")
    return stories
