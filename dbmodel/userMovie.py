from config import db


class MovieName(db.Model):
    __tablename__ = "user_recommend_movie"
    userId = db.Column(db.BIGINT)
    movieName = db.Column(db.String(255))
    rating = db.Column(db.Float)
    id = db.Column(db.BIGINT, primary_key=True)


class Ratings(db.Model):
    __tablename__ = "ratings"
    userId = db.Column(db.Integer)
    movieId = db.Column(db.Integer)
    rating = db.Column(db.Float)
    timestamp = db.Column(db.Integer, primary_key=True)
