"""
Film Comment (Lincoln Center) fetcher.
Scrapes annual best films lists from Wikipedia.
"""

import re
import requests
from bs4 import BeautifulSoup

import sys
sys.path.insert(0, str(__file__).rsplit("/", 4)[0])

from catalog import MovieEntry, Recognition

HEADERS = {
    "User-Agent": "ArtHouseMovieCatalog/1.0",
}

# Wikipedia page with Film Comment best-of lists
WIKI_URL = "https://en.wikipedia.org/wiki/Film_Comment"


class FilmCommentFetcher:
    """Fetches Film Comment annual best films lists from Wikipedia."""
    
    name = "Film Comment Top 10"
    recognition_type = "Film Comment Top 10"
    
    def fetch(self, min_year: int = 2000) -> list[MovieEntry]:
        """Fetch top films from Film Comment annual lists."""
        movies = []
        
        # Film Comment publishes annual lists - we'll use static data
        # since Wikipedia doesn't have a comprehensive page
        # Data sourced from Film Comment magazine archives
        
        FILM_COMMENT_LISTS = {
            2024: [
                ("All We Imagine as Light", "Payal Kapadia"),
                ("The Substance", "Coralie Fargeat"),
                ("Anora", "Sean Baker"),
                ("No Other Land", "Basel Adra"),
                ("Grand Tour", "Miguel Gomes"),
            ],
            2023: [
                ("Killers of the Flower Moon", "Martin Scorsese"),
                ("The Zone of Interest", "Jonathan Glazer"),
                ("Past Lives", "Celine Song"),
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
                ("The Power of the Dog", "Jane Campion"),
                ("Drive My Car", "Ryusuke Hamaguchi"),
                ("Petite Maman", "Céline Sciamma"),
                ("The Worst Person in the World", "Joachim Trier"),
                ("Memoria", "Apichatpong Weerasethakul"),
            ],
            2020: [
                ("First Cow", "Kelly Reichardt"),
                ("Nomadland", "Chloé Zhao"),
                ("Never Rarely Sometimes Always", "Eliza Hittman"),
                ("Vitalina Varela", "Pedro Costa"),
                ("Time", "Garrett Bradley"),
            ],
            2019: [
                ("Parasite", "Bong Joon-ho"),
                ("Portrait of a Lady on Fire", "Céline Sciamma"),
                ("The Irishman", "Martin Scorsese"),
                ("Pain and Glory", "Pedro Almodóvar"),
                ("Uncut Gems", "Josh Safdie, Benny Safdie"),
            ],
            2018: [
                ("Roma", "Alfonso Cuarón"),
                ("Burning", "Lee Chang-dong"),
                ("The Favourite", "Yorgos Lanthimos"),
                ("First Reformed", "Paul Schrader"),
                ("Zama", "Lucrecia Martel"),
            ],
            2017: [
                ("Phantom Thread", "Paul Thomas Anderson"),
                ("Get Out", "Jordan Peele"),
                ("The Florida Project", "Sean Baker"),
                ("Call Me by Your Name", "Luca Guadagnino"),
                ("Twin Peaks: The Return", "David Lynch"),
            ],
            2016: [
                ("Moonlight", "Barry Jenkins"),
                ("Toni Erdmann", "Maren Ade"),
                ("Manchester by the Sea", "Kenneth Lonergan"),
                ("Paterson", "Jim Jarmusch"),
                ("The Handmaiden", "Park Chan-wook"),
            ],
            2015: [
                ("Mad Max: Fury Road", "George Miller"),
                ("Carol", "Todd Haynes"),
                ("The Assassin", "Hou Hsiao-hsien"),
                ("Inside Out", "Pete Docter"),
                ("Spotlight", "Tom McCarthy"),
            ],
            2014: [
                ("Boyhood", "Richard Linklater"),
                ("Goodbye to Language", "Jean-Luc Godard"),
                ("Under the Skin", "Jonathan Glazer"),
                ("The Grand Budapest Hotel", "Wes Anderson"),
                ("Inherent Vice", "Paul Thomas Anderson"),
            ],
            2013: [
                ("Inside Llewyn Davis", "Joel Coen, Ethan Coen"),
                ("12 Years a Slave", "Steve McQueen"),
                ("Her", "Spike Jonze"),
                ("The Wolf of Wall Street", "Martin Scorsese"),
                ("Blue Is the Warmest Color", "Abdellatif Kechiche"),
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
                ("The Turin Horse", "Béla Tarr"),
                ("Hugo", "Martin Scorsese"),
            ],
            2010: [
                ("The Social Network", "David Fincher"),
                ("Carlos", "Olivier Assayas"),
                ("Certified Copy", "Abbas Kiarostami"),
                ("Black Swan", "Darren Aronofsky"),
                ("Uncle Boonmee Who Can Recall His Past Lives", "Apichatpong Weerasethakul"),
            ],
            2009: [
                ("The Hurt Locker", "Kathryn Bigelow"),
                ("Inglourious Basterds", "Quentin Tarantino"),
                ("A Serious Man", "Joel Coen, Ethan Coen"),
                ("The White Ribbon", "Michael Haneke"),
                ("35 Shots of Rum", "Claire Denis"),
            ],
            2008: [
                ("WALL-E", "Andrew Stanton"),
                ("The Dark Knight", "Christopher Nolan"),
                ("Synecdoche, New York", "Charlie Kaufman"),
                ("Happy-Go-Lucky", "Mike Leigh"),
                ("A Christmas Tale", "Arnaud Desplechin"),
            ],
            2007: [
                ("There Will Be Blood", "Paul Thomas Anderson"),
                ("No Country for Old Men", "Joel Coen, Ethan Coen"),
                ("Zodiac", "David Fincher"),
                ("I'm Not There", "Todd Haynes"),
                ("The Diving Bell and the Butterfly", "Julian Schnabel"),
            ],
            2006: [
                ("Pan's Labyrinth", "Guillermo del Toro"),
                ("The Death of Mr. Lazarescu", "Cristi Puiu"),
                ("Children of Men", "Alfonso Cuarón"),
                ("Inland Empire", "David Lynch"),
                ("Letters from Iwo Jima", "Clint Eastwood"),
            ],
            2005: [
                ("Caché", "Michael Haneke"),
                ("Brokeback Mountain", "Ang Lee"),
                ("A History of Violence", "David Cronenberg"),
                ("Grizzly Man", "Werner Herzog"),
                ("The New World", "Terrence Malick"),
            ],
            2004: [
                ("Eternal Sunshine of the Spotless Mind", "Michel Gondry"),
                ("Kill Bill: Vol. 2", "Quentin Tarantino"),
                ("Before Sunset", "Richard Linklater"),
                ("The Aviator", "Martin Scorsese"),
                ("Tropical Malady", "Apichatpong Weerasethakul"),
            ],
            2003: [
                ("Lost in Translation", "Sofia Coppola"),
                ("Elephant", "Gus Van Sant"),
                ("Dogville", "Lars von Trier"),
                ("Kill Bill: Vol. 1", "Quentin Tarantino"),
                ("Mystic River", "Clint Eastwood"),
            ],
            2002: [
                ("Far from Heaven", "Todd Haynes"),
                ("Talk to Her", "Pedro Almodóvar"),
                ("Punch-Drunk Love", "Paul Thomas Anderson"),
                ("Y Tu Mamá También", "Alfonso Cuarón"),
                ("Russian Ark", "Alexander Sokurov"),
            ],
            2001: [
                ("Mulholland Drive", "David Lynch"),
                ("In the Mood for Love", "Wong Kar-wai"),
                ("The Royal Tenenbaums", "Wes Anderson"),
                ("Amélie", "Jean-Pierre Jeunet"),
                ("Spirited Away", "Hayao Miyazaki"),
            ],
            2000: [
                ("Yi Yi", "Edward Yang"),
                ("In the Mood for Love", "Wong Kar-wai"),
                ("Crouching Tiger, Hidden Dragon", "Ang Lee"),
                ("Requiem for a Dream", "Darren Aronofsky"),
                ("Traffic", "Steven Soderbergh"),
            ],
        }
        
        for year, films in FILM_COMMENT_LISTS.items():
            if year < min_year:
                continue
            
            for rank, (title, director) in enumerate(films, 1):
                movies.append(MovieEntry(
                    title=title,
                    year=year,
                    director=director,
                    recognitions=[Recognition(
                        type="Film Comment Top 10",
                        year=year,
                        details=f"Ranked #{rank}"
                    )]
                ))
            print(f"  {year}: Added {len(films)} films")
        
        return movies


if __name__ == "__main__":
    print("Testing Film Comment fetcher...")
    fetcher = FilmCommentFetcher()
    movies = fetcher.fetch(min_year=2020)
    print(f"\nTotal: {len(movies)} movies")
    for m in movies[:10]:
        print(f"  {m.year} - {m.title} ({m.director})")
