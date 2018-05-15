from flask import Flask,request
from server.recommendation_pickle import recommendationPickle
from server.data_operations import operations
from server.reverse_geocoding import city_name
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)
MENU_API_LIST=[]

@app.route("/")
def index():
    return "mySquareMealServer ... !!!"

@app.route("/recommendation",methods=['POST','GET'])
def getRecommendation():
    #lat = request.args.get("latitude")
    #long = request.args.get("longitude")
    request_data = request.get_json()
    email=request_data.get('email')
    lat=request_data.get('latitude')
    long=request_data.get('longitude')
    city = city_name.get_city_name(lat,long)
    print(lat,long,city)
    check_city = operations.check_city_list(city=city)
    print("City Present in DB: "+str(check_city))
    print("email: "+email)
    if check_city:
        nearby_restaurants = operations.get_nearby(lat=lat,long=long,city=city)
        menu_api, menu_list = operations.get_menu_items(nearby_restaurants)
        list_of_apis, list_of_menus = operations.filter_for_user_allergies(email,menu_api, menu_list)
        print(len(list_of_apis))
        result_api_list = recommendationPickle.get_recommendation_from_pickle(list_of_apis, list_of_menus)
        MENU_API_LIST = result_api_list
        result = operations.get_result_data(result_api_list,city)
        return json.dumps(result)
    else:
        return "city not found in database"


@app.route("/nutrition-recommendation",methods=['GET'])
def getNutritionInfo():
    print(MENU_API_LIST)
    return "success"


if __name__=='__main__':
    app.run(debug=True, port=8001)
    #data_operations_object = operations()
    #pickle_object = recommendationPickle()