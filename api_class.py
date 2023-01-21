import requests


class SearchMovie:
    def __init__(self):
        self.search_api = "https://api.themoviedb.org/3/search/movie?"
        self.api_key = "6fa4185b4ed9c711e2dd54ef6d28061b"
        self.movie_api = "https://api.themoviedb.org/3/movie/"

    def get_movies(self, movie_name):
        respond = requests.get(
            url=self.search_api,
            params={
                "api_key": self.api_key,
                "query": movie_name
            }
        )
        desired_data = respond.json()["results"]
        return desired_data

    def current_movie(self, movie_id):
        respond = requests.get(
            url=f"{self.movie_api}{int(movie_id)}?",
            params={
                "api_key": self.api_key,
                "language": "en-US"
            }
        )
        data = respond.json()
        current_movie = {
            "title": data["title"],
            "year": int(data["release_date"].split("-")[0]),
            "description": data["overview"],
            "img_uri": f'https://image.tmdb.org/t/p/w500{data["poster_path"]}'
        }
        return current_movie
