from pymongo import MongoClient
from server.recommendation_pickle import recommendationPickle
import pandas as pd
from geopy.distance import great_circle
import time
start = time.time()

MONGODB_URI = "mongodb://mySquareMeal:mysquaremeal@ds239009.mlab.com:39009/eat_street_bay_area"
client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database("eat_street_bay_area")


MONGODB_URI_USER_PROFILE = "mongodb://mySquareMeal:mySquareMeal@ds157653.mlab.com:57653/mysquaremeal_user_profile_database"
client_user_profile = MongoClient(MONGODB_URI_USER_PROFILE, connectTimeoutMS=30000)
db_profile = client_user_profile.get_database("mysquaremeal_user_profile_database")

class operations:

    def check_city_list(city):

        city_list = ['Concord', 'Cupertino', 'San Francisco', 'San Ramon', 'Union City', 'Palo Alto', 'Newark', 'San Carlos',
         'San Bruno', 'San Mateo', 'Antioch', 'Oakland', 'El Cerrito', 'Menlo Park', 'Sunnyvale', 'Sausalito',
         'Walnut Creek', 'San Rafael', 'Campbell', 'South San Francisco', 'Mountain View', 'Fremont', 'Milpitas',
         'San Pablo', 'San Jose', 'Alameda', 'Sacramento', 'Rancho Cordova', 'Santa Clara', 'Pleasanton', 'Dublin',
         'Hayward', 'Lodi', 'San Leandro', 'Livermore', 'Folsom', 'Roseville', 'Citrus Heights', 'Santa Rosa',
         'Richmond', 'Daly City', 'Belmont', 'Rocklin', 'Novato', 'Berkeley', 'Albany', 'Rohnert Park',
         'Point Richmond', 'Petaluma', 'Hercules', 'Redwood City', 'Sunny Vale', 'Foster City', 'San Lorenzo',
         'Burlingame', 'Danville', 'Vallejo', 'Sonora', 'Elk Grove', 'Brisbane', 'Millbrae', 'Pacific Grove', 'Davis',
         'Oakland,', 'Tiburon', 'Lockeford', 'Emeryville', 'Santa Cruz', 'West Sacramento', 'Pittsburg', 'Gilroy',
         'Morgan Hill', 'Pinole', 'North Beach', 'Woodland', 'Yuba City', 'Vacaville', 'Modesto', 'Dixon', 'Marysville',
         'Tracy', 'Placerville', 'Brentwood', 'Galt', 'Windsor', 'Napa', 'Chico', 'Lincoln', 'Seaside', 'Pleasant Hill',
         'Suisun City', 'Mill Valley', 'Fair Oaks', 'Corte Madera', 'Los Gatos', 'Lafayette', 'Larkspur', 'Orinda',
         'El Sobrante', 'Castro Valley']

        if city in city_list:
            return True
        else:
            return False

    def get_nearby(lat, long, city):

        #restaurant_data = self.db.eatstreet_bay_area_collection.find({'address.city':city})
        restaurant_data = db[city].find()
        nearby_restaurants = []
        for doc in restaurant_data:
            longitude = doc["address"]["longitude"]
            latitude = doc["address"]["latitude"]

            current_location = (float(lat),float(long))
            given_locations = (latitude,longitude)
            dist = great_circle(given_locations, current_location).miles
            if dist <2.00000:
                nearby_restaurants.append(doc)
        return nearby_restaurants

    def get_menu_items(restaurants):
        menu_api_key=[]
        test_list=[]
        rest_data = restaurants
        for each in rest_data:
            menu = each["menu"]
            for each in menu:
                items = each["items"]
                for each in items:
                    apikey = each["apiKey"]
                    if "description" in each:
                        menu_item_str = each["name"]+each["description"]
                    else:
                        menu_item_str = each["name"]

                    menu_api_key.append(apikey)
                    test_list.append(menu_item_str)

        return menu_api_key, test_list

    def get_result_data(result_api,city):

        result =[]

        restaurant_data = db[city].find()
        count = 0
        for doc in restaurant_data:
            rest_data={}
            items=[]
            menu = doc["menu"]
            for each in menu:
                items = items + each["items"]

            menu_names_list = []

            for each in items:
                if each["apiKey"] in result_api:
                    count += 1

                    menu_names_list.append(each["name"])

            if len(menu_names_list) != 0:
                rest_data["restaurant_name"] = doc["restaurant_name"]
                rest_data["address"] = doc["address"]
                rest_data["menu_data"]=menu_names_list
                result.append(rest_data)

        return result

    def filter_for_user_allergies(email, menu_api, menu_list):
        list_of_apis = []
        list_of_menus = []
        print(email)

        profile_data = db_profile['user_profile_collection'].find({'email':email})
        food_to_avoid = None
        for doc in profile_data:
            food_to_avoid = doc["food_to_avoid"]

            for each in menu_list:
                if any(item.lower() in each.lower() for item in food_to_avoid):
                    continue
                else:

                    list_of_menus.append(each.lower())
                    list_of_apis.append(menu_api[menu_list.index(each)])

        return list_of_apis,list_of_menus

'''
if __name__=='__main__':
    obj = operations()
    rest = obj.get_nearby(lat=37.3352,long=-121.8811,city='San Jose')
    menu_api, menu_list = obj.get_menu_items(rest)
    #print(menu_list)
    pickle_obj = recommendationPickle
    #result = pickle_obj.get_recommendation_from_pickle(menu_list)
    result_api_list = recommendationPickle.get_recommendation_from_pickle(menu_api, menu_list)
    print(result_api_list)
    end = time.time()
    print(end - start)
'''