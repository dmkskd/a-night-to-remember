"""
Indiewire Critics Poll fetcher.
Annual top films as voted by critics.
"""

import sys
sys.path.insert(0, str(__file__).rsplit("/", 3)[0])

from catalog import MovieEntry, Recognition

# Indiewire Critics Poll - Top films each year (curated selection)
INDIEWIRE_TOP_FILMS = {
    2024: [
        ("Anora", "Sean Baker"),
        ("The Brutalist", "Brady Corbet"),
        ("All We Imagine as Light", "Payal Kapadia"),
        ("I'm Still Here", "Walter Salles"),
        ("A Real Pain", "Jesse Eisenberg"),
    ],
    2023: [
        ("Past Lives", "Celine Song"),
        ("Killers of the Flower Moon", "Martin Scorsese"),
        ("The Zone of Interest", "Jonathan Glazer"),
        ("Anatomy of a Fall", "Justine Triet"),
        ("Poor Things", "Yorgos Lanthimos"),
    ],
    2022: [
        ("Tár", "Todd Field"),
        ("Decision to Leave", "Park Chan-wook"),
        ("Aftersun", "Charlotte Wells"),
        ("The Banshees of Inisherin", "Martin McDonagh"),
        ("EO", "Jerzy Skolimowski"),
    ],
    2021: [
        ("Drive My Car", "Ryusuke Hamaguchi"),
        ("The Power of the Dog", "Jane Campion"),
        ("The Worst Person in the World", "Joachim Trier"),
        ("Petite Maman", "Céline Sciamma"),
        ("Memoria", "Apichatpong Weerasethakul"),
    ],
    2020: [
        ("Nomadland", "Chloé Zhao"),
        ("First Cow", "Kelly Reichardt"),
        ("Never Rarely Sometimes Always", "Eliza Hittman"),
        ("Minari", "Lee Isaac Chung"),
        ("Time", "Garrett Bradley"),
    ],
    2019: [
        ("Parasite", "Bong Joon-ho"),
        ("Portrait of a Lady on Fire", "Céline Sciamma"),
        ("The Irishman", "Martin Scorsese"),
        ("Marriage Story", "Noah Baumbach"),
        ("Uncut Gems", "Josh Safdie"),
    ],
    2018: [
        ("Roma", "Alfonso Cuarón"),
        ("The Favourite", "Yorgos Lanthimos"),
        ("Burning", "Lee Chang-dong"),
        ("First Reformed", "Paul Schrader"),
        ("Shoplifters", "Hirokazu Kore-eda"),
    ],
    2017: [
        ("Get Out", "Jordan Peele"),
        ("Phantom Thread", "Paul Thomas Anderson"),
        ("Call Me by Your Name", "Luca Guadagnino"),
        ("The Florida Project", "Sean Baker"),
        ("Lady Bird", "Greta Gerwig"),
    ],
    2016: [
        ("Moonlight", "Barry Jenkins"),
        ("Manchester by the Sea", "Kenneth Lonergan"),
        ("Toni Erdmann", "Maren Ade"),
        ("La La Land", "Damien Chazelle"),
        ("Paterson", "Jim Jarmusch"),
    ],
    2015: [
        ("Carol", "Todd Haynes"),
        ("Mad Max: Fury Road", "George Miller"),
        ("Spotlight", "Tom McCarthy"),
        ("The Assassin", "Hou Hsiao-hsien"),
        ("Son of Saul", "László Nemes"),
    ],
    2014: [
        ("Boyhood", "Richard Linklater"),
        ("Under the Skin", "Jonathan Glazer"),
        ("Goodbye to Language", "Jean-Luc Godard"),
        ("Inherent Vice", "Paul Thomas Anderson"),
        ("Leviathan", "Andrey Zvyagintsev"),
    ],
    2013: [
        ("12 Years a Slave", "Steve McQueen"),
        ("Inside Llewyn Davis", "Joel Coen"),
        ("Blue Is the Warmest Color", "Abdellatif Kechiche"),
        ("Her", "Spike Jonze"),
        ("Before Midnight", "Richard Linklater"),
    ],
    2012: [
        ("The Master", "Paul Thomas Anderson"),
        ("Holy Motors", "Leos Carax"),
        ("Amour", "Michael Haneke"),
        ("Moonrise Kingdom", "Wes Anderson"),
        ("Zero Dark Thirty", "Kathryn Bigelow"),
    ],
    2011: [
        ("The Tree of Life", "Terrence Malick"),
        ("A Separation", "Asghar Farhadi"),
        ("Melancholia", "Lars von Trier"),
        ("The Artist", "Michel Hazanavicius"),
        ("Drive", "Nicolas Winding Refn"),
    ],
    2010: [
        ("The Social Network", "David Fincher"),
        ("Black Swan", "Darren Aronofsky"),
        ("Uncle Boonmee Who Can Recall His Past Lives", "Apichatpong Weerasethakul"),
        ("Carlos", "Olivier Assayas"),
        ("Certified Copy", "Abbas Kiarostami"),
    ],
}


class IndiewireFetcher:
    """Fetches Indiewire Critics Poll top films."""
    
    name = "Indiewire Critics Poll"
    recognition_type = "Indiewire Critics Poll"
    
    def fetch(self, min_year: int = 2000) -> list[MovieEntry]:
        """Fetch Indiewire top films since min_year."""
        movies = []
        
        for year, films in INDIEWIRE_TOP_FILMS.items():
            if year < min_year:
                continue
            
            for title, director in films:
                movies.append(MovieEntry(
                    title=title,
                    year=year,
                    director=director,
                    recognitions=[Recognition(
                        type="Indiewire Critics Poll",
                        year=year,
                        details="Top 5"
                    )]
                ))
            print(f"  {year}: Added {len(films)} films")
        
        return movies
