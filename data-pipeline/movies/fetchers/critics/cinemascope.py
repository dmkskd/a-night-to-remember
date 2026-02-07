"""
Cinema Scope Best Films fetcher.
Canadian art-house film magazine's annual top 10.
"""

import sys
sys.path.insert(0, str(__file__).rsplit("/", 4)[0])

from catalog import MovieEntry, Recognition

# Cinema Scope Top 10 - highly respected art-house picks
CINEMASCOPE_TOP_FILMS = {
    2024: [
        ("Grand Tour", "Miguel Gomes"),
        ("All We Imagine as Light", "Payal Kapadia"),
        ("Dahomey", "Mati Diop"),
        ("No Other Land", "Basel Adra"),
        ("Caught by the Tides", "Jia Zhangke"),
    ],
    2023: [
        ("The Zone of Interest", "Jonathan Glazer"),
        ("Showing Up", "Kelly Reichardt"),
        ("Asteroid City", "Wes Anderson"),
        ("About Dry Grasses", "Nuri Bilge Ceylan"),
        ("Fallen Leaves", "Aki Kaurismäki"),
    ],
    2022: [
        ("Saint Omer", "Alice Diop"),
        ("Decision to Leave", "Park Chan-wook"),
        ("Aftersun", "Charlotte Wells"),
        ("EO", "Jerzy Skolimowski"),
        ("Pacifiction", "Albert Serra"),
    ],
    2021: [
        ("Drive My Car", "Ryusuke Hamaguchi"),
        ("Memoria", "Apichatpong Weerasethakul"),
        ("Petite Maman", "Céline Sciamma"),
        ("The Worst Person in the World", "Joachim Trier"),
        ("Wheel of Fortune and Fantasy", "Ryusuke Hamaguchi"),
    ],
    2020: [
        ("First Cow", "Kelly Reichardt"),
        ("Vitalina Varela", "Pedro Costa"),
        ("Never Rarely Sometimes Always", "Eliza Hittman"),
        ("Malmkrog", "Cristi Puiu"),
        ("The Woman Who Ran", "Hong Sang-soo"),
    ],
    2019: [
        ("Parasite", "Bong Joon-ho"),
        ("Portrait of a Lady on Fire", "Céline Sciamma"),
        ("An Elephant Sitting Still", "Hu Bo"),
        ("A Hidden Life", "Terrence Malick"),
        ("Varda by Agnès", "Agnès Varda"),
    ],
    2018: [
        ("Burning", "Lee Chang-dong"),
        ("Zama", "Lucrecia Martel"),
        ("The Image Book", "Jean-Luc Godard"),
        ("Ash Is Purest White", "Jia Zhangke"),
        ("Cold War", "Pawel Pawlikowski"),
    ],
    2017: [
        ("Twin Peaks: The Return", "David Lynch"),
        ("A Quiet Passion", "Terence Davies"),
        ("The Day After", "Hong Sang-soo"),
        ("Good Time", "Josh Safdie"),
        ("Phantom Thread", "Paul Thomas Anderson"),
    ],
    2016: [
        ("Toni Erdmann", "Maren Ade"),
        ("Paterson", "Jim Jarmusch"),
        ("Certain Women", "Kelly Reichardt"),
        ("The Handmaiden", "Park Chan-wook"),
        ("Elle", "Paul Verhoeven"),
    ],
    2015: [
        ("The Assassin", "Hou Hsiao-hsien"),
        ("Carol", "Todd Haynes"),
        ("Right Now, Wrong Then", "Hong Sang-soo"),
        ("Cemetery of Splendour", "Apichatpong Weerasethakul"),
        ("Mountains May Depart", "Jia Zhangke"),
    ],
    2014: [
        ("Goodbye to Language", "Jean-Luc Godard"),
        ("Horse Money", "Pedro Costa"),
        ("Jauja", "Lisandro Alonso"),
        ("Winter Sleep", "Nuri Bilge Ceylan"),
        ("Stray Dogs", "Tsai Ming-liang"),
    ],
    2013: [
        ("A Touch of Sin", "Jia Zhangke"),
        ("Inside Llewyn Davis", "Joel Coen"),
        ("Blue Is the Warmest Color", "Abdellatif Kechiche"),
        ("The Act of Killing", "Joshua Oppenheimer"),
        ("Norte, the End of History", "Lav Diaz"),
    ],
    2012: [
        ("Holy Motors", "Leos Carax"),
        ("The Master", "Paul Thomas Anderson"),
        ("Tabu", "Miguel Gomes"),
        ("Amour", "Michael Haneke"),
        ("Post Tenebras Lux", "Carlos Reygadas"),
    ],
    2011: [
        ("The Turin Horse", "Béla Tarr"),
        ("The Tree of Life", "Terrence Malick"),
        ("A Separation", "Asghar Farhadi"),
        ("Once Upon a Time in Anatolia", "Nuri Bilge Ceylan"),
        ("Melancholia", "Lars von Trier"),
    ],
    2010: [
        ("Uncle Boonmee Who Can Recall His Past Lives", "Apichatpong Weerasethakul"),
        ("Certified Copy", "Abbas Kiarostami"),
        ("Film Socialisme", "Jean-Luc Godard"),
        ("Carlos", "Olivier Assayas"),
        ("Poetry", "Lee Chang-dong"),
    ],
}


class CinemaScopeFetcher:
    """Fetches Cinema Scope top films."""
    
    name = "Cinema Scope Top 10"
    recognition_type = "Cinema Scope Top 10"
    
    def fetch(self, min_year: int = 2000) -> list[MovieEntry]:
        """Fetch Cinema Scope top films since min_year."""
        movies = []
        
        for year, films in CINEMASCOPE_TOP_FILMS.items():
            if year < min_year:
                continue
            
            for title, director in films:
                movies.append(MovieEntry(
                    title=title,
                    year=year,
                    director=director,
                    recognitions=[Recognition(
                        type="Cinema Scope Top 10",
                        year=year,
                        details="Top 5"
                    )]
                ))
            print(f"  {year}: Added {len(films)} films")
        
        return movies
