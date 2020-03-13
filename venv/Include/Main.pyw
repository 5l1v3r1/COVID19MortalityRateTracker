import urllib.request as urllib
import json
from appJar import gui
import timeg
from threading import Thread

#Sry für die UI straight outta Windows 95... Wollte das einfachste UI Framework nehmen das ich finden konnte

def getData():
    try:
        requestString = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=(Confirmed%20%3E%200)%20AND%20(Deaths%3E0)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Deaths%20desc%2CCountry_Region%20asc%2CProvince_State%20asc&resultOffset=0&resultRecordCount=250&cacheHint=true"
        request = urllib.urlopen(requestString)
        rawData = request.read()
    except:
        print("Error with downloading Data (URL is not working)")

    try:
        encoding = request.info().get_content_charset('utf-8')
        dataJson = json.loads(rawData.decode(encoding))
    except:
        print("Error with parsing incoming JSON")
        return 0

    return dataJson


def refresh():
    dataJson = getData()

    confirmed = 0
    deaths = 0
    recovered = 0

    for country in dataJson.get("features"):
        confirmed += country.get("attributes").get("Confirmed")
        deaths += country.get("attributes").get("Deaths")
        recovered += country.get("attributes").get("Recovered")

    app.setLabel("lblMortalityRate", str(round(deaths / (recovered + deaths)* 100, 4)) + "%")
    app.setLabel("lblConfirmed", confirmed)
    app.setLabel("lblRecovered", recovered)
    app.setLabel("lblDeaths", deaths)

def setUpLoop():
    while 1:
        refresh()
        time.sleep(3600)


app = gui("Corona-Tracker", "400x200")
app.addLabel("textMortalityRate", "Mortality rate: ", 0, 0)
app.addLabel("lblMortalityRate", "", 0, 1)
app.addLabel("textConfirmed", "Total Infected: ", 1, 0)
app.addLabel("lblConfirmed", "", 1, 1)
app.addLabel("txtRecovered", "Total Healed: ", 2, 0)
app.addLabel("lblRecovered", "", 2, 1)
app.addLabel("txtDeaths", "Total Deaths: ", 3, 0)
app.addLabel("lblDeaths", "", 3,1)
app.addButton("Refresh", refresh, 4, 0)
app.setOnTop(stay=True)
app.setResizable(canResize=False)
app.setFont(size = 16, family="Calibri")

t = Thread(target=setUpLoop, args=())
t.start()

app.go()




