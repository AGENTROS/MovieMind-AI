import os
import json
import urllib.parse
import requests

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'tmdb_cache.json')
ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

def load_env_vars():
    """Load variables from .env file if available."""
    env = {}
    if os.path.exists(ENV_FILE):
        try:
            with open(ENV_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        env[k.strip()] = v.strip()
        except Exception:
            pass
    return env

_env_vars = load_env_vars()

DEFAULT_API_KEY = _env_vars.get('TMDB_API_KEY', os.environ.get('TMDB_API_KEY', ''))
DEFAULT_TOKEN = _env_vars.get('TMDB_READ_ACCESS_TOKEN', os.environ.get('TMDB_READ_ACCESS_TOKEN', ''))
TMDB_BASE_URLS = ['https://api.tmdb.org/3', 'https://api.themoviedb.org/3']

# Curated High-Definition Posters & Backdrops for instant zero-latency loading
CURATED_POSTERS = {
    "dune: part two": {
        "poster_path": "https://image.tmdb.org/t/p/w500/8b8R8l88Qje9dn9OE8PY05Nxl1X.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/xOMo8BRK7PfcJv9JCnx7s520b4a.jpg",
        "overview": "Follow the mythic journey of Paul Atreides as he unites with Chani and the Fremen while on a path of revenge against the conspirators who destroyed his family.",
        "vote_average": 8.5,
        "release_date": "2024-03-01",
        "trailer_url": "https://www.youtube.com/watch?v=Way9Dexny3w"
    },
    "deadpool & wolverine": {
        "poster_path": "https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/yDHYTjA3R0ne84guT43Q57ZOxZf.jpg",
        "overview": "A listless Wade Wilson toils away in civilian life with his days as the morally flexible mercenary Deadpool behind him.",
        "vote_average": 7.8,
        "release_date": "2024-07-26",
        "trailer_url": "https://www.youtube.com/watch?v=73_1biulkYk"
    },
    "inside out 2": {
        "poster_path": "https://image.tmdb.org/t/p/w500/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/stKGOmPAgpnQzU21wAaupFsI81e.jpg",
        "overview": "Teenager Riley's mind headquarters is undergoing a sudden demolition to make room for unexpected emotions.",
        "vote_average": 7.6,
        "release_date": "2024-06-14",
        "trailer_url": "https://www.youtube.com/watch?v=LEjhY15eCx0"
    },
    "a quiet place: day one": {
        "poster_path": "https://image.tmdb.org/t/p/w500/yrpPYK2qm969CuEN79pFiAV9v5f.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/2RVcJbWFmICRDs7RI89GZKsTXLQ.jpg",
        "overview": "As New York City is invaded by alien creatures who hunt by sound, a woman named Sam must fight to survive.",
        "vote_average": 7.5,
        "release_date": "2024-06-28",
        "trailer_url": "https://www.youtube.com/watch?v=YPY7J-flzE8"
    },
    "kingdom of the planet of the apes": {
        "poster_path": "https://image.tmdb.org/t/p/w500/gKkl37BQuKTanygYQG1pyYgLVgf.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/fqv8v6AycXKsivp1T5yKtLbGXce.jpg",
        "overview": "Several generations in the future following Caesar's reign, apes are now the dominant species and live harmoniously while humans have been reduced to living in the shadows.",
        "vote_average": 7.4,
        "release_date": "2024-05-10",
        "trailer_url": "https://www.youtube.com/watch?v=Kdr5oedn7q8"
    },
    "the fall guy": {
        "poster_path": "https://image.tmdb.org/t/p/w500/tSz1qsmS9Soio7zAZOCv5jt20hv.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/H5HqqQgLTsvTzp4v4ppZ6nm6eh.jpg",
        "overview": "Fresh off an almost career-ending accident, stuntman Colt Seavers has to track down a missing movie star.",
        "vote_average": 7.1,
        "release_date": "2024-05-03",
        "trailer_url": "https://www.youtube.com/watch?v=j7jPnwVGdZ8"
    },
    "furiosa: a mad max saga": {
        "poster_path": "https://image.tmdb.org/t/p/w500/iADOJ8Zymht2JPMoy3R7xceZprc.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/wNAhuOZ3Zf84jCI5TeTVlY5Fe39.jpg",
        "overview": "As the world fell, young Furiosa is snatched from the Green Place of Many Mothers and falls into the hands of a great Biker Horde led by the Warlord Dementus.",
        "vote_average": 7.8,
        "release_date": "2024-05-24",
        "trailer_url": "https://www.youtube.com/watch?v=XJMuhwVlca4"
    },
    "godzilla x kong: the new empire": {
        "poster_path": "https://image.tmdb.org/t/p/w500/z1p34vh7dEOnLDmyCrlUVLuoDzd.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/xRd1eJIDc7DLAgMVuv4qb50YFm5.jpg",
        "overview": "Following their explosive showdown, Godzilla and Kong must reunite against a colossal undiscovered threat hidden within our world.",
        "vote_average": 6.8,
        "release_date": "2024-03-29",
        "trailer_url": "https://www.youtube.com/watch?v=lV1OOlGwExg"
    },
    "interstellar": {
        "poster_path": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/xJHokMbljvjADYdit5fK5VQsXEG.jpg",
        "overview": "The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage.",
        "vote_average": 8.6,
        "release_date": "2014-11-05",
        "trailer_url": "https://www.youtube.com/watch?v=zSWdZVtXT7E"
    },
    "inception": {
        "poster_path": "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/8ZTVqvKDQ8emSGUEMjsS4yHAwrp.jpg",
        "overview": "Cobb, a skilled thief who steals corporate secrets through dream-sharing technology, is given the inverse task of planting an idea into the mind of a C.E.O.",
        "vote_average": 8.8,
        "release_date": "2010-07-16",
        "trailer_url": "https://www.youtube.com/watch?v=YoHD9XEInc0"
    },
    "the dark knight": {
        "poster_path": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/hkBaDkMWbLaf8B1lsWsKX7Ew3Xq.jpg",
        "overview": "Batman raises the stakes in his war on crime with the help of Lt. Jim Gordon and District Attorney Harvey Dent, but faces a psychopathic criminal mastermind known as The Joker.",
        "vote_average": 9.0,
        "release_date": "2008-07-18",
        "trailer_url": "https://www.youtube.com/watch?v=EXeTwQWrcwY"
    },
    "dark knight, the": {
        "poster_path": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/hkBaDkMWbLaf8B1lsWsKX7Ew3Xq.jpg",
        "overview": "Batman raises the stakes in his war on crime with the help of Lt. Jim Gordon and District Attorney Harvey Dent.",
        "vote_average": 9.0,
        "release_date": "2008-07-18",
        "trailer_url": "https://www.youtube.com/watch?v=EXeTwQWrcwY"
    },
    "the martian": {
        "poster_path": "https://image.tmdb.org/t/p/w500/5BHuvQ6p9kL09NM29MmgiFDjYjr.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/w03QjPkWvj9Uolp3s5R29NnI9P.jpg",
        "overview": "An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive.",
        "vote_average": 8.0,
        "release_date": "2015-10-02",
        "trailer_url": "https://www.youtube.com/watch?v=ej3ioOneTy8"
    },
    "martian, the": {
        "poster_path": "https://image.tmdb.org/t/p/w500/5BHuvQ6p9kL09NM29MmgiFDjYjr.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/w03QjPkWvj9Uolp3s5R29NnI9P.jpg",
        "overview": "An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive.",
        "vote_average": 8.0,
        "release_date": "2015-10-02",
        "trailer_url": "https://www.youtube.com/watch?v=ej3ioOneTy8"
    },
    "fight club": {
        "poster_path": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/hZkgoQYus5vegHoetLkCJzb17zJ.jpg",
        "overview": "A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy.",
        "vote_average": 8.4,
        "release_date": "1999-10-15",
        "trailer_url": "https://www.youtube.com/watch?v=qtRKdV9eiG4"
    },
    "pulp fiction": {
        "poster_path": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/suaEOtk1916guXlZTTC439F57bC.jpg",
        "overview": "A burger-loving hit man, his philosophical partner, a drug-addled gangster's moll and a washed-up boxer converge in four tales of violence and redemption.",
        "vote_average": 8.5,
        "release_date": "1994-09-10",
        "trailer_url": "https://www.youtube.com/watch?v=s7EdQ4FqbhY"
    },
    "toy story": {
        "poster_path": "https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/lxD5ak7BOxMg9XY2yXWqUj5k7cT.jpg",
        "overview": "Led by Woody, Andy's toys live happily in his room until Andy's birthday brings Buzz Lightyear onto the scene.",
        "vote_average": 8.0,
        "release_date": "1995-10-30",
        "trailer_url": "https://www.youtube.com/watch?v=v-PjgYDrg70"
    }
}

class TMDBClient:
    def __init__(self, api_key=None, read_token=None):
        self.api_key = api_key or DEFAULT_API_KEY
        self.read_token = read_token or DEFAULT_TOKEN
        self.cache = self._load_cache()
        self._mem_cache = dict(self.cache)
        self.session = requests.Session()
        self._save_counter = 0

    def set_api_key(self, api_key, read_token=None):
        """Update TMDB API key dynamically."""
        self.api_key = api_key.strip() if api_key else ''
        if read_token:
            self.read_token = read_token.strip()

    def _load_cache(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        try:
            os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f)
        except Exception:
            pass

    def _fetch_from_tmdb(self, endpoint, params=None):
        """Perform request to TMDB API using api.tmdb.org (with fallback)."""
        if not params:
            params = {}
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        if self.read_token:
            headers['Authorization'] = f'Bearer {self.read_token}'
        if self.api_key:
            if self.read_token:
                headers['Authorization'] = f'Bearer {self.read_token}'
            params['api_key'] = self.api_key

        if self.read_token:
            headers['Authorization'] = f'Bearer {self.read_token}'

        for base_url in TMDB_BASE_URLS:
            try:
                url = f"{base_url}/{endpoint.lstrip('/')}"
                resp = self.session.get(url, params=params, headers=headers, timeout=5)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                continue
        return None

    def discover_movies(self, page=1, sort_by="popularity.desc", filters=None):
        """Return one page of live TMDB discovery results."""
        if not self.api_key and not self.read_token:
            raise RuntimeError("A TMDB API key or read token is required for live discovery.")

        params = dict(filters or {})
        params.update({"page": max(1, min(int(page), 500)), "sort_by": sort_by})
        data = self._fetch_from_tmdb("discover/movie", params=params)
        if not data or not isinstance(data.get("results"), list):
            raise RuntimeError("TMDB movie discovery failed. Check the API connection and try again.")
        return data

    def search_movies(self, query, page=1):
        """Search the live TMDB catalog by title or keyword."""
        if not self.api_key and not self.read_token:
            raise RuntimeError("A TMDB API key or read token is required for live search.")
        data = self._fetch_from_tmdb(
            "search/movie",
            params={"query": query, "page": max(1, min(int(page), 500))},
        )
        if not data or not isinstance(data.get("results"), list):
            raise RuntimeError("TMDB movie search failed. Check the API connection and try again.")
        return data

    def get_movie_details(self, tmdb_id=None, title=None, year=None, include_extras=True, refresh=False):
        """
        Fetch details for a movie.
        Checks memory cache -> disk cache -> curated dictionary -> live TMDB API -> dynamic fallback.
        """
        cache_key = f"{tmdb_id}_{title}".lower().strip()
        
        # 1. Check in-memory cache for instant 0ms return
        if not refresh and cache_key in self._mem_cache:
            entry = self._mem_cache[cache_key]
            if entry.get('poster_path') and 'image.tmdb.org' in entry.get('poster_path', ''):
                return entry

        # 2. Check disk cache if valid
        if not refresh and cache_key in self.cache:
            entry = self.cache[cache_key]
            if entry.get('poster_path') and 'image.tmdb.org' in entry.get('poster_path', ''):
                self._mem_cache[cache_key] = entry
                return entry

        # 3. Check curated list
        clean_title = (title or '').lower().strip()
        for k, v in CURATED_POSTERS.items():
            if not refresh and (k == clean_title or k in clean_title):
                res = v.copy()
                res['title'] = title
                self.cache[cache_key] = res
                self._mem_cache[cache_key] = res
                return res

        # 4. Live TMDB API Fetching
        if self.api_key or self.read_token:
            data = None
            if tmdb_id and int(tmdb_id) > 0:
                params = {'append_to_response': 'videos,credits'} if include_extras else {}
                data = self._fetch_from_tmdb(f"movie/{tmdb_id}", params=params)

            if not data and title:
                search_params = {'query': title}
                if year:
                    search_params['year'] = year
                search_data = self._fetch_from_tmdb("search/movie", params=search_params)
                if search_data and search_data.get('results'):
                    first_hit = search_data['results'][0]
                    hit_id = first_hit.get('id')
                    if hit_id:
                        params = {'append_to_response': 'videos,credits'} if include_extras else {}
                        data = self._fetch_from_tmdb(f"movie/{hit_id}", params=params)
                    if not data:
                        data = first_hit

            if data:
                poster_path = data.get('poster_path')
                backdrop_path = data.get('backdrop_path')
                
                poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                backdrop = f"https://image.tmdb.org/t/p/w1280{backdrop_path}" if backdrop_path else None

                trailer_url = None
                videos = data.get('videos', {}).get('results', [])
                for vid in videos:
                    if vid.get('site') == 'YouTube' and vid.get('type') in ['Trailer', 'Teaser']:
                        trailer_url = f"https://www.youtube.com/watch?v={vid.get('key')}"
                        break

                if not trailer_url and title:
                    trailer_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(title + ' official trailer')}"

                res = {
                    "title": data.get('title', title),
                    "poster_path": poster or f"https://placehold.co/500x750/0b0f19/3b82f6?text={urllib.parse.quote((title or 'Movie')[:25])}&font=roboto",
                    "backdrop_path": backdrop or "https://image.tmdb.org/t/p/w1280/xJHokMbljvjADYdit5fK5VQsXEG.jpg",
                    "overview": data.get('overview') or "A critically acclaimed film discovered through machine learning collaborative and content-based similarity patterns.",
                    "vote_average": round(float(data.get('vote_average', 7.5)), 1),
                    "release_date": data.get('release_date') or str(year or ''),
                    "trailer_url": trailer_url,
                    "runtime": data.get('runtime'),
                    "imdb_id": data.get('imdb_id'),
                    "genres": [genre.get('name', '') for genre in data.get('genres', [])]
                }
                self.cache[cache_key] = res
                self._mem_cache[cache_key] = res
                self._save_counter += 1
                if self._save_counter % 5 == 0:
                    self._save_cache()
                return res

        # 5. Dynamic fallback poster
        colors = ["3B82F6", "8B5CF6", "EC4899", "10B981", "F59E0B", "6366F1", "06B6D4"]
        seed = sum(ord(c) for c in (title or "Movie")) % len(colors)
        color = colors[seed]
        
        display_title = urllib.parse.quote((title or 'Movie')[:25])
        fallback_poster = f"https://placehold.co/500x750/0b0f19/{color}?text={display_title}&font=roboto"
        fallback_backdrop = f"https://placehold.co/1280x720/0b0f19/{color}?text={display_title}&font=roboto"

        res = {
            "title": title,
            "poster_path": fallback_poster,
            "backdrop_path": fallback_backdrop,
            "overview": "An acclaimed cinematic story discovered and recommended through machine learning similarity patterns.",
            "vote_average": 7.5,
            "release_date": str(year) if year else "N/A",
            "trailer_url": f"https://www.youtube.com/results?search_query={urllib.parse.quote((title or '') + ' trailer')}"
        }
        self.cache[cache_key] = res
        self._mem_cache[cache_key] = res
        return res

    def get_batch_movie_details(self, movies_list):
        """Fetch details for a list of movie objects concurrently."""
        from concurrent.futures import ThreadPoolExecutor
        def _fetch_one(m):
            t = m.get('clean_title', m.get('title', 'Movie'))
            y = m.get('year')
            mid = m.get('tmdbId') or m.get('tmdb_id', 0)
            # Carousel cards only need artwork and basic metadata. Avoid
            # fetching videos/credits until the user opens movie details.
            return self.get_movie_details(tmdb_id=mid, title=t, year=y, include_extras=False)
        with ThreadPoolExecutor(max_workers=8) as ex:
            return list(ex.map(_fetch_one, movies_list))

tmdb_client = TMDBClient()
