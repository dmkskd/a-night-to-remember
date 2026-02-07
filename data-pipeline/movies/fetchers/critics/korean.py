"""
Korean Association of Film Critics Awards (KAFCA) fetcher.
Annual best film awards from Korea's film critics association.
"""

import sys
sys.path.insert(0, str(__file__).rsplit("/", 4)[0])

from catalog import MovieEntry, Recognition

# KAFCA Best Film winners and top picks (international focus)
KAFCA_FILMS = {
    2024: [
        ("Exhuma", "Jang Jae-hyun"),
        ("12.12: The Day", "Kim Sung-su"),
        ("Concrete Utopia", "Um Tae-hwa"),
        ("Past Lives", "Celine Song"),
        ("The Zone of Interest", "Jonathan Glazer"),
    ],
    2023: [
        ("Decision to Leave", "Park Chan-wook"),
        ("Broker", "Hirokazu Kore-eda"),
        ("The Banshees of Inisherin", "Martin McDonagh"),
        ("Tár", "Todd Field"),
        ("Triangle of Sadness", "Ruben Östlund"),
    ],
    2022: [
        ("Drive My Car", "Ryusuke Hamaguchi"),
        ("Escape from Mogadishu", "Ryoo Seung-wan"),
        ("The Power of the Dog", "Jane Campion"),
        ("The Worst Person in the World", "Joachim Trier"),
        ("Petite Maman", "Céline Sciamma"),
    ],
    2021: [
        ("Minari", "Lee Isaac Chung"),
        ("The Book of Fish", "Lee Joon-ik"),
        ("Nomadland", "Chloé Zhao"),
        ("Another Round", "Thomas Vinterberg"),
        ("First Cow", "Kelly Reichardt"),
    ],
    2020: [
        ("Parasite", "Bong Joon-ho"),
        ("The Gangster, the Cop, the Devil", "Lee Won-tae"),
        ("Portrait of a Lady on Fire", "Céline Sciamma"),
        ("Marriage Story", "Noah Baumbach"),
        ("Pain and Glory", "Pedro Almodóvar"),
    ],
    2019: [
        ("Burning", "Lee Chang-dong"),
        ("Default", "Choi Kook-hee"),
        ("Roma", "Alfonso Cuarón"),
        ("Cold War", "Pawel Pawlikowski"),
        ("Shoplifters", "Hirokazu Kore-eda"),
    ],
    2018: [
        ("1987: When the Day Comes", "Jang Joon-hwan"),
        ("A Taxi Driver", "Jang Hoon"),
        ("The Shape of Water", "Guillermo del Toro"),
        ("Phantom Thread", "Paul Thomas Anderson"),
        ("Call Me by Your Name", "Luca Guadagnino"),
    ],
    2017: [
        ("The Handmaiden", "Park Chan-wook"),
        ("The Wailing", "Na Hong-jin"),
        ("Moonlight", "Barry Jenkins"),
        ("Toni Erdmann", "Maren Ade"),
        ("La La Land", "Damien Chazelle"),
    ],
    2016: [
        ("The Assassin", "Hou Hsiao-hsien"),
        ("Veteran", "Ryoo Seung-wan"),
        ("Carol", "Todd Haynes"),
        ("Son of Saul", "László Nemes"),
        ("Mad Max: Fury Road", "George Miller"),
    ],
    2015: [
        ("A Hard Day", "Kim Seong-hun"),
        ("Ode to My Father", "Yoon Je-kyoon"),
        ("Boyhood", "Richard Linklater"),
        ("Whiplash", "Damien Chazelle"),
        ("Ida", "Pawel Pawlikowski"),
    ],
}


class KoreanCriticsFetcher:
    """Fetches Korean Film Critics Association top films."""
    
    name = "Korean Film Critics (KAFCA)"
    recognition_type = "Korean Film Critics (KAFCA)"
    
    def fetch(self, min_year: int = 2000) -> list[MovieEntry]:
        """Fetch Korean critics' top films since min_year."""
        movies = []
        
        for year, films in KAFCA_FILMS.items():
            if year < min_year:
                continue
            
            for title, director in films:
                movies.append(MovieEntry(
                    title=title,
                    year=year - 1,  # Awards given for previous year's films
                    director=director,
                    recognitions=[Recognition(
                        type="Korean Film Critics (KAFCA)",
                        year=year,
                        details="Top 5"
                    )]
                ))
            print(f"  {year}: Added {len(films)} films")
        
        return movies
