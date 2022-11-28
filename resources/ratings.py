from flask_restful import Resource, reqparse
from models.rating import RatingModel
from flask_jwt_extended import jwt_required

class Ratings(Resource):
    def get(self):
        return {'ratings' : [rating.json() for rating in RatingModel.query.all()]}


class Rating(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('description', type=str, required=True, help="description is required")
    minha_requisicao.add_argument('rating', type=int, required=True, help='rating is required')
    minha_requisicao.add_argument('rating_id')

    @jwt_required()
    def get(self, id):
        rating = RatingModel.find_rating_by_id(id)
        if rating: #if rating is not None
            return rating.json()
        return {'message':'rating not found'}, 200 # or 204

    @jwt_required()
    def post(self, id):
        rating_id = RatingModel.find_last_rating()
        dados = Rating.minha_requisicao.parse_args()
        new_rating = RatingModel(rating_id, **dados)
        
        try:
            new_rating.save_rating()
        except:
            return {'message':'An internal error ocurred.'}, 500

        return new_rating.json(), 201

    def put(self, id):
        dados = Rating.minha_requisicao.parse_args()
        rating = RatingModel.find_rating_by_id(id)
        if rating:
            rating.update_rating(**dados)
            rating.save_rating()
            return rating.json(), 200

        rating_id = RatingModel.find_last_rating()
        new_rating = RatingModel(rating_id, **dados)
        new_rating.save_rating()
        return new_rating.json(), 201

    def delete(self, id):
        rating = RatingModel.find_rating_by_id(id)
        if rating:
            rating.delete_rating()
            return {'message' : 'rating deleted.'}
        return {'message' : 'rating not founded'}, 204