import urllib.request as urllib
import json
from appJar import gui

#Sry für die UI straight outta Windows 95... Wollte das einfachste UI Framework nehmen das ich finden konnte

def getMortalityRate():
    confirmed = 0
    deaths = 0

    try:
        requestString = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=(Confirmed%20%3E%200)%20AND%20(Deaths%3E0)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Deaths%20desc%2CCountry_Region%20asc%2CProvince_State%20asc&resultOffset=0&resultRecordCount=250&cacheHint=true"
        request = urllib.urlopen(requestString)
        rawData = request.read()
    except:
        print("Error with downloading Data (URL is not working)")
        return 0

    try:
        encoding = request.info().get_content_charset('utf-8')
        dataJson = json.loads(rawData.decode(encoding))

        for country in dataJson.get("features"):
            confirmed += country.get("attributes").get("Confirmed")
            deaths += country.get("attributes").get("Deaths")
    except:
        print("Error with parsing incoming JSON")
        return 0

    return round(deaths/confirmed * 100, 4)

def refresh(button):
    app.setLabel("lblMortalityRate", "Mortality rate: " + str(getMortalityRate()) + "%")

app = gui()
app.addLabel("lblMortalityRate", "Mortality rate: " + str(getMortalityRate()) + "%" )
app.addButton("Refresh", refresh)
app.go()

