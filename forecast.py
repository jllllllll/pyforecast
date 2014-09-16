import forecastio
import datetime
import urllib
import re
import json

# Using checkip.dyndns.org to external IP address.
externalipurl = "http://checkip.dyndns.org"
findip = urllib.urlopen(externalipurl).read()
myIP = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", findip)

# Using IP address to determine geolocation.
geolocationurl = "http://api.hostip.info/get_json.php?ip=" + str(myIP[0]) + "&position=true"
findlocation = urllib.urlopen(geolocationurl).read()
geodata = json.loads(findlocation)

# This script uses the forecast.io api and the forecastio python library to download weather information.
# You must create an account with forecast.io and request an api token.
api_key = "FORECASE.IO_API_TOKEN"

forecast = forecastio.load_forecast(api_key, geodata['lat'], geodata['lng'])
dayofWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

current = forecast.currently()

fdate = datetime.date(current.time.year,current.time.month,current.time.day)
tdy = datetime.date.today()
tom = tdy + datetime.timedelta(days=1)

print "\n" + geodata['city']

print "\n--- Currently ---"
print str(current.summary)
print "Temperature:\t" + str(current.temperature)
print "Humidity:\t" + str(current.humidity * 100) + "%"

byDay = forecast.daily()

print "\n--- 4 Day Forecast ---"
for dailyData in byDay.data[:4]:
    ddate = datetime.date(dailyData.time.year,dailyData.time.month,dailyData.time.day)
    if ddate == tdy:
        print "\nToday"
    elif ddate == tom:
        print "\nTomorrow"
    else:
        print "\n" + dayofWeek[dailyData.time.weekday()]
    print str(dailyData.summary)
    print "Max:\t" + str(dailyData.temperatureMax)
    print "Min:\t" + str(dailyData.temperatureMin)
    print "Rain:\t" + str(dailyData.precipProbability * 100) + "%"
print "\n"
