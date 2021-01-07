from config import db


class MovieName(db.Model):
    __tablename__ = "user_recommend_movie"
    userId = db.Column(db.BIGINT)
    movieName = db.Column(db.String(255))
    rating = db.Column(db.Float)
    id = db.Column(db.BIGINT, primary_key=True)
    movieId = db.Column(db.BIGINT)


class Ratings(db.Model):
    __tablename__ = "ratings"
    userId = db.Column(db.Integer)
    movieId = db.Column(db.Integer)
    rating = db.Column(db.Float)
    timestamp = db.Column(db.Integer, primary_key=True)


class Ranking(db.Model):
    __tablename__ = "movie_average_rating"
    movieId = db.Column(db.BIGINT)
    movieName = db.Column(db.String(255))
    average_rating = db.Column(db.Float)
    id = db.Column(db.BIGINT, primary_key=True)


class Movies(db.Model):
    __tablename__ = "movies"
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    genres = db.Column(db.String(255))
