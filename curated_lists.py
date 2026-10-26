"""
Curated Film Lists and AI Movie Picker Data Engine
Inspired by MovieDecider.com and PickAMovieForMe.com
"""

CURATED_LISTS = {
    "under-90": {
        "id": "under-90",
        "title": "Great Films Under 90 Minutes",
        "short_desc": "Browse verified films under 90 minutes from the live movie catalog, page by page.",
        "badge": "LIVE CATALOG",
        "tagline": "Start one of these at nine and you will still be in bed before midnight.",
        "editorial": (
            "There is a particular kind of tired where you want to watch something properly — a real film, "
            "with a beginning and an end — but the thought of a two-and-a-half-hour commitment is enough to send you "
            "back to endless scrolling. This list is for that mood. Every displayed film is checked for a runtime "
            "under ninety minutes before it is shown. Short runtimes get unfairly associated with slightness, but a tight film is usually "
            "a disciplined one: nothing padded, no sagging middle act, every scene doing work. Animation and documentary are "
            "over-represented for exactly that reason — both traditions grew up with tight running times and learned to use them."
        ),
        "movies": [
            {"title": "The Lion King", "year": 1994, "rating": 8.5, "genres": "Animation, Drama"},
            {"title": "Modern Times", "year": 1936, "rating": 8.5, "genres": "Comedy, Drama"},
            {"title": "Paths of Glory", "year": 1957, "rating": 8.4, "genres": "Drama, War"},
            {"title": "City Lights", "year": 1931, "rating": 8.5, "genres": "Comedy, Drama"},
            {"title": "Toy Story", "year": 1995, "rating": 8.3, "genres": "Animation, Adventure"},
            {"title": "The Kid", "year": 1921, "rating": 8.2, "genres": "Comedy, Drama"},
            {"title": "Mulan", "year": 1998, "rating": 7.6, "genres": "Animation, Adventure"},
            {"title": "The Iron Giant", "year": 1999, "rating": 8.0, "genres": "Animation, Sci-Fi"},
            {"title": "The Nightmare Before Christmas", "year": 1993, "rating": 7.9, "genres": "Animation, Fantasy"},
            {"title": "Rope", "year": 1948, "rating": 8.0, "genres": "Crime, Thriller"},
            {"title": "Stand by Me", "year": 1986, "rating": 8.1, "genres": "Adventure, Drama"},
            {"title": "Fantastic Mr. Fox", "year": 2009, "rating": 7.9, "genres": "Animation, Comedy"},
            {"title": "Before Sunset", "year": 2004, "rating": 8.1, "genres": "Drama, Romance"},
            {"title": "Grave of the Fireflies", "year": 1988, "rating": 8.5, "genres": "Animation, Drama"},
            {"title": "Run Lola Run", "year": 1998, "rating": 7.7, "genres": "Action, Thriller"},
            {"title": "A Quiet Place", "year": 2018, "rating": 7.5, "genres": "Horror, Sci-Fi"},
            {"title": "Following", "year": 1998, "rating": 7.5, "genres": "Mystery, Thriller"},
            {"title": "Primer", "year": 2004, "rating": 6.9, "genres": "Sci-Fi, Drama"},
            {"title": "Phone Booth", "year": 2002, "rating": 7.1, "genres": "Thriller, Crime"},
            {"title": "Zombieland", "year": 2009, "rating": 7.6, "genres": "Comedy, Horror"},
            {"title": "Airplane!", "year": 1980, "rating": 7.7, "genres": "Comedy"},
            {"title": "Fargo", "year": 1996, "rating": 8.1, "genres": "Crime, Drama"},
            {"title": "Whiplash", "year": 2014, "rating": 8.5, "genres": "Drama, Music"},
            {"title": "Drive", "year": 2011, "rating": 7.8, "genres": "Crime, Drama"}
        ]
    },
    "hidden-gems": {
        "id": "hidden-gems",
        "title": "Hidden Gems: Great Films Almost Nobody Has Seen",
        "short_desc": "Films that rate highly with the people who found them but have a fraction of the audience of a mainstream release — the best of our long tail.",
        "badge": "24 FILMS",
        "tagline": "Deliberately sorted against popularity to surface overlooked cinematic masterpieces.",
        "editorial": (
            "Standard recommendation algorithms obsess over what is trending this week. Hidden Gems works by doing the exact opposite: "
            "we deliberate sort by audience appreciation against total commercial volume. These twenty-four films received little to no "
            "theatrical marketing, yet nearly everyone who watches them rates them four or five stars. If you are tired of seeing the same "
            "thirty blockbusters recycled on every home screen, start exploring here."
        ),
        "movies": [
            {"title": "Coherence", "year": 2013, "rating": 7.2, "genres": "Mystery, Sci-Fi"},
            {"title": "Predestination", "year": 2014, "rating": 7.5, "genres": "Sci-Fi, Thriller"},
            {"title": "The Fall", "year": 2006, "rating": 7.8, "genres": "Adventure, Fantasy"},
            {"title": "Incendies", "year": 2010, "rating": 8.3, "genres": "Drama, Mystery"},
            {"title": "Sing Street", "year": 2016, "rating": 7.9, "genres": "Comedy, Drama, Music"},
            {"title": "Wind River", "year": 2017, "rating": 7.7, "genres": "Crime, Mystery"},
            {"title": "Nightcrawler", "year": 2014, "rating": 7.8, "genres": "Crime, Drama, Thriller"},
            {"title": "Hunt for the Wilderpeople", "year": 2016, "rating": 7.8, "genres": "Adventure, Comedy"},
            {"title": "Captain Fantastic", "year": 2016, "rating": 7.8, "genres": "Comedy, Drama"},
            {"title": "Ex Machina", "year": 2014, "rating": 7.7, "genres": "Sci-Fi, Thriller"},
            {"title": "Moon", "year": 2009, "rating": 7.8, "genres": "Drama, Sci-Fi"},
            {"title": "Locke", "year": 2013, "rating": 7.1, "genres": "Drama"},
            {"title": "Victoria", "year": 2015, "rating": 7.6, "genres": "Crime, Drama"},
            {"title": "The Man from Earth", "year": 2007, "rating": 7.9, "genres": "Drama, Sci-Fi"},
            {"title": "Upgrade", "year": 2018, "rating": 7.5, "genres": "Action, Sci-Fi"},
            {"title": "Prisoners", "year": 2013, "rating": 8.1, "genres": "Crime, Drama, Mystery"},
            {"title": "Columbus", "year": 2017, "rating": 7.2, "genres": "Drama"},
            {"title": "The Florida Project", "year": 2017, "rating": 7.6, "genres": "Drama"},
            {"title": "Short Term 12", "year": 2013, "rating": 7.9, "genres": "Drama"},
            {"title": "About Time", "year": 2013, "rating": 7.8, "genres": "Comedy, Drama, Fantasy"},
            {"title": "Sound of Metal", "year": 2020, "rating": 7.7, "genres": "Drama, Music"},
            {"title": "Margin Call", "year": 2011, "rating": 7.1, "genres": "Drama, Thriller"},
            {"title": "The Nice Guys", "year": 2016, "rating": 7.4, "genres": "Action, Comedy, Crime"},
            {"title": "Sicario", "year": 2015, "rating": 7.6, "genres": "Action, Crime, Drama"}
        ]
    },
    "scifi-think": {
        "id": "scifi-think",
        "title": "Science Fiction That Makes You Think",
        "short_desc": "Well-rated science fiction built on ideas rather than explosions — the films that use the impossible to ask something real.",
        "badge": "24 FILMS",
        "tagline": "Ideas, philosophy, and mind-bending concepts over brainless CGI.",
        "editorial": (
            "Most studio science fiction treats the genre merely as an excuse to destroy skylines with louder lasers. "
            "This list is for viewers who prefer science fiction as a rigorous, thought-provoking philosophical device. "
            "These twenty-four films use alien encounters, simulated realities, paradoxes of time travel, and synthetic consciousness "
            "to interrogate what it actually means to be human."
        ),
        "movies": [
            {"title": "Interstellar", "year": 2014, "rating": 8.6, "genres": "Adventure, Drama, Sci-Fi"},
            {"title": "Inception", "year": 2010, "rating": 8.8, "genres": "Action, Adventure, Sci-Fi"},
            {"title": "The Matrix", "year": 1999, "rating": 8.7, "genres": "Action, Sci-Fi"},
            {"title": "Arrival", "year": 2016, "rating": 7.9, "genres": "Drama, Mystery, Sci-Fi"},
            {"title": "Blade Runner 2049", "year": 2017, "rating": 8.0, "genres": "Action, Drama, Sci-Fi"},
            {"title": "2001: A Space Odyssey", "year": 1968, "rating": 8.3, "genres": "Adventure, Sci-Fi"},
            {"title": "Contact", "year": 1997, "rating": 7.5, "genres": "Drama, Mystery, Sci-Fi"},
            {"title": "Children of Men", "year": 2006, "rating": 7.9, "genres": "Action, Drama, Sci-Fi"},
            {"title": "Eternal Sunshine of the Spotless Mind", "year": 2004, "rating": 8.3, "genres": "Drama, Romance, Sci-Fi"},
            {"title": "Gattaca", "year": 1997, "rating": 7.8, "genres": "Drama, Sci-Fi, Thriller"},
            {"title": "Her", "year": 2013, "rating": 8.0, "genres": "Drama, Romance, Sci-Fi"},
            {"title": "Ex Machina", "year": 2014, "rating": 7.7, "genres": "Drama, Sci-Fi, Thriller"},
            {"title": "Dark City", "year": 1998, "rating": 7.6, "genres": "Mystery, Sci-Fi"},
            {"title": "Twelve Monkeys", "year": 1995, "rating": 8.0, "genres": "Mystery, Sci-Fi, Thriller"},
            {"title": "Donnie Darko", "year": 2001, "rating": 8.0, "genres": "Drama, Mystery, Sci-Fi"},
            {"title": "Solaris", "year": 1972, "rating": 8.0, "genres": "Drama, Mystery, Sci-Fi"},
            {"title": "The Truman Show", "year": 1998, "rating": 8.2, "genres": "Comedy, Drama"},
            {"title": "Source Code", "year": 2011, "rating": 7.5, "genres": "Action, Mystery, Sci-Fi"},
            {"title": "Edge of Tomorrow", "year": 2014, "rating": 7.9, "genres": "Action, Adventure, Sci-Fi"},
            {"title": "Annihilation", "year": 2018, "rating": 6.8, "genres": "Adventure, Drama, Horror"},
            {"title": "Minority Report", "year": 2002, "rating": 7.6, "genres": "Action, Crime, Mystery"},
            {"title": "District 9", "year": 2009, "rating": 7.9, "genres": "Action, Sci-Fi, Thriller"},
            {"title": "Dune: Part Two", "year": 2024, "rating": 8.5, "genres": "Action, Adventure, Sci-Fi"},
            {"title": "The Prestige", "year": 2006, "rating": 8.5, "genres": "Drama, Mystery, Sci-Fi"}
        ]
    },
    "best-90s": {
        "id": "best-90s",
        "title": "The Best Films of the 1990s",
        "short_desc": "The decade of the video store and the independent boom — the best-rated films released between 1990 and 1999.",
        "badge": "24 FILMS",
        "tagline": "Tarantino, Fincher, Spielberg, and the Coen brothers at their absolute peak.",
        "editorial": (
            "Cinema in the 1990s struck a magical balance between studio capital and unfiltered directorial ambition. "
            "Independent distributors like Miramax proved that idiosyncratic dialogue and non-linear narratives could fill multiplexes, "
            "while revolutionary digital effects were deployed in service of transcendent storytelling rather than replacing it."
        ),
        "movies": [
            {"title": "Pulp Fiction", "year": 1994, "rating": 8.9, "genres": "Crime, Drama"},
            {"title": "The Shawshank Redemption", "year": 1994, "rating": 9.3, "genres": "Drama"},
            {"title": "Fight Club", "year": 1999, "rating": 8.8, "genres": "Drama"},
            {"title": "The Matrix", "year": 1999, "rating": 8.7, "genres": "Action, Sci-Fi"},
            {"title": "Goodfellas", "year": 1990, "rating": 8.7, "genres": "Biography, Crime, Drama"},
            {"title": "Se7en", "year": 1995, "rating": 8.6, "genres": "Crime, Drama, Mystery"},
            {"title": "The Silence of the Lambs", "year": 1991, "rating": 8.6, "genres": "Crime, Drama, Thriller"},
            {"title": "Forrest Gump", "year": 1994, "rating": 8.8, "genres": "Drama, Romance"},
            {"title": "Saving Private Ryan", "year": 1998, "rating": 8.6, "genres": "Drama, War"},
            {"title": "The Green Mile", "year": 1999, "rating": 8.6, "genres": "Crime, Drama, Fantasy"},
            {"title": "Fargo", "year": 1996, "rating": 8.1, "genres": "Crime, Drama, Thriller"},
            {"title": "The Big Lebowski", "year": 1998, "rating": 8.1, "genres": "Comedy, Crime"},
            {"title": "Jurassic Park", "year": 1993, "rating": 8.2, "genres": "Action, Adventure, Sci-Fi"},
            {"title": "Heat", "year": 1995, "rating": 8.3, "genres": "Action, Crime, Drama"},
            {"title": "The Usual Suspects", "year": 1995, "rating": 8.5, "genres": "Crime, Mystery, Thriller"},
            {"title": "Léon: The Professional", "year": 1994, "rating": 8.5, "genres": "Action, Crime, Drama"},
            {"title": "American Beauty", "year": 1999, "rating": 8.3, "genres": "Drama"},
            {"title": "Magnolia", "year": 1999, "rating": 8.0, "genres": "Drama"},
            {"title": "Reservoir Dogs", "year": 1992, "rating": 8.3, "genres": "Crime, Drama, Thriller"},
            {"title": "L.A. Confidential", "year": 1997, "rating": 8.2, "genres": "Crime, Drama, Mystery"},
            {"title": "Schindler's List", "year": 1993, "rating": 9.0, "genres": "Biography, Drama, History"},
            {"title": "The Sixth Sense", "year": 1999, "rating": 8.2, "genres": "Drama, Mystery, Thriller"},
            {"title": "Toy Story", "year": 1995, "rating": 8.3, "genres": "Animation, Adventure, Comedy"},
            {"title": "Princess Mononoke", "year": 1997, "rating": 8.4, "genres": "Animation, Action, Adventure"}
        ]
    },
    "family-agree": {
        "id": "family-agree",
        "title": "Family Films Everyone Can Actually Agree On",
        "short_desc": "Films that work for a room with a wide age range — well-rated family titles that do not condescend to anyone in it.",
        "badge": "24 FILMS",
        "tagline": "Pure joy that enchants eight-year-olds without boring parents.",
        "editorial": (
            "Family movie night is notoriously tricky to negotiate. The younger audience wants color and kinetic energy; "
            "adults dread grating jokes and lazy slapstick. These twenty-four masterpieces solve that dilemma: heartfelt, "
            "visually stunning, emotionally mature, and thoroughly entertaining for viewers of every age."
        ),
        "movies": [
            {"title": "Spirited Away", "year": 2001, "rating": 8.6, "genres": "Animation, Adventure, Family"},
            {"title": "Up", "year": 2009, "rating": 8.3, "genres": "Animation, Adventure, Comedy"},
            {"title": "WALL·E", "year": 2008, "rating": 8.4, "genres": "Animation, Adventure, Family"},
            {"title": "Coco", "year": 2017, "rating": 8.4, "genres": "Animation, Adventure, Family"},
            {"title": "Finding Nemo", "year": 2003, "rating": 8.2, "genres": "Animation, Adventure, Comedy"},
            {"title": "Ratatouille", "year": 2007, "rating": 8.1, "genres": "Animation, Comedy, Family"},
            {"title": "Inside Out", "year": 2015, "rating": 8.1, "genres": "Animation, Adventure, Comedy"},
            {"title": "The Incredibles", "year": 2004, "rating": 8.0, "genres": "Animation, Action, Adventure"},
            {"title": "Spider-Man: Into the Spider-Verse", "year": 2018, "rating": 8.4, "genres": "Animation, Action, Adventure"},
            {"title": "Paddington 2", "year": 2017, "rating": 7.8, "genres": "Adventure, Comedy, Family"},
            {"title": "Toy Story 3", "year": 2010, "rating": 8.3, "genres": "Animation, Adventure, Comedy"},
            {"title": "Monsters, Inc.", "year": 2001, "rating": 8.1, "genres": "Animation, Adventure, Comedy"},
            {"title": "How to Train Your Dragon", "year": 2010, "rating": 8.1, "genres": "Animation, Action, Adventure"},
            {"title": "The Lion King", "year": 1994, "rating": 8.5, "genres": "Animation, Drama, Family"},
            {"title": "Zootopia", "year": 2016, "rating": 8.0, "genres": "Animation, Adventure, Comedy"},
            {"title": "Shrek", "year": 2001, "rating": 7.9, "genres": "Animation, Adventure, Comedy"},
            {"title": "Fantastic Mr. Fox", "year": 2009, "rating": 7.9, "genres": "Animation, Adventure, Comedy"},
            {"title": "Klaus", "year": 2019, "rating": 8.2, "genres": "Animation, Adventure, Comedy"},
            {"title": "Soul", "year": 2020, "rating": 8.0, "genres": "Animation, Adventure, Comedy"},
            {"title": "Paddington", "year": 2014, "rating": 7.3, "genres": "Adventure, Comedy, Family"},
            {"title": "Harry Potter and the Prisoner of Azkaban", "year": 2004, "rating": 7.9, "genres": "Adventure, Family, Fantasy"},
            {"title": "Back to the Future", "year": 1985, "rating": 8.5, "genres": "Adventure, Comedy, Sci-Fi"},
            {"title": "The Princess Bride", "year": 1987, "rating": 8.0, "genres": "Adventure, Family, Fantasy"},
            {"title": "School of Rock", "year": 2003, "rating": 7.2, "genres": "Comedy, Music"}
        ]
    },
    "crime-late-night": {
        "id": "crime-late-night",
        "title": "Crime Films Worth a Late Night",
        "short_desc": "Heists, investigations and slow-burn character studies — the best-rated crime films in our library.",
        "badge": "24 FILMS",
        "tagline": "Neon-lit streets, razor-sharp dialogue, and high-stakes moral ambiguity.",
        "editorial": (
            "When the clock passes midnight, lighthearted entertainment won't do. You need grit, tension, meticulously planned heists, "
            "and moral ambiguity. These twenty-four films represent the pinnacle of crime cinema — from Scorsese's mob sagas to Fincher's "
            "obsessive police procedural investigations."
        ),
        "movies": [
            {"title": "The Dark Knight", "year": 2008, "rating": 9.0, "genres": "Action, Crime, Drama"},
            {"title": "Goodfellas", "year": 1990, "rating": 8.7, "genres": "Biography, Crime, Drama"},
            {"title": "Pulp Fiction", "year": 1994, "rating": 8.9, "genres": "Crime, Drama"},
            {"title": "The Godfather", "year": 1972, "rating": 9.2, "genres": "Crime, Drama"},
            {"title": "The Godfather Part II", "year": 1974, "rating": 9.0, "genres": "Crime, Drama"},
            {"title": "Heat", "year": 1995, "rating": 8.3, "genres": "Action, Crime, Drama"},
            {"title": "Se7en", "year": 1995, "rating": 8.6, "genres": "Crime, Drama, Mystery"},
            {"title": "The Departed", "year": 2006, "rating": 8.5, "genres": "Crime, Drama, Thriller"},
            {"title": "No Country for Old Men", "year": 2007, "rating": 8.2, "genres": "Crime, Drama, Thriller"},
            {"title": "Fargo", "year": 1996, "rating": 8.1, "genres": "Crime, Drama, Thriller"},
            {"title": "Reservoir Dogs", "year": 1992, "rating": 8.3, "genres": "Crime, Drama, Thriller"},
            {"title": "Memories of Murder", "year": 2003, "rating": 8.1, "genres": "Crime, Drama, Mystery"},
            {"title": "The Usual Suspects", "year": 1995, "rating": 8.5, "genres": "Crime, Mystery, Thriller"},
            {"title": "Zodiac", "year": 2007, "rating": 7.7, "genres": "Crime, Drama, Mystery"},
            {"title": "Prisoners", "year": 2013, "rating": 8.1, "genres": "Crime, Drama, Mystery"},
            {"title": "Sicario", "year": 2015, "rating": 7.6, "genres": "Action, Crime, Drama"},
            {"title": "Drive", "year": 2011, "rating": 7.8, "genres": "Action, Drama"},
            {"title": "Baby Driver", "year": 2017, "rating": 7.6, "genres": "Action, Crime, Drama"},
            {"title": "Ocean's Eleven", "year": 2001, "rating": 7.7, "genres": "Crime, Thriller"},
            {"title": "The Town", "year": 2010, "rating": 7.5, "genres": "Crime, Drama, Thriller"},
            {"title": "Snatch", "year": 2000, "rating": 8.2, "genres": "Comedy, Crime"},
            {"title": "Collateral", "year": 2004, "rating": 7.5, "genres": "Action, Crime, Drama"},
            {"title": "Nightcrawler", "year": 2014, "rating": 7.8, "genres": "Crime, Drama, Thriller"},
            {"title": "Training Day", "year": 2001, "rating": 7.7, "genres": "Crime, Drama, Thriller"}
        ]
    },
    "comedies-hold-up": {
        "id": "comedies-hold-up",
        "title": "Comedies That Actually Hold Up",
        "short_desc": "Comedy dates faster than any other genre. These are the ones that survived — the best-rated comedies in our library.",
        "badge": "24 FILMS",
        "tagline": "Timeless jokes, brilliant timing, and belly laughs that never get old.",
        "editorial": (
            "Slang changes, pop culture references evaporate, and societal norms evolve. That makes comedic filmmaking the most fragile "
            "genre in cinema history. The twenty-four comedies assembled here don't rely on cheap gimmicks — they succeed because of "
            "impeccable character construction, timeless wit, and universal human quirks."
        ),
        "movies": [
            {"title": "The Big Lebowski", "year": 1998, "rating": 8.1, "genres": "Comedy, Crime"},
            {"title": "Groundhog Day", "year": 1993, "rating": 8.0, "genres": "Comedy, Fantasy, Romance"},
            {"title": "Superbad", "year": 2007, "rating": 7.6, "genres": "Comedy"},
            {"title": "The Grand Budapest Hotel", "year": 2014, "rating": 8.1, "genres": "Adventure, Comedy, Crime"},
            {"title": "Shaun of the Dead", "year": 2004, "rating": 7.9, "genres": "Comedy, Horror"},
            {"title": "Monty Python and the Holy Grail", "year": 1975, "rating": 8.2, "genres": "Adventure, Comedy, Fantasy"},
            {"title": "Hot Fuzz", "year": 2007, "rating": 7.8, "genres": "Action, Comedy, Mystery"},
            {"title": "What We Do in the Shadows", "year": 2014, "rating": 7.7, "genres": "Comedy, Horror"},
            {"title": "In Bruges", "year": 2008, "rating": 7.9, "genres": "Comedy, Crime, Drama"},
            {"title": "Airplane!", "year": 1980, "rating": 7.7, "genres": "Comedy"},
            {"title": "Snatch", "year": 2000, "rating": 8.2, "genres": "Comedy, Crime"},
            {"title": "The Nice Guys", "year": 2016, "rating": 7.4, "genres": "Action, Comedy, Crime"},
            {"title": "Ferris Bueller's Day Off", "year": 1986, "rating": 7.8, "genres": "Comedy"},
            {"title": "Mean Girls", "year": 2004, "rating": 7.1, "genres": "Comedy"},
            {"title": "Tropic Thunder", "year": 2008, "rating": 7.1, "genres": "Action, Comedy"},
            {"title": "21 Jump Street", "year": 2012, "rating": 7.2, "genres": "Action, Comedy, Crime"},
            {"title": "Crazy, Stupid, Love.", "year": 2011, "rating": 7.4, "genres": "Comedy, Drama, Romance"},
            {"title": "Anchorman: The Legend of Ron Burgundy", "year": 2004, "rating": 7.1, "genres": "Comedy"},
            {"title": "Knives Out", "year": 2019, "rating": 7.9, "genres": "Comedy, Crime, Drama"},
            {"title": "School of Rock", "year": 2003, "rating": 7.2, "genres": "Comedy, Music"},
            {"title": "Modern Times", "year": 1936, "rating": 8.5, "genres": "Comedy, Drama"},
            {"title": "City Lights", "year": 1931, "rating": 8.5, "genres": "Comedy, Drama, Romance"},
            {"title": "Little Miss Sunshine", "year": 2006, "rating": 7.8, "genres": "Comedy, Drama"},
            {"title": "The Hangover", "year": 2009, "rating": 7.7, "genres": "Comedy"}
        ]
    },
    "long-films": {
        "id": "long-films",
        "title": "Long Films That Earn Their Runtime",
        "short_desc": "Films over two and a half hours that use every minute — for a weekend afternoon with nothing else booked.",
        "badge": "24 FILMS",
        "tagline": "Expansive canvases, profound emotional payoffs, and immersive world-building.",
        "editorial": (
            "A bloated movie can feel like an eternity. But when an epic film truly justifies its massive length, "
            "it becomes an unforgettable journey that completely transports you. Settle into the sofa with your favorite snack — "
            "these twenty-four titles make every single minute count."
        ),
        "movies": [
            {"title": "The Lord of the Rings: The Fellowship of the Ring", "year": 2001, "rating": 8.9, "genres": "Action, Adventure, Drama"},
            {"title": "The Lord of the Rings: The Return of the King", "year": 2003, "rating": 9.0, "genres": "Action, Adventure, Drama"},
            {"title": "The Godfather", "year": 1972, "rating": 9.2, "genres": "Crime, Drama"},
            {"title": "The Godfather Part II", "year": 1974, "rating": 9.0, "genres": "Crime, Drama"},
            {"title": "Interstellar", "year": 2014, "rating": 8.6, "genres": "Adventure, Drama, Sci-Fi"},
            {"title": "Oppenheimer", "year": 2023, "rating": 8.9, "genres": "Biography, Drama, History"},
            {"title": "The Wolf of Wall Street", "year": 2013, "rating": 8.2, "genres": "Biography, Comedy, Crime"},
            {"title": "Avengers: Endgame", "year": 2019, "rating": 8.4, "genres": "Action, Adventure, Drama"},
            {"title": "Once Upon a Time in Hollywood", "year": 2019, "rating": 7.6, "genres": "Comedy, Drama"},
            {"title": "The Green Mile", "year": 1999, "rating": 8.6, "genres": "Crime, Drama, Fantasy"},
            {"title": "Heat", "year": 1995, "rating": 8.3, "genres": "Action, Crime, Drama"},
            {"title": "Django Unchained", "year": 2012, "rating": 8.5, "genres": "Drama, Western"},
            {"title": "Casino", "year": 1995, "rating": 8.2, "genres": "Crime, Drama"},
            {"title": "Braveheart", "year": 1995, "rating": 8.4, "genres": "Biography, Drama, History"},
            {"title": "Gladiator", "year": 2000, "rating": 8.5, "genres": "Action, Adventure, Drama"},
            {"title": "Schindler's List", "year": 1993, "rating": 9.0, "genres": "Biography, Drama, History"},
            {"title": "Zodiac", "year": 2007, "rating": 7.7, "genres": "Crime, Drama, Mystery"},
            {"title": "Titanic", "year": 1997, "rating": 7.9, "genres": "Drama, Romance"},
            {"title": "The Batman", "year": 2022, "rating": 7.8, "genres": "Action, Crime, Drama"},
            {"title": "Dune: Part Two", "year": 2024, "rating": 8.5, "genres": "Action, Adventure, Sci-Fi"},
            {"title": "There Will Be Blood", "year": 2007, "rating": 8.2, "genres": "Drama"},
            {"title": "Blade Runner 2049", "year": 2017, "rating": 8.0, "genres": "Action, Drama, Sci-Fi"},
            {"title": "Seven Samurai", "year": 1954, "rating": 8.6, "genres": "Action, Drama"},
            {"title": "Lawrence of Arabia", "year": 1962, "rating": 8.3, "genres": "Adventure, Biography, Drama"}
        ]
    },
    "flops-deserved-better": {
        "id": "flops-deserved-better",
        "title": "Box Office Flops That Deserved Better",
        "short_desc": "Films that lost money in cinemas but rate well with audiences who found them later — the gap between commercial failure and actual quality.",
        "badge": "24 FILMS",
        "tagline": "Box office receipts measure marketing budgets, not artistic greatness.",
        "editorial": (
            "Studios often panic when a film doesn't recoup its production budget during its opening weekend. "
            "Yet history repeatedly proves that box office receipts measure distribution timing and marketing spend, "
            "not artistic worth. These twenty-four films bombed at the ticket counter, only to become beloved, enduring cultural touchstones."
        ),
        "movies": [
            {"title": "The Shawshank Redemption", "year": 1994, "rating": 9.3, "genres": "Drama"},
            {"title": "Fight Club", "year": 1999, "rating": 8.8, "genres": "Drama"},
            {"title": "Blade Runner", "year": 1982, "rating": 8.1, "genres": "Action, Drama, Sci-Fi"},
            {"title": "The Iron Giant", "year": 1999, "rating": 8.0, "genres": "Animation, Action, Adventure"},
            {"title": "Children of Men", "year": 2006, "rating": 7.9, "genres": "Action, Drama, Sci-Fi"},
            {"title": "Donnie Darko", "year": 2001, "rating": 8.0, "genres": "Drama, Mystery, Sci-Fi"},
            {"title": "The Big Lebowski", "year": 1998, "rating": 8.1, "genres": "Comedy, Crime"},
            {"title": "Office Space", "year": 1999, "rating": 7.7, "genres": "Comedy"},
            {"title": "Scott Pilgrim vs. the World", "year": 2010, "rating": 7.5, "genres": "Action, Comedy, Fantasy"},
            {"title": "Dredd", "year": 2012, "rating": 7.1, "genres": "Action, Sci-Fi"},
            {"title": "The Nice Guys", "year": 2016, "rating": 7.4, "genres": "Action, Comedy, Crime"},
            {"title": "Annihilation", "year": 2018, "rating": 6.8, "genres": "Adventure, Drama, Horror"},
            {"title": "Almost Famous", "year": 2000, "rating": 7.9, "genres": "Adventure, Comedy, Drama"},
            {"title": "Treasure Planet", "year": 2002, "rating": 7.2, "genres": "Animation, Adventure, Family"},
            {"title": "Hugo", "year": 2011, "rating": 7.5, "genres": "Drama, Family, Fantasy"},
            {"title": "The Master", "year": 2012, "rating": 7.2, "genres": "Drama"},
            {"title": "Steve Jobs", "year": 2015, "rating": 7.2, "genres": "Biography, Drama"},
            {"title": "Cloud Atlas", "year": 2012, "rating": 7.4, "genres": "Action, Drama, Mystery"},
            {"title": "Event Horizon", "year": 1997, "rating": 6.7, "genres": "Horror, Sci-Fi"},
            {"title": "Kiss Kiss Bang Bang", "year": 2005, "rating": 7.5, "genres": "Comedy, Crime, Mystery"},
            {"title": "Warrior", "year": 2011, "rating": 8.2, "genres": "Action, Drama, Sport"},
            {"title": "Gattaca", "year": 1997, "rating": 7.8, "genres": "Drama, Sci-Fi, Thriller"},
            {"title": "Silence", "year": 2016, "rating": 7.2, "genres": "Drama, History"},
            {"title": "Popstar: Never Stop Never Stopping", "year": 2016, "rating": 6.7, "genres": "Comedy, Music"}
        ]
    },
    "thrillers-guessing": {
        "id": "thrillers-guessing",
        "title": "Thrillers That Keep You Guessing",
        "short_desc": "Suspense done properly — the best-rated thrillers in our library, from slow-tightening dread to full paranoia.",
        "badge": "24 FILMS",
        "tagline": "Unbearable suspense, psychological warfare, and jaw-dropping twists.",
        "editorial": (
            "A masterwork thriller creates a claustrophobic psychological contract: every shadow is suspicious, "
            "every character has something to hide, and the floor could drop out from beneath you at any second. "
            "These twenty-four selections represent the absolute masters of the craft."
        ),
        "movies": [
            {"title": "Se7en", "year": 1995, "rating": 8.6, "genres": "Crime, Drama, Mystery"},
            {"title": "The Prestige", "year": 2006, "rating": 8.5, "genres": "Drama, Mystery, Sci-Fi"},
            {"title": "Shutter Island", "year": 2010, "rating": 8.2, "genres": "Mystery, Thriller"},
            {"title": "Memento", "year": 2000, "rating": 8.4, "genres": "Mystery, Thriller"},
            {"title": "Gone Girl", "year": 2014, "rating": 8.1, "genres": "Drama, Mystery, Thriller"},
            {"title": "Prisoners", "year": 2013, "rating": 8.1, "genres": "Crime, Drama, Mystery"},
            {"title": "The Sixth Sense", "year": 1999, "rating": 8.2, "genres": "Drama, Mystery, Thriller"},
            {"title": "The Silence of the Lambs", "year": 1991, "rating": 8.6, "genres": "Crime, Drama, Thriller"},
            {"title": "Parasite", "year": 2019, "rating": 8.5, "genres": "Drama, Thriller"},
            {"title": "Zodiac", "year": 2007, "rating": 7.7, "genres": "Crime, Drama, Mystery"},
            {"title": "Oldboy", "year": 2003, "rating": 8.4, "genres": "Action, Drama, Mystery"},
            {"title": "Black Swan", "year": 2010, "rating": 8.0, "genres": "Drama, Thriller"},
            {"title": "Knives Out", "year": 2019, "rating": 7.9, "genres": "Comedy, Crime, Drama"},
            {"title": "Nightcrawler", "year": 2014, "rating": 7.8, "genres": "Crime, Drama, Thriller"},
            {"title": "The Invisible Guest", "year": 2016, "rating": 8.0, "genres": "Crime, Drama, Mystery"},
            {"title": "Get Out", "year": 2017, "rating": 7.7, "genres": "Horror, Mystery, Thriller"},
            {"title": "No Country for Old Men", "year": 2007, "rating": 8.2, "genres": "Crime, Drama, Thriller"},
            {"title": "Sicario", "year": 2015, "rating": 7.6, "genres": "Action, Crime, Drama"},
            {"title": "Coherence", "year": 2013, "rating": 7.2, "genres": "Mystery, Sci-Fi"},
            {"title": "10 Cloverfield Lane", "year": 2016, "rating": 7.2, "genres": "Action, Drama, Horror"},
            {"title": "Wind River", "year": 2017, "rating": 7.7, "genres": "Crime, Drama, Mystery"},
            {"title": "Ex Machina", "year": 2014, "rating": 7.7, "genres": "Drama, Sci-Fi, Thriller"},
            {"title": "A Quiet Place", "year": 2018, "rating": 7.5, "genres": "Drama, Horror, Sci-Fi"},
            {"title": "Misery", "year": 1990, "rating": 7.8, "genres": "Drama, Thriller"}
        ]
    }
}

# Quiz configuration for AI Movie Picker (PickAMovieForMe style)
QUIZ_MOODS = [
    {"label": "⚡ High Adrenaline & Action", "value": "adrenaline", "genres": ["Action", "Adventure", "Thriller"]},
    {"label": "😄 Fun, Laughs & Uplifting", "value": "happy", "genres": ["Comedy", "Animation", "Adventure"]},
    {"label": "🧠 Mind-Bending & Deep", "value": "mindbending", "genres": ["Sci-Fi", "Mystery", "Drama"]},
    {"label": "🍿 Chill & Easy-Going", "value": "chill", "genres": ["Comedy", "Adventure", "Family"]},
    {"label": "🌑 Dark, Gritty & Intense", "value": "dark", "genres": ["Crime", "Thriller", "Drama"]},
    {"label": "❤️ Romantic & Heartfelt", "value": "romance", "genres": ["Romance", "Drama", "Comedy"]},
    {"label": "😱 Spooky & Suspenseful", "value": "spooky", "genres": ["Horror", "Mystery", "Thriller"]}
]

QUIZ_OCCASIONS = [
    {"label": "👤 Solo Night (Total Immersion)", "value": "solo"},
    {"label": "💑 Movie Date Night", "value": "date"},
    {"label": "🍻 Friends & Popcorn", "value": "friends"},
    {"label": "👨‍👩‍👧‍👦 Family & Kids Night", "value": "family"}
]

QUIZ_SPECIAL_THEMES = [
    "🎲 Surprise Me (Any Theme)",
    "🚀 Space & Sci-Fi Oddities",
    "💰 Heists & Elaborate Robberies",
    "🧠 Mind-Bending Twists",
    "📖 Based on True Stories",
    "🏆 Highest-Rated Community Picks",
    "🏎️ Fast Cars & High Speed",
    "🕵️ Hard-Boiled Detective & Noir"
]

QUIZ_ERAS = [
    "Any Era",
    "Modern Cinema (2015 - 2024)",
    "The 2000s Peak (2000 - 2014)",
    "90s Golden Era (1990 - 1999)",
    "Vintage Classics (Pre-1990)"
]
