from flask import Flask,request
from server.recommendation_pickle import recommendationPickle
from server.data_operations import operations
import json


app = Flask(__name__)

@app.route("/")
def index():
    return "mySquareMealServer ... !!!"

@app.route("/recommendation",methods=['POST','GET'])
def getRecommendation():
    lat = request.args.get("latitude")
    long = request.args.get("longitude")
    city = request.args.get("city")
    print(lat,long,city)
    nearby_restaurants = operations.get_nearby(lat=lat,long=long,city=city)
    menu_api, menu_list = operations.get_menu_items(nearby_restaurants)

    result_api_list = recommendationPickle.get_recommendation_from_pickle(menu_api, menu_list)
    result = operations.get_result_data(result_api_list,city)
    return json.dumps(result)

if __name__=='__main__':
    app.run(debug=True)
    #data_operations_object = operations()
    #pickle_object = recommendationPickle()
