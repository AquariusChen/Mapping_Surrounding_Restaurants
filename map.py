import folium
import geocoder
import pandas
import requests as req
import json
import os

def isfloat(str):
    try:
        f = float(str)
    except ValueError:
        return False
    return True

def mark_color(rating):
    if rating >= 4.5:
        return 'darkred'
    elif rating >= 3.5:
        return 'red'
    else:
        return 'lightred'

stream = os.popen('./locateme -f "{LAT},{LON}"')
output = stream.read()
segments = output.split(',')

g = geocoder.ip('me')
map = folium.Map(location=segments, zoom_start=14,tiles="OpenStreetMap")
hi = "Hi! You are currently at %s, %s!" % (g.city, g.state)
f = folium.FeatureGroup(name="My Map")
f.add_child(folium.Marker(location=segments, popup=folium.Popup(hi), icon=folium.Icon('blue')))


api_key = '9Muq5wcq6bVdiblfSgNeisll3VZI6AUkZ_odZnUUqP1BDqqLjjfXEQhfdvYX_lKC5Wy_GweFkV_nT22zgg9bdQ4qLj9j3F3_z_qKAPErJz1dODmHI-vqemtt-EEeX3Yx'
#business_id = 'JHU5HF1aEDkdwIWf2D765A'
header = {'Authorization': 'bearer %s' % api_key}
endpoint = 'https://api.yelp.com/v3/businesses/search'
param = {
'term': input("search for: "),
'limit': 50,
'radius': 20000,
'location': "%s, %s" % (g.city,g.state)}

response = req.get(url = endpoint, params = param, headers = header)
#convert JSON string to a Dictionary
data = response.json()
#ataFrame = pandas.DataFrame(data, columms = data.keys())
keys = data.keys()
business = data['businesses']

rating = input("rating(>=): ")
while not isfloat(rating):
    rating = input("【please input a number】\nrating (>=): ")
for bus in business:
    if bus['rating'] >= float(rating):
        print(bus['name'])
        pop = "<a href=%s target='_blank'>%s</a>\n%s" % (bus['url'],bus['name'],bus['rating'])
        f.add_child(folium.Marker(location=list(bus['coordinates'].values()), popup=pop, icon=folium.Icon(mark_color(bus['rating']))))


#data = pandas.read_csv("")


map.add_child(f)
map.save("Map.html")
