import csv
from datetime import datetime
import os
import random

import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

INATURALIST_API_URL = "https://api.inaturalist.org/v1/observations"


def get_two_bird_images():
    # Ask iNaturalist for random, research-grade bird observations with photos.
    search_options = {
        "taxon_id": 3,
        "photos": "true",
        "quality_grade": "research",
        "per_page": 100,
        "order_by": "random",
    }
    response = requests.get(
        INATURALIST_API_URL, params=search_options, timeout=15
    )
    response.raise_for_status()
    observations = response.json().get("results", [])

    images = []
    for observation in observations:
        photos = observation.get("photos", [])
        taxon = observation.get("taxon") or {}
        if not photos:
            continue

        common_name = taxon.get("preferred_common_name")
        species_name = taxon.get("name", "Bird")
        title = common_name or observation.get("species_guess") or species_name
        photo = photos[0]
        image_url = photo.get("url", "").replace("/square.", "/large.")

        if image_url:
            images.append(
                {
                    "id": observation["id"],
                    "title": title,
                    "image_url": image_url,
                }
            )

    if len(images) < 2:
        raise ValueError("iNaturalist did not return two bird photos.")

    return random.sample(images, 2)


@app.route("/")
def home():
    return send_from_directory(app.root_path, "index.html")


@app.route("/style.css")
def stylesheet():
    return send_from_directory(app.root_path, "style.css", mimetype="text/css")


@app.route("/api/images")
def images():
    try:
        image_pair = get_two_bird_images()
        return jsonify(images=image_pair)
    except (requests.RequestException, ValueError) as error:
        app.logger.error("Could not load bird photos: %s", error)
        return jsonify(error="Bird photos are temporarily unavailable."), 502


@app.route("/api/vote", methods=["POST"])
def vote():
    vote_data = request.get_json(silent=True)
    if not isinstance(vote_data, dict):
        return jsonify(error="A valid vote is required."), 400

    option = vote_data.get("option")
    titles = vote_data.get("titles")
    if type(option) is not int or option not in (1, 2):
        return jsonify(error="Choose Option 1 or Option 2."), 400
    if not isinstance(titles, list) or len(titles) != 2:
        return jsonify(error="The selected image pair is invalid."), 400
    if not all(isinstance(title, str) for title in titles):
        return jsonify(error="The selected image pair is invalid."), 400

    chosen_bird = titles[option - 1]
    csv_path = os.path.join(app.root_path, "votes.csv")
    try:
        file_is_new = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
        with open(csv_path, "a", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            if file_is_new:
                writer.writerow(
                    ["timestamp", "option", "chosen_bird", "option_1_bird", "option_2_bird"]
                )
            writer.writerow(
                [
                    datetime.now().astimezone().isoformat(timespec="seconds"),
                    option,
                    chosen_bird,
                    titles[0],
                    titles[1],
                ]
            )
    except OSError as error:
        app.logger.error("Could not save vote to CSV: %s", error)
        return jsonify(error="Your choice could not be saved."), 500

    print(f"Vote: Option {option} — {chosen_bird}", flush=True)
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(debug=True)
