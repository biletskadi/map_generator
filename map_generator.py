from twitter2 import twit
import folium
from geopy.geocoders import Nominatim
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")


def recursively_parse_json(input_json, target_key, s=set()):
    if type(input_json) is dict:
        for key in input_json:
            if key == target_key:
                s.add((input_json['name'], input_json[key], input_json['screen_name']))
            recursively_parse_json(input_json[key], target_key)
    elif type(input_json) is list:
        for entity in input_json:
            recursively_parse_json(entity, target_key)
    return s


def location(locations):
    """
    function returns latitude and longitude from location name
    """
    geo = Nominatim(user_agent="main.py")
    location1 = geo.geocode(locations)
    return location1.latitude, location1.longitude


@app.route("/map", methods=["POST"])
def map1():
    user_name = str(request.form['name'])
    json_dct = twit(user_name)
    lst = []
    lst1 = []
    # with open("twit.json", 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    x = list(recursively_parse_json(json_dct, "location"))
    for i in x:
        if len(i[1]) > 1:
            lst.append([i[0], i[1], i[2]])
    for i, y in enumerate(lst):
        try:
            y.append(location(y[1]))
        except AttributeError:
            continue
    for z in lst:
        if len(z) == 4:
            lst1.append(z)
    m = folium.Map(location=[49.8350125, 24.0197128],
                   zoom_start=12)
    for i in range(len(lst1) - 1):
        tooltip = str(lst1[i][0])
        folium.Marker([lst1[i][3][0], lst1[i][3][1]], popup=lst1[i][2], tooltip=tooltip).add_to(m)

    n = m.get_root().render()
    contex = {"n": n}

    return render_template('map.html', **contex)

if __name__ == '__main__':
    app.run(debug = True, port=3000)

map1()