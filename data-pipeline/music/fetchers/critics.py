"""Quality music sources - critic and community-driven lists."""

# Mercury Prize Winners & Nominees (UK - highly respected)
MERCURY_PRIZE = [
    # Winners
    {"artist": "English Teacher", "album": "This Could Be Texas", "year": 2024, "details": "Winner"},
    {"artist": "CMAT", "album": "Crazymad, for Me", "year": 2024, "details": "Nominee"},
    {"artist": "Beth Gibbons", "album": "Lives Outgrown", "year": 2024, "details": "Nominee"},
    {"artist": "Charli XCX", "album": "Brat", "year": 2024, "details": "Nominee"},
    {"artist": "The Last Dinner Party", "album": "Prelude to Ecstasy", "year": 2024, "details": "Nominee"},
    {"artist": "Ezra Collective", "album": "Where I'm Meant to Be", "year": 2023, "details": "Winner"},
    {"artist": "Self Esteem", "album": "Prioritise Pleasure", "year": 2022, "details": "Nominee"},
    {"artist": "Arlo Parks", "album": "Collapsed in Sunbeams", "year": 2021, "details": "Winner"},
    {"artist": "Michael Kiwanuka", "album": "Kiwanuka", "year": 2020, "details": "Winner"},
    {"artist": "Dave", "album": "Psychodrama", "year": 2019, "details": "Winner"},
    {"artist": "Wolf Alice", "album": "Visions of a Life", "year": 2018, "details": "Winner"},
    {"artist": "Sampha", "album": "Process", "year": 2017, "details": "Winner"},
    {"artist": "Skepta", "album": "Konnichiwa", "year": 2016, "details": "Winner"},
    {"artist": "Benjamin Clementine", "album": "At Least for Now", "year": 2015, "details": "Winner"},
    {"artist": "Young Fathers", "album": "Dead", "year": 2014, "details": "Winner"},
    {"artist": "James Blake", "album": "Overgrown", "year": 2013, "details": "Winner"},
    {"artist": "Alt-J", "album": "An Awesome Wave", "year": 2012, "details": "Winner"},
    {"artist": "PJ Harvey", "album": "Let England Shake", "year": 2011, "details": "Winner"},
    {"artist": "The xx", "album": "xx", "year": 2010, "details": "Winner"},
    # Notable nominees
    {"artist": "black midi", "album": "Hellfire", "year": 2022, "details": "Nominee"},
    {"artist": "Little Simz", "album": "Sometimes I Might Be Introvert", "year": 2022, "details": "Nominee"},
    {"artist": "Squid", "album": "Bright Green Field", "year": 2021, "details": "Nominee"},
    {"artist": "SAULT", "album": "Untitled (Black Is)", "year": 2021, "details": "Nominee"},
    {"artist": "Laura Marling", "album": "Song for Our Daughter", "year": 2020, "details": "Nominee"},
    {"artist": "Porridge Radio", "album": "Every Bad", "year": 2020, "details": "Nominee"},
]

# Polaris Music Prize (Canada - artist-focused, no label influence)
POLARIS_PRIZE = [
    {"artist": "Charlotte Cardin", "album": "99 Nights", "year": 2024, "details": "Winner"},
    {"artist": "Elisapie", "album": "Inuktitut", "year": 2023, "details": "Winner"},
    {"artist": "Backxwash", "album": "God Has Nothing to Do with This Leave Him Out of It", "year": 2020, "details": "Winner"},
    {"artist": "Haviah Mighty", "album": "13th Floor", "year": 2019, "details": "Winner"},
    {"artist": "Jeremy Dutcher", "album": "Wolastoqiyik Lintuwakonawa", "year": 2018, "details": "Winner"},
    {"artist": "Lido Pimienta", "album": "La Papessa", "year": 2017, "details": "Winner"},
    {"artist": "Kaytranada", "album": "99.9%", "year": 2016, "details": "Winner"},
    {"artist": "Buffy Sainte-Marie", "album": "Power in the Blood", "year": 2015, "details": "Winner"},
    {"artist": "Tanya Tagaq", "album": "Animism", "year": 2014, "details": "Winner"},
    {"artist": "Godspeed You! Black Emperor", "album": "Allelujah! Don't Bend! Ascend!", "year": 2013, "details": "Winner"},
    {"artist": "Feist", "album": "Metals", "year": 2012, "details": "Winner"},
    {"artist": "Arcade Fire", "album": "The Suburbs", "year": 2011, "details": "Winner"},
    {"artist": "Karkwa", "album": "Les Chemins de verre", "year": 2010, "details": "Winner"},
]

# Wire Magazine / Quietus - Experimental & Avant-garde
EXPERIMENTAL_PICKS = [
    {"artist": "Adrianne Lenker", "album": "Bright Future", "year": 2024},
    {"artist": "Cindy Lee", "album": "Diamond Jubilee", "year": 2024},
    {"artist": "Kim Gordon", "album": "The Collective", "year": 2024},
    {"artist": "Geordie Greep", "album": "The New Sound", "year": 2024},
    {"artist": "Mabe Fratti", "album": "Sentir Que No Sabes", "year": 2024},
    {"artist": "claire rousay", "album": "sentiment", "year": 2024},
    {"artist": "Arca", "album": "KicK iii", "year": 2021},
    {"artist": "SOPHIE", "album": "Oil of Every Pearl's Un-Insides", "year": 2018},
    {"artist": "Oneohtrix Point Never", "album": "Age Of", "year": 2018},
    {"artist": "Grouper", "album": "Grid of Points", "year": 2018},
    {"artist": "Tim Hecker", "album": "Konoyo", "year": 2018},
    {"artist": "Yves Tumor", "album": "Safe in the Hands of Love", "year": 2018},
    {"artist": "Daughters", "album": "You Won't Get What You Want", "year": 2018},
    {"artist": "Anna Meredith", "album": "Varmints", "year": 2016},
    {"artist": "Jenny Hval", "album": "Blood Bitch", "year": 2016},
    {"artist": "Mica Levi", "album": "Under the Skin OST", "year": 2014},
    {"artist": "Swans", "album": "To Be Kind", "year": 2014},
    {"artist": "Scott Walker", "album": "Bish Bosch", "year": 2012},
    {"artist": "Julia Holter", "album": "Have You in My Wilderness", "year": 2015},
    {"artist": "Holly Herndon", "album": "Platform", "year": 2015},
    {"artist": "Dean Blunt", "album": "Black Metal", "year": 2014},
    {"artist": "FKA twigs", "album": "LP1", "year": 2014},
]

# Bandcamp Daily / Underground picks
UNDERGROUND_PICKS = [
    {"artist": "MJ Lenderman", "album": "Manning Fireworks", "year": 2024},
    {"artist": "Waxahatchee", "album": "Tigers Blood", "year": 2024},
    {"artist": "Jessica Pratt", "album": "Here in the Pitch", "year": 2024},
    {"artist": "Fontaines D.C.", "album": "Romance", "year": 2024},
    {"artist": "Magdalena Bay", "album": "Imaginal Disk", "year": 2024},
    {"artist": "Nick Cave & The Bad Seeds", "album": "Wild God", "year": 2024},
    {"artist": "Vampire Weekend", "album": "Only God Was Above Us", "year": 2024},
    {"artist": "Clairo", "album": "Charm", "year": 2024},
    {"artist": "Mk.gee", "album": "Two Star & the Dream Police", "year": 2024},
    {"artist": "Mdou Moctar", "album": "Funeral for Justice", "year": 2024},
    {"artist": "Mdou Moctar", "album": "Afrique Victime", "year": 2021},
    {"artist": "Arooj Aftab", "album": "Vulture Prince", "year": 2021},
    {"artist": "Cassandra Jenkins", "album": "An Overview on Phenomenal Nature", "year": 2021},
    {"artist": "Floating Points, Pharoah Sanders & LSO", "album": "Promises", "year": 2021},
    {"artist": "Tirzah", "album": "Colourgrade", "year": 2021},
    {"artist": "Dry Cleaning", "album": "New Long Leg", "year": 2021},
    {"artist": "Lingua Ignota", "album": "Sinner Get Ready", "year": 2021},
    {"artist": "Injury Reserve", "album": "By the Time I Get to Phoenix", "year": 2021},
    {"artist": "Turnstile", "album": "Glow On", "year": 2021},
    {"artist": "Spellling", "album": "The Turning Wheel", "year": 2021},
    {"artist": "Parquet Courts", "album": "Wide Awake!", "year": 2018},
    {"artist": "IDLES", "album": "Joy as an Act of Resistance", "year": 2018},
    {"artist": "Khruangbin", "album": "Con Todo El Mundo", "year": 2018},
    {"artist": "Noname", "album": "Room 25", "year": 2018},
    {"artist": "Mitski", "album": "Be the Cowboy", "year": 2018},
    {"artist": "Snail Mail", "album": "Lush", "year": 2018},
    {"artist": "Soccer Mommy", "album": "Clean", "year": 2018},
    {"artist": "Hop Along", "album": "Bark Your Head Off, Dog", "year": 2018},
    {"artist": "Car Seat Headrest", "album": "Twin Fantasy", "year": 2018},
    {"artist": "Jeff Rosenstock", "album": "POST-", "year": 2018},
]

# World Music / Global sounds
WORLD_MUSIC = [
    {"artist": "Tinariwen", "album": "Amadjar", "year": 2019},
    {"artist": "Bombino", "album": "Deran", "year": 2018},
    {"artist": "Fatoumata Diawara", "album": "Fenfo", "year": 2018},
    {"artist": "Ibeyi", "album": "Ash", "year": 2017},
    {"artist": "Anoushka Shankar", "album": "Land of Gold", "year": 2016},
    {"artist": "Mulatu Astatke", "album": "Sketches of Ethiopia", "year": 2013},
    {"artist": "Ali Farka Touré & Toumani Diabaté", "album": "Ali and Toumani", "year": 2010},
    {"artist": "Rokia Traoré", "album": "Tchamantché", "year": 2008},
    {"artist": "Oumou Sangaré", "album": "Seya", "year": 2009},
    {"artist": "Orchestra Baobab", "album": "Specialist in All Styles", "year": 2002},
    {"artist": "Buena Vista Social Club", "album": "Buena Vista Social Club", "year": 1997},
    {"artist": "Fela Kuti", "album": "Zombie", "year": 1977},
]


def fetch_mercury_prize() -> list[dict]:
    """Return Mercury Prize winners and notable nominees."""
    print("Fetching Mercury Prize albums...")
    albums = []
    for item in MERCURY_PRIZE:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [{"type": "Mercury Prize", "year": item["year"], "details": item.get("details", "")}],
        })
    print(f"  Found {len(albums)} albums")
    return albums


def fetch_polaris_prize() -> list[dict]:
    """Return Polaris Music Prize winners."""
    print("Fetching Polaris Music Prize albums...")
    albums = []
    for item in POLARIS_PRIZE:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [{"type": "Polaris Prize", "year": item["year"], "details": item.get("details", "")}],
        })
    print(f"  Found {len(albums)} albums")
    return albums


def fetch_experimental() -> list[dict]:
    """Return experimental/avant-garde picks."""
    print("Fetching Experimental/Avant-garde albums...")
    albums = []
    for item in EXPERIMENTAL_PICKS:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [{"type": "Experimental Essential", "year": item["year"], "details": "Critics' Pick"}],
        })
    print(f"  Found {len(albums)} albums")
    return albums


def fetch_underground() -> list[dict]:
    """Return underground/indie picks."""
    print("Fetching Underground/Indie albums...")
    albums = []
    for item in UNDERGROUND_PICKS:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [{"type": "Underground Essential", "year": item["year"], "details": "Critics' Pick"}],
        })
    print(f"  Found {len(albums)} albums")
    return albums


def fetch_world_music() -> list[dict]:
    """Return world music essentials."""
    print("Fetching World Music albums...")
    albums = []
    for item in WORLD_MUSIC:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [{"type": "World Music Essential", "year": item["year"], "details": "Classic"}],
        })
    print(f"  Found {len(albums)} albums")
    return albums
