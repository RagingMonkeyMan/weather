import requests
from datetime import datetime
import sys
import config

# Calls the api and gets the forecast data
def get_weather_data(url):
    try:
        response = requests.get(url)
        code = response.status_code
        data = response.json()

    except Exception as e:
        print("\nThere was a problem retrieving your weather data, please try again later.", end="\n\n")
        raise e
        sys.exit()

    match code:
        case code if code == 404:
            if 'message' in data and data['message'] == 'city not found':
                print("\nThe zip code entered does not corrispond to a US city, please try another zip code", end="\n\n")
            else:
                print("\nThe Open Weather API is not responding, please try again later.", end="\n\n")
            sys.exit()
            
        case code if code >= 300:
            print("\nThere was a problem retrieving your weather data, please try again later.", end="\n\n")
            sys.exit()

    return data

# Validates zip code input
def validate_zip(zip):
    try:
        zip = zip.strip()
        if not zip.isnumeric():
            raise TypeError("Zip code must be numeric")
        if len(zip) != 5:
            raise Exception("Zip code must be a 5 digit number")
    except Exception as e:
        print(e)
        sys.exit()


# Get zip input from user
print("\nEnter your zip code: ")
zip = input()
validate_zip(zip)

# Make request and put response data in json format
url = "http://api.openweathermap.org/data/2.5/weather?zip=" + str(zip) + "," + config.COUNTRY + "&appid=" + config.API_KEY + "&units=" + config.UNITS
data = get_weather_data(url)

# location and date/time
date_updated = datetime.fromtimestamp(int(data['dt'])).strftime(config.DATETIME_FORMAT)
print("\n", data['name'], "\t\t", date_updated, sep="", end="\n\n")

temps = data['main']
weather_conditions = data['weather']

# There can be multiple weather conditions, handle each here
for condition in weather_conditions:
    id = condition['id']

    # tailor output to weather condition
    match id:
        case id if id < 600: # rain/drizzle/thunderstorm
            print(condition['description'].capitalize(),  sep='', end="\t\t")
            if 'rain' in data:
                if '1h' in data['rain']:
                    print("Rain in the last hour: ", data['rain']['1h'], " mm", sep="")
                if '3h' in data['rain']:
                    print("\t\t\tRain in the last 3 hours: ", data['rain']['3h'], " mm", sep="")
        case id if id < 700: # snow
            print(condition['description'].capitalize(),  sep='', end="\t\t")
            if 'snow' in data:
                if '1h' in data['snow']:
                    print("Snow in the last hour: ", data['snow']['1h'], " mm", sep="")
                if '3h' in data['snow']:
                    print("\t\t\tSnow in the last 3 hours: ", data['snow']['3h'], " mm", sep="")
        case id if id > 800: # clouds
            print(condition['description'].capitalize(), " ", data['clouds']['all'], "%", sep="")
        case _: # default, clear/atmoshperic conditions
            print(condition['main'], sep='')
    print()

print(int(temps['temp']), "°F", sep='')
print("High ", int(temps['temp_max']), "°, Low ", int(temps['temp_min']), "°", sep='')
print("Feels Like ", int(temps['feels_like']), "°", sep='', end="\n\n")

if 'wind' in data:
    wind = data['wind']

    # gust is not always supplied, must check it here
    if 'gust' in wind:
        print("Wind ", int(wind['speed']), " mph, ", wind['deg'], "° with gusts up to ", wind['gust'], " mph", sep='')
    else:
        print("Wind ", int(wind['speed']), " mph, ", wind['deg'], "°", sep='')

print("Humidity ", temps['humidity'], "%", sep='')
print("Pressure ", temps['pressure'], " hPa", sep='') 

if 'visibility' in data:
    print("Visibility ", data['visibility'], " meters", sep='')

print()