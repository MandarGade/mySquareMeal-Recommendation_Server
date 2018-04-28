import requests
import json

class city_name:

    def get_city_name(lat, long):
        # grab some lat/long coords from wherever. For this example,
        # I just opened a javascript console in the browser and ran:
        #
        # navigator.geolocation.getCurrentPosition(function(p) {
        #   console.log(p);
        # })
        #
        # latitude = 35.1330343
        # longitude = -90.0625056
        # latitude=37.3351874
        # longitude=-121.88107150000002
        # latitude=37.4159317
        # longitude=-122.1431202
        latitude = lat
        longitude = long
        # Did the geocoding request comes from a device with a
        # location sensor? Must be either true or false.
        sensor = 'true'

        # Hit Google's reverse geocoder directly
        # NOTE: I *think* their terms state that you're supposed to
        # use google maps if you use their api for anything.
        base = "http://maps.googleapis.com/maps/api/geocode/json?"
        params = "latlng={lat},{lon}&sensor={sen}".format(
            lat=latitude,
            lon=longitude,
            sen=sensor
        )
        url = "{base}{params}".format(base=base, params=params)
        # response = requests.get(url)
        while True:
            response = requests.get(url).json()
            if (response['status'] == 'OK'):
                result = response['results'][0]
                break

        keys_list = ['locality', 'political']
        for each in result['address_components']:
            if each['types'] == keys_list:
                city_name = each['short_name']

        return city_name


        # print(get_city_name(37.3351874,-121.88107150000002))