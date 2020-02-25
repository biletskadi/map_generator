import twitter2
import folium
import certifi
import ssl
import geopy
from geopy.geocoders import Nominatim
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def recursively_parse_json(input_json):
    s = set()
    for key in input_json['users']:
        s.add((key['name'], key['screen_name'], key['location']))
    return s


def location(locations):
    """
    function returns latitude and longitude from location name
    """
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx

    geo = Nominatim(user_agent="map_main.py", timeout=10)
    location1 = geo.geocode(locations)
    return location1.latitude, location1.longitude


@app.route("/map", methods=["POST"])
def map1():
    user_name = str(request.form['name'])
    print(user_name)
    json_dct = twitter2.twit(user_name)
    lst = []
    lst1 = []
    # with open("twit.json", 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    x = list(recursively_parse_json(json_dct))
    print(x)
    for i in x:
        if len(i[2]) > 1:
            lst.append([i[0], i[1], i[2]])
    for i, y in enumerate(lst):
        try:
            y.append(location(y[2]))
        except AttributeError:
            continue
    print(y)
    for z in lst:
        if len(z) == 4:
            lst1.append(z)
    m = folium.Map(location=[49.8350125, 24.0197128],
                   zoom_start=12)
    for i in range(len(lst1) - 1):
        tooltip = str(lst1[i][0])
        folium.Marker(location=[lst1[i][3][0], lst1[i][3][1]], popup=lst1[i][1], tooltip=tooltip).add_to(m)

    n = m.get_root().render()
    contex = {"n": n}

    return render_template('map.html', **contex)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
