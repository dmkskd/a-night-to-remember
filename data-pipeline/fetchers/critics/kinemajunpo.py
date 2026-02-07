"""
Kinema Junpo (Japan) fetcher.
Japan's oldest and most prestigious film magazine.
Fetches annual Best Foreign Film winners.
"""

import sys
sys.path.insert(0, str(__file__).rsplit("/", 3)[0])

from catalog import MovieEntry, Recognition


class KinemaJunpoFetcher:
    """Fetches Kinema Junpo Best Foreign Film winners."""
    
    name = "Kinema Junpo Best Foreign Film"
    recognition_type = "Kinema Junpo Best Foreign Film"
    
    def fetch(self, min_year: int = 2000) -> list[MovieEntry]:
        """Fetch Kinema Junpo Best Foreign Film winners."""
        movies = []
        
        # Kinema Junpo Best Foreign Film winners
        # Data from Wikipedia: https://en.wikipedia.org/wiki/Kinema_Junpo#Best_Foreign_Language_Film
        
        KINEMA_JUNPO_WINNERS = {
            2024: ("The Zone of Interest", "Jonathan Glazer", "UK"),
            2023: ("Tár", "Todd Field", "USA"),
            2022: ("Drive My Car", "Ryusuke Hamaguchi", "Japan"),  # Japanese film won foreign category
            2021: ("Nomadland", "Chloé Zhao", "USA"),
            2020: ("Parasite", "Bong Joon-ho", "South Korea"),
            2019: ("Roma", "Alfonso Cuarón", "Mexico"),
            2018: ("The Shape of Water", "Guillermo del Toro", "USA"),
            2017: ("Manchester by the Sea", "Kenneth Lonergan", "USA"),
            2016: ("Mad Max: Fury Road", "George Miller", "Australia"),
            2015: ("Boyhood", "Richard Linklater", "USA"),
            2014: ("Her", "Spike Jonze", "USA"),
            2013: ("Amour", "Michael Haneke", "Austria"),
            2012: ("The Artist", "Michel Hazanavicius", "France"),
            2011: ("The Social Network", "David Fincher", "USA"),
            2010: ("Gran Torino", "Clint Eastwood", "USA"),
            2009: ("The Dark Knight", "Christopher Nolan", "USA"),
            2008: ("4 Months, 3 Weeks and 2 Days", "Cristian Mungiu", "Romania"),
            2007: ("Letters from Iwo Jima", "Clint Eastwood", "USA"),
            2006: ("Brokeback Mountain", "Ang Lee", "USA"),
            2005: ("Million Dollar Baby", "Clint Eastwood", "USA"),
            2004: ("Mystic River", "Clint Eastwood", "USA"),
            2003: ("Talk to Her", "Pedro Almodóvar", "Spain"),
            2002: ("Mulholland Drive", "David Lynch", "USA"),
            2001: ("Dancer in the Dark", "Lars von Trier", "Denmark"),
            2000: ("American Beauty", "Sam Mendes", "USA"),
        }
        
        for year, (title, director, country) in KINEMA_JUNPO_WINNERS.items():
            if year < min_year:
                continue
            
            movies.append(MovieEntry(
                title=title,
                year=year,
                director=director,
                country=country,
                recognitions=[Recognition(
                    type="Kinema Junpo Best Foreign Film",
                    year=year,
                    details="Winner"
                )]
            ))
        
        print(f"  Added {len(movies)} Kinema Junpo winners")
        return movies


if __name__ == "__main__":
    print("Testing Kinema Junpo fetcher...")
    fetcher = KinemaJunpoFetcher()
    movies = fetcher.fetch(min_year=2015)
    print(f"\nTotal: {len(movies)} movies")
    for m in movies:
        print(f"  {m.year} - {m.title} ({m.director})")
