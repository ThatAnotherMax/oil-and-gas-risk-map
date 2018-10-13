# coding: utf-8

from flask import Flask, render_template, Markup

app = Flask(__name__, template_folder="templates")

API_KEY = "AIzaSyD7uRVSlRJRCICowKelW5zurV9PTs3HYGE"

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = API_KEY


@app.route('/')
def fullmap():
    map_params = dict(
        identifier="fullmap",
        varname="fullmap",
        lat=48.383022,
        lng=31.1828699,
        zoom=6.5,
        drawing=False
    )
    return render_template('fullmap.html', **map_params)

@app.route('/drawing')
def drawing():
    map_params = dict(
        identifier="fullmap",
        varname="fullmap",
        lat=48.383022,
        lng=31.1828699,
        zoom=6.5,
        drawing=True
    )
    return render_template('fullmap.html', **map_params)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
