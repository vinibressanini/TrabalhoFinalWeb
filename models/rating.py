from sql_alchemy import database
from sqlalchemy.sql.expression import func


class RatingModel (database.Model):
    
    __tablename__ = 'rating'
    rating_id = database.Column(database.Integer, primary_key = True)
    description = database.Column(database.String(255))
    movie_id = database.Column(database.Integer)
    rating = database.Column(database.Integer)

    def __init__(self, rating_id, movie_id, description, rating):
        self.rating_id = rating_id
        self.movie_id = movie_id
        self.description = description
        self.rating = rating

    def json(self):
        return {'rating_id' : self.rating_id,
        'movie_id' : self.movie_id,
        'description' : self.description,
        'rating' : self.rating}

    @classmethod  
    def find_rating_by_id(cls, rating_id): 
        rating = cls.query.filter_by(rating_id = rating_id).first()
        if rating:
            return rating
        return None

    def save_rating(self): 
        database.session.add(self)
        database.session.commit()

    def update_rating(self, rating_id, movie_id, description, rating): 
        self.rating_id = rating_id
        self.movie_id = movie_id
        self.description = description
        self.rating = rating

    def delete_rating(self): 
        database.session.delete(self)
        database.session.commit()
        
    @classmethod
    def find_last_rating(cls):
        # rating_id = database.engine.execute("select nextval('rating_id') as new_id").fetchone() - postgres
        rating_id = database.session.query(func.max(cls.rating_id)).one()[0]

        if rating_id:
            return rating_id + 1
        return 1