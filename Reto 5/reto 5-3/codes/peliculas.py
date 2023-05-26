from mrjob.job import MRJob


class PeliculaVistaRating(MRJob):
    def mapper(self, _, line):
        usuario, movie, rating, genre, date = line.split(",")
        if usuario != "Usuario":
            yield usuario, (movie, float(rating))

    def reducer(self, usuario, data):
        ratings = list(data)
        num_movies = len(ratings)
        avg_rating = sum(r for _, r in ratings) / num_movies
        yield usuario, [num_movies, avg_rating]


class DiaVistas(MRJob):
    def mapper(self, _, line):
        usuario, movie, rating, genre, date = line.split(",")
        if usuario != "Usuario":
            yield None, (date, movie)

    def reducer(self, _, data):
        movie_counts = {}
        for date, movie in data:
            if date not in movie_counts:
                movie_counts[date] = 0
            movie_counts[date] += 1
        max_date, max_count = max(movie_counts.items(), key=lambda x: x[1])
        min_date, min_count = min(movie_counts.items(), key=lambda x: x[1])
        yield max_date, max_count
        yield min_date, min_count


class UsuarioVistaRating(MRJob):
    def mapper(self, _, line):
        usuario, movie, rating, genre, date = line.split(",")
        if usuario != "Usuario":
            yield movie, (usuario, float(rating))

    def reducer(self, movie, data):
        ratings = list(data)
        num_users = len(ratings)
        avg_rating = sum(r for _, r in ratings) / num_users
        yield movie, [num_users, avg_rating]


class DiaRating(MRJob):
    def mapper(self, _, line):
        usuario, movie, rating, genre, date = line.split(",")
        if usuario != "Usuario":
            yield None, (date, float(rating))

    def reducer(self, _, data):
        ratings = list(data)
        date_ratings = {}
        for date, rating in ratings:
            if date not in date_ratings:
                date_ratings[date] = []
            date_ratings[date].append(rating)
        max_date, max_avg = max(date_ratings.items(), key=lambda x: sum(x[1]) / len(x[1]))
        min_date, min_avg = min(date_ratings.items(), key=lambda x: sum(x[1]) / len(x[1]))
        yield max_date, sum(max_avg) / len(max_avg)
        yield min_date, sum(min_avg) / len(min_avg)


class GeneroRating(MRJob):
    def mapper(self, _, line):
        usuario, movie, rating, genre, date = line.split(",")
        if usuario != "Usuario":
            yield genre, (movie, float(rating))

    def reducer(self, genre, data):
        ratings = list(data)
        genre_ratings = {}
        for movie, rating in ratings:
            if movie not in genre_ratings:
                genre_ratings[movie] = []
            genre_ratings[movie].append(rating)
        max_movie, _ = max(genre_ratings.items(), key=lambda x: sum(x[1]) / len(x[1]))
        min_movie, _ = min(genre_ratings.items(), key=lambda x: sum(x[1]) / len(x[1]))
        yield genre, max_movie
        yield genre, min_movie


if __name__ == "__main__":
    jobs = [
        ("Peliculas vistas y rating promedio por usuario", PeliculaVistaRating),
        ("Dia con más y menos películas vistas", DiaVistas),
        ("Vistas por película y rating promedio de ella", UsuarioVistaRating),
        ("Dia con mayor y menor rating", DiaRating),
        ("Película con mayor y menor rating por género", GeneroRating)
    ]

    for job_name, job_class in jobs:
        print(f">>>>>>>>>> {job_name}")
        job = job_class()
        with job.make_runner() as runner:
            runner.run()
            for key, value in job.parse_output(runner.cat_output()):
                print(f"{key}: {value}")
