"""Classic and genre-specific essential albums."""

# Jazz Classics - essential jazz albums
JAZZ_CLASSICS = [
    {"artist": "Miles Davis", "album": "Kind of Blue", "year": 1959},
    {"artist": "John Coltrane", "album": "A Love Supreme", "year": 1965},
    {"artist": "Miles Davis", "album": "Bitches Brew", "year": 1970},
    {"artist": "Herbie Hancock", "album": "Head Hunters", "year": 1973},
    {"artist": "Charles Mingus", "album": "Mingus Ah Um", "year": 1959},
    {"artist": "Thelonious Monk", "album": "Brilliant Corners", "year": 1957},
    {"artist": "Dave Brubeck", "album": "Time Out", "year": 1959},
    {"artist": "Bill Evans Trio", "album": "Waltz for Debby", "year": 1962},
    {"artist": "Ornette Coleman", "album": "The Shape of Jazz to Come", "year": 1959},
    {"artist": "Art Blakey & The Jazz Messengers", "album": "Moanin'", "year": 1958},
    {"artist": "Kamasi Washington", "album": "The Epic", "year": 2015},
    {"artist": "Snarky Puppy", "album": "We Like It Here", "year": 2014},
    {"artist": "Robert Glasper Experiment", "album": "Black Radio", "year": 2012},
    {"artist": "Esperanza Spalding", "album": "Emily's D+Evolution", "year": 2016},
]

# Metal Essentials - classic and modern metal
METAL_ESSENTIALS = [
    {"artist": "Black Sabbath", "album": "Paranoid", "year": 1970},
    {"artist": "Metallica", "album": "Master of Puppets", "year": 1986},
    {"artist": "Iron Maiden", "album": "The Number of the Beast", "year": 1982},
    {"artist": "Slayer", "album": "Reign in Blood", "year": 1986},
    {"artist": "Megadeth", "album": "Rust in Peace", "year": 1990},
    {"artist": "Pantera", "album": "Vulgar Display of Power", "year": 1992},
    {"artist": "Tool", "album": "Lateralus", "year": 2001},
    {"artist": "Opeth", "album": "Blackwater Park", "year": 2001},
    {"artist": "Mastodon", "album": "Crack the Skye", "year": 2009},
    {"artist": "Gojira", "album": "From Mars to Sirius", "year": 2005},
    {"artist": "Meshuggah", "album": "ObZen", "year": 2008},
    {"artist": "Deafheaven", "album": "Sunbather", "year": 2013},
    {"artist": "Sleep", "album": "Dopesmoker", "year": 2003},
    {"artist": "Electric Wizard", "album": "Dopethrone", "year": 2000},
]

# Electronic/Dance Classics
ELECTRONIC_CLASSICS = [
    {"artist": "Kraftwerk", "album": "Trans-Europe Express", "year": 1977},
    {"artist": "Aphex Twin", "album": "Selected Ambient Works 85-92", "year": 1992},
    {"artist": "Boards of Canada", "album": "Music Has the Right to Children", "year": 1998},
    {"artist": "Burial", "album": "Untrue", "year": 2007},
    {"artist": "Autechre", "album": "Tri Repetae", "year": 1995},
    {"artist": "The Prodigy", "album": "The Fat of the Land", "year": 1997},
    {"artist": "The Chemical Brothers", "album": "Dig Your Own Hole", "year": 1997},
    {"artist": "Massive Attack", "album": "Mezzanine", "year": 1998},
    {"artist": "Portishead", "album": "Dummy", "year": 1994},
    {"artist": "Four Tet", "album": "Rounds", "year": 2003},
    {"artist": "Flying Lotus", "album": "Cosmogramma", "year": 2010},
    {"artist": "Nicolas Jaar", "album": "Space Is Only Noise", "year": 2011},
    {"artist": "Jon Hopkins", "album": "Immunity", "year": 2013},
    {"artist": "Arca", "album": "Kick i", "year": 2020},
]

# Hip-Hop Classics
HIPHOP_CLASSICS = [
    {"artist": "Nas", "album": "Illmatic", "year": 1994},
    {"artist": "Wu-Tang Clan", "album": "Enter the Wu-Tang (36 Chambers)", "year": 1993},
    {"artist": "A Tribe Called Quest", "album": "The Low End Theory", "year": 1991},
    {"artist": "The Notorious B.I.G.", "album": "Ready to Die", "year": 1994},
    {"artist": "Dr. Dre", "album": "The Chronic", "year": 1992},
    {"artist": "MF DOOM", "album": "Madvillainy", "year": 2004},
    {"artist": "Kanye West", "album": "The College Dropout", "year": 2004},
    {"artist": "Kendrick Lamar", "album": "good kid, m.A.A.d city", "year": 2012},
    {"artist": "Run the Jewels", "album": "Run the Jewels 2", "year": 2014},
    {"artist": "Danny Brown", "album": "Atrocity Exhibition", "year": 2016},
    {"artist": "Little Simz", "album": "Sometimes I Might Be Introvert", "year": 2021},
    {"artist": "Tyler, the Creator", "album": "CALL ME IF YOU GET LOST", "year": 2021},
]

# Singer-Songwriter / Folk
FOLK_CLASSICS = [
    {"artist": "Joni Mitchell", "album": "Blue", "year": 1971},
    {"artist": "Nick Drake", "album": "Pink Moon", "year": 1972},
    {"artist": "Leonard Cohen", "album": "Songs of Leonard Cohen", "year": 1967},
    {"artist": "Bob Dylan", "album": "Blood on the Tracks", "year": 1975},
    {"artist": "Elliott Smith", "album": "Either/Or", "year": 1997},
    {"artist": "Jeff Buckley", "album": "Grace", "year": 1994},
    {"artist": "Iron & Wine", "album": "The Creek Drank the Cradle", "year": 2002},
    {"artist": "Bon Iver", "album": "22, A Million", "year": 2016},
    {"artist": "Big Thief", "album": "U.F.O.F.", "year": 2019},
    {"artist": "Adrianne Lenker", "album": "songs", "year": 2020},
]


def fetch_jazz_classics() -> list[dict]:
    """Return essential jazz albums."""
    print("Fetching Jazz Classics...")
    albums = []
    for item in JAZZ_CLASSICS:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [{"type": "Jazz Essential", "year": item["year"], "details": "Classic"}],
        })
    print(f"  Found {len(albums)} albums")
    return albums


def fetch_metal_essentials() -> list[dict]:
    """Return essential metal albums."""
    print("Fetching Metal Essentials...")
    albums = []
    for item in METAL_ESSENTIALS:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [{"type": "Metal Essential", "year": item["year"], "details": "Classic"}],
        })
    print(f"  Found {len(albums)} albums")
    return albums


def fetch_electronic_classics() -> list[dict]:
    """Return essential electronic albums."""
    print("Fetching Electronic Classics...")
    albums = []
    for item in ELECTRONIC_CLASSICS:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [{"type": "Electronic Essential", "year": item["year"], "details": "Classic"}],
        })
    print(f"  Found {len(albums)} albums")
    return albums


def fetch_hiphop_classics() -> list[dict]:
    """Return essential hip-hop albums."""
    print("Fetching Hip-Hop Classics...")
    albums = []
    for item in HIPHOP_CLASSICS:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [{"type": "Hip-Hop Essential", "year": item["year"], "details": "Classic"}],
        })
    print(f"  Found {len(albums)} albums")
    return albums


def fetch_folk_classics() -> list[dict]:
    """Return essential folk/singer-songwriter albums."""
    print("Fetching Folk/Singer-Songwriter Classics...")
    albums = []
    for item in FOLK_CLASSICS:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [{"type": "Folk Essential", "year": item["year"], "details": "Classic"}],
        })
    print(f"  Found {len(albums)} albums")
    return albums
