"""
German Film Critics Association (Verband der deutschen Filmkritik) fetcher.
Annual best film awards from Germany's film critics.
"""

import sys
sys.path.insert(0, str(__file__).rsplit("/", 3)[0])

from catalog import MovieEntry, Recognition

# German Film Critics Association - Best Film winners
GERMAN_CRITICS_FILMS = {
    2024: [
        ("The Zone of Interest", "Jonathan Glazer"),
        ("Anatomy of a Fall", "Justine Triet"),
        ("Past Lives", "Celine Song"),
        ("All of Us Strangers", "Andrew Haigh"),
        ("The Teachers' Lounge", "İlker Çatak"),
    ],
    2023: [
        ("Tár", "Todd Field"),
        ("Decision to Leave", "Park Chan-wook"),
        ("Triangle of Sadness", "Ruben Östlund"),
        ("Aftersun", "Charlotte Wells"),
        ("Holy Spider", "Ali Abbasi"),
    ],
    2022: [
        ("Drive My Car", "Ryusuke Hamaguchi"),
        ("The Worst Person in the World", "Joachim Trier"),
        ("Licorice Pizza", "Paul Thomas Anderson"),
        ("Petite Maman", "Céline Sciamma"),
        ("A Hero", "Asghar Farhadi"),
    ],
    2021: [
        ("Nomadland", "Chloé Zhao"),
        ("First Cow", "Kelly Reichardt"),
        ("Minari", "Lee Isaac Chung"),
        ("Another Round", "Thomas Vinterberg"),
        ("Never Rarely Sometimes Always", "Eliza Hittman"),
    ],
    2020: [
        ("Parasite", "Bong Joon-ho"),
        ("Portrait of a Lady on Fire", "Céline Sciamma"),
        ("Marriage Story", "Noah Baumbach"),
        ("The Lighthouse", "Robert Eggers"),
        ("Pain and Glory", "Pedro Almodóvar"),
    ],
    2019: [
        ("Roma", "Alfonso Cuarón"),
        ("Cold War", "Pawel Pawlikowski"),
        ("Burning", "Lee Chang-dong"),
        ("The Favourite", "Yorgos Lanthimos"),
        ("Shoplifters", "Hirokazu Kore-eda"),
    ],
    2018: [
        ("The Square", "Ruben Östlund"),
        ("Phantom Thread", "Paul Thomas Anderson"),
        ("Call Me by Your Name", "Luca Guadagnino"),
        ("Lady Bird", "Greta Gerwig"),
        ("The Florida Project", "Sean Baker"),
    ],
    2017: [
        ("Toni Erdmann", "Maren Ade"),
        ("Moonlight", "Barry Jenkins"),
        ("Elle", "Paul Verhoeven"),
        ("Paterson", "Jim Jarmusch"),
        ("Manchester by the Sea", "Kenneth Lonergan"),
    ],
    2016: [
        ("Son of Saul", "László Nemes"),
        ("Carol", "Todd Haynes"),
        ("The Assassin", "Hou Hsiao-hsien"),
        ("Spotlight", "Tom McCarthy"),
        ("Room", "Lenny Abrahamson"),
    ],
    2015: [
        ("Boyhood", "Richard Linklater"),
        ("Leviathan", "Andrey Zvyagintsev"),
        ("Winter Sleep", "Nuri Bilge Ceylan"),
        ("Ida", "Pawel Pawlikowski"),
        ("Whiplash", "Damien Chazelle"),
    ],
}


class GermanCriticsFetcher:
    """Fetches German Film Critics Association top films."""
    
    name = "German Film Critics"
    recognition_type = "German Film Critics"
    
    def fetch(self, min_year: int = 2000) -> list[MovieEntry]:
        """Fetch German critics' top films since min_year."""
        movies = []
        
        for year, films in GERMAN_CRITICS_FILMS.items():
            if year < min_year:
                continue
            
            for title, director in films:
                movies.append(MovieEntry(
                    title=title,
                    year=year - 1,  # Awards given for previous year's films
                    director=director,
                    recognitions=[Recognition(
                        type="German Film Critics",
                        year=year,
                        details="Top 5"
                    )]
                ))
            print(f"  {year}: Added {len(films)} films")
        
        return movies
