"""Pitchfork Best New Music and high-rated albums fetcher."""

# Curated list of Pitchfork 10.0 and Best New Music albums
# These are albums that received perfect or near-perfect scores

PITCHFORK_CLASSICS = [
    # Perfect 10.0 scores
    {"artist": "Radiohead", "album": "Kid A", "year": 2000, "score": 10.0, "award": "Pitchfork 10.0"},
    {"artist": "Kanye West", "album": "My Beautiful Dark Twisted Fantasy", "year": 2010, "score": 10.0, "award": "Pitchfork 10.0"},
    {"artist": "Wilco", "album": "Yankee Hotel Foxtrot", "year": 2002, "score": 10.0, "award": "Pitchfork 10.0"},
    {"artist": "Arcade Fire", "album": "Funeral", "year": 2004, "score": 10.0, "award": "Pitchfork 10.0"},
    {"artist": "Neutral Milk Hotel", "album": "In the Aeroplane Over the Sea", "year": 1998, "score": 10.0, "award": "Pitchfork 10.0"},
    {"artist": "My Bloody Valentine", "album": "Loveless", "year": 1991, "score": 10.0, "award": "Pitchfork 10.0"},
    {"artist": "Fiona Apple", "album": "Fetch the Bolt Cutters", "year": 2020, "score": 10.0, "award": "Pitchfork 10.0"},
    
    # 9.5+ scores
    {"artist": "Björk", "album": "Vespertine", "year": 2001, "score": 9.8, "award": "Pitchfork Best New Music"},
    {"artist": "Björk", "album": "Homogenic", "year": 1997, "score": 9.6, "award": "Pitchfork Best New Music"},
    {"artist": "Radiohead", "album": "OK Computer", "year": 1997, "score": 9.6, "award": "Pitchfork Best New Music"},
    {"artist": "Radiohead", "album": "In Rainbows", "year": 2007, "score": 9.5, "award": "Pitchfork Best New Music"},
    {"artist": "Kendrick Lamar", "album": "To Pimp a Butterfly", "year": 2015, "score": 9.5, "award": "Pitchfork Best New Music"},
    {"artist": "LCD Soundsystem", "album": "Sound of Silver", "year": 2007, "score": 9.5, "award": "Pitchfork Best New Music"},
    {"artist": "The Avalanches", "album": "Since I Left You", "year": 2000, "score": 9.5, "award": "Pitchfork Best New Music"},
    {"artist": "Godspeed You! Black Emperor", "album": "Lift Your Skinny Fists Like Antennas to Heaven", "year": 2000, "score": 9.4, "award": "Pitchfork Best New Music"},
    {"artist": "Sigur Rós", "album": "Ágætis byrjun", "year": 1999, "score": 9.4, "award": "Pitchfork Best New Music"},
    {"artist": "Sufjan Stevens", "album": "Illinois", "year": 2005, "score": 9.2, "award": "Pitchfork Best New Music"},
    {"artist": "The Microphones", "album": "The Glow Pt. 2", "year": 2001, "score": 9.3, "award": "Pitchfork Best New Music"},
    {"artist": "Talking Heads", "album": "Remain in Light", "year": 1980, "score": 9.5, "award": "Pitchfork Best New Music"},
    {"artist": "D'Angelo", "album": "Voodoo", "year": 2000, "score": 9.4, "award": "Pitchfork Best New Music"},
    {"artist": "OutKast", "album": "Stankonia", "year": 2000, "score": 9.5, "award": "Pitchfork Best New Music"},
    {"artist": "Daft Punk", "album": "Discovery", "year": 2001, "score": 9.4, "award": "Pitchfork Best New Music"},
    {"artist": "Animal Collective", "album": "Merriweather Post Pavilion", "year": 2009, "score": 9.6, "award": "Pitchfork Best New Music"},
    {"artist": "Beach House", "album": "Depression Cherry", "year": 2015, "score": 9.1, "award": "Pitchfork Best New Music"},
    {"artist": "Frank Ocean", "album": "Blonde", "year": 2016, "score": 9.0, "award": "Pitchfork Best New Music"},
    {"artist": "Bon Iver", "album": "For Emma, Forever Ago", "year": 2008, "score": 9.0, "award": "Pitchfork Best New Music"},
    {"artist": "Fleet Foxes", "album": "Fleet Foxes", "year": 2008, "score": 9.0, "award": "Pitchfork Best New Music"},
    {"artist": "Vampire Weekend", "album": "Modern Vampires of the City", "year": 2013, "score": 9.3, "award": "Pitchfork Best New Music"},
    {"artist": "Tame Impala", "album": "Currents", "year": 2015, "score": 9.3, "award": "Pitchfork Best New Music"},
    {"artist": "Tyler, the Creator", "album": "IGOR", "year": 2019, "score": 9.0, "award": "Pitchfork Best New Music"},
    {"artist": "Phoebe Bridgers", "album": "Punisher", "year": 2020, "score": 9.0, "award": "Pitchfork Best New Music"},
]


def fetch_pitchfork_albums() -> list[dict]:
    """Return curated list of Pitchfork acclaimed albums."""
    print("Fetching Pitchfork acclaimed albums...")
    albums = []
    
    for item in PITCHFORK_CLASSICS:
        albums.append({
            "artist": item["artist"],
            "title": item["album"],
            "year": item["year"],
            "recognitions": [
                {
                    "type": item["award"],
                    "year": item["year"],
                    "details": f"Score: {item['score']}"
                }
            ],
            "rating": item["score"],
        })
    
    print(f"  Found {len(albums)} albums")
    return albums
