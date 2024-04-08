from flask import url_for
from flask import redirect
from flask import request
import logging

from flask import Flask, render_template
from gunicorn.app.base import BaseApplication

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/search")
def search():
    search_query = request.args.get('search', None)
    if not search_query:
        return redirect(url_for('home'))
    search_results = {}
    from swapi import fetch_data
    for category in ["people", "planets", "starships", "vehicles"]:
        search_results[category] = fetch_data(category, search_query)
    return render_template("search_results.html", search_query=search_query, search_results=search_results)

@app.route("/planets")
def planets(search_query=None):
    from swapi import fetch_data
    planets_data = fetch_data("planets", search_query)
    for planet in planets_data.get("results", []):
        planet["image_url"] = "https://starwars-visualguide.com/assets/img/planets/" + str(planet["url"].split('/')[-2]) + ".jpg"
    if "error" not in planets_data:
        return render_template("planets.html", planets=planets_data.get("results", []))
    else:
        return "<h1>Error fetching data</h1>"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/people", methods=['GET', 'POST'])
def people():
    search_query = request.args.get('search', None)
    from swapi import fetch_data
    people_data = fetch_data("people", search_query)
    for person in people_data.get("results", []):
        person["image_url"] = "https://starwars-visualguide.com/assets/img/characters/" + str(person["url"].split('/')[-2]) + ".jpg"
    if "error" not in people_data:
        return render_template("people.html", people=people_data.get("results", []), search_query=search_query)
    else:
        return "<h1>Error fetching data</h1>"

@app.route("/vehicles", methods=['GET', 'POST'])
def vehicles():
    search_query = request.args.get('search', None)
    from swapi import fetch_data
    vehicles_data = fetch_data("vehicles", search_query)
    for vehicle in vehicles_data.get("results", []):
        vehicle["image_url"] = "https://starwars-visualguide.com/assets/img/vehicles/" + str(vehicle["url"].split('/')[-2]) + ".jpg"
    if "error" not in vehicles_data:
        return render_template("vehicles.html", vehicles=vehicles_data.get("results", []), search_query=search_query)
    else:
        return "<h1>Error fetching data</h1>"

@app.route("/starships", methods=['GET', 'POST'])
def starships():
    search_query = request.args.get('search', None)
    from swapi import fetch_data
    starships_data = fetch_data("starships", search_query)
    for starship in starships_data.get("results", []):
        # Fix for images not loading: Check if 'url' exists and construct image_url accordingly
        if 'url' in starship:
            starship["image_url"] = "https://starwars-visualguide.com/assets/img/starships/" + str(starship["url"].split('/')[-2]) + ".jpg"
        else:
            starship["image_url"] = "https://starwars-visualguide.com/assets/img/placeholder.jpg"  # Placeholder image if 'url' is missing
    if "error" not in starships_data:
        return render_template("starships.html", starships=starships_data.get("results", []), search_query=search_query)
    else:
        return "<h1>Error fetching data</h1>"


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


# Do not remove the main function while updating the app.
if __name__ == "__main__":
    options = {"bind": "%s:%s" % ("0.0.0.0", "8080"), "workers": 4, "loglevel": "info", "accesslog": "-"}
    StandaloneApplication(app, options).run()
