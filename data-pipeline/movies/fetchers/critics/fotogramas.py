"""
Fotogramas (Spain) fetcher.
Spain's oldest and most prestigious film magazine - annual awards.
"""

import sys
sys.path.insert(0, str(__file__).rsplit("/", 4)[0])

from catalog import MovieEntry, Recognition

# Fotogramas de Plata - Best International Film winners and nominees
FOTOGRAMAS_FILMS = {
    2024: [
        ("Anatomy of a Fall", "Justine Triet"),
        ("Past Lives", "Celine Song"),
        ("The Zone of Interest", "Jonathan Glazer"),
        ("Poor Things", "Yorgos Lanthimos"),
        ("Oppenheimer", "Christopher Nolan"),
    ],
    2023: [
        ("Tár", "Todd Field"),
        ("The Banshees of Inisherin", "Martin McDonagh"),
        ("Triangle of Sadness", "Ruben Östlund"),
        ("Decision to Leave", "Park Chan-wook"),
        ("Everything Everywhere All at Once", "Daniel Kwan"),
    ],
    2022: [
        ("Drive My Car", "Ryusuke Hamaguchi"),
        ("The Power of the Dog", "Jane Campion"),
        ("Licorice Pizza", "Paul Thomas Anderson"),
        ("The Worst Person in the World", "Joachim Trier"),
        ("Belfast", "Kenneth Branagh"),
    ],
    2021: [
        ("Nomadland", "Chloé Zhao"),
        ("Another Round", "Thomas Vinterberg"),
        ("Minari", "Lee Isaac Chung"),
        ("The Father", "Florian Zeller"),
        ("Promising Young Woman", "Emerald Fennell"),
    ],
    2020: [
        ("Parasite", "Bong Joon-ho"),
        ("1917", "Sam Mendes"),
        ("Portrait of a Lady on Fire", "Céline Sciamma"),
        ("Marriage Story", "Noah Baumbach"),
        ("Joker", "Todd Phillips"),
    ],
    2019: [
        ("Roma", "Alfonso Cuarón"),
        ("Cold War", "Pawel Pawlikowski"),
        ("The Favourite", "Yorgos Lanthimos"),
        ("Green Book", "Peter Farrelly"),
        ("A Star Is Born", "Bradley Cooper"),
    ],
    2018: [
        ("The Shape of Water", "Guillermo del Toro"),
        ("Three Billboards Outside Ebbing, Missouri", "Martin McDonagh"),
        ("Phantom Thread", "Paul Thomas Anderson"),
        ("Call Me by Your Name", "Luca Guadagnino"),
        ("Lady Bird", "Greta Gerwig"),
    ],
    2017: [
        ("Moonlight", "Barry Jenkins"),
        ("La La Land", "Damien Chazelle"),
        ("Manchester by the Sea", "Kenneth Lonergan"),
        ("Toni Erdmann", "Maren Ade"),
        ("Elle", "Paul Verhoeven"),
    ],
    2016: [
        ("Son of Saul", "László Nemes"),
        ("Spotlight", "Tom McCarthy"),
        ("Carol", "Todd Haynes"),
        ("The Revenant", "Alejandro González Iñárritu"),
        ("Room", "Lenny Abrahamson"),
    ],
    2015: [
        ("Boyhood", "Richard Linklater"),
        ("Birdman", "Alejandro González Iñárritu"),
        ("Whiplash", "Damien Chazelle"),
        ("The Grand Budapest Hotel", "Wes Anderson"),
        ("Ida", "Pawel Pawlikowski"),
    ],
}


class FotogramasFetcher:
    """Fetches Fotogramas (Spain) top films."""
    
    name = "Fotogramas (Spain)"
    recognition_type = "Fotogramas (Spain)"
    
    def fetch(self, min_year: int = 2000) -> list[MovieEntry]:
        """Fetch Fotogramas top films since min_year."""
        movies = []
        
        for year, films in FOTOGRAMAS_FILMS.items():
            if year < min_year:
                continue
            
            for title, director in films:
                movies.append(MovieEntry(
                    title=title,
                    year=year - 1,  # Awards given for previous year's films
                    director=director,
                    recognitions=[Recognition(
                        type="Fotogramas (Spain)",
                        year=year,
                        details="Top 5"
                    )]
                ))
            print(f"  {year}: Added {len(films)} films")
        
        return movies
