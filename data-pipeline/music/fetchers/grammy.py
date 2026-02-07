"""Grammy Award winners fetcher."""

# Album of the Year winners (recent decades)
GRAMMY_AOTY = [
    {"artist": "Taylor Swift", "album": "Midnights", "year": 2024},
    {"artist": "Harry Styles", "album": "Harry's House", "year": 2023},
    {"artist": "Jon Batiste", "album": "We Are", "year": 2022},
    {"artist": "Taylor Swift", "album": "Folklore", "year": 2021},
    {"artist": "Billie Eilish", "album": "When We All Fall Asleep, Where Do We Go?", "year": 2020},
    {"artist": "Kacey Musgraves", "album": "Golden Hour", "year": 2019},
    {"artist": "Bruno Mars", "album": "24K Magic", "year": 2018},
    {"artist": "Adele", "album": "25", "year": 2017},
    {"artist": "Taylor Swift", "album": "1989", "year": 2016},
    {"artist": "Beck", "album": "Morning Phase", "year": 2015},
    {"artist": "Daft Punk", "album": "Random Access Memories", "year": 2014},
    {"artist": "Mumford & Sons", "album": "Babel", "year": 2013},
    {"artist": "Adele", "album": "21", "year": 2012},
    {"artist": "Arcade Fire", "album": "The Suburbs", "year": 2011},
    {"artist": "Taylor Swift", "album": "Fearless", "year": 2010},
    {"artist": "Robert Plant & Alison Krauss", "album": "Raising Sand", "year": 2009},
    {"artist": "Herbie Hancock", "album": "River: The Joni Letters", "year": 2008},
    {"artist": "Dixie Chicks", "album": "Taking the Long Way", "year": 2007},
    {"artist": "U2", "album": "How to Dismantle an Atomic Bomb", "year": 2006},
    {"artist": "Ray Charles", "album": "Genius Loves Company", "year": 2005},
    {"artist": "OutKast", "album": "Speakerboxxx/The Love Below", "year": 2004},
]

# Best Alternative Album winners
GRAMMY_ALTERNATIVE = [
    {"artist": "Boygenius", "album": "The Record", "year": 2024},
    {"artist": "Wet Leg", "album": "Wet Leg", "year": 2023},
    {"artist": "St. Vincent", "album": "Daddy's Home", "year": 2022},
    {"artist": "Fiona Apple", "album": "Fetch the Bolt Cutters", "year": 2021},
    {"artist": "Vampire Weekend", "album": "Father of the Bride", "year": 2020},
    {"artist": "St. Vincent", "album": "Masseduction", "year": 2019},
    {"artist": "The National", "album": "Sleep Well Beast", "year": 2018},
    {"artist": "David Bowie", "album": "Blackstar", "year": 2017},
    {"artist": "Alabama Shakes", "album": "Sound & Color", "year": 2016},
    {"artist": "St. Vincent", "album": "St. Vincent", "year": 2015},
    {"artist": "Vampire Weekend", "album": "Modern Vampires of the City", "year": 2014},
    {"artist": "Gotye", "album": "Making Mirrors", "year": 2013},
    {"artist": "Bon Iver", "album": "Bon Iver", "year": 2012},
    {"artist": "Arcade Fire", "album": "The Suburbs", "year": 2011},
    {"artist": "Phoenix", "album": "Wolfgang Amadeus Phoenix", "year": 2010},
    {"artist": "Radiohead", "album": "In Rainbows", "year": 2009},
    {"artist": "Wilco", "album": "Sky Blue Sky", "year": 2008},
]


def fetch_grammy_albums() -> list[dict]:
    """Return Grammy Award winning albums."""
    print("Fetching Grammy Award winners...")
    albums = []
    
    for item in GRAMMY_AOTY:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [
                {
                    "type": "Grammy Album of the Year",
                    "year": item["year"],
                    "details": "Winner"
                }
            ],
        })
    
    for item in GRAMMY_ALTERNATIVE:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [
                {
                    "type": "Grammy Best Alternative Album",
                    "year": item["year"],
                    "details": "Winner"
                }
            ],
        })
    
    print(f"  Found {len(albums)} albums")
    return albums
