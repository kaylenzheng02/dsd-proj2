from flask import Flask, render_template

app = Flask(__name__)

models = [
    {
        "name": "Mexico 66",
        "description": "A low-profile heritage sneaker with the brand's signature stripes.",
    },
    {
        "name": "Serrano",
        "description": "A lightweight, running-inspired silhouette with a slim profile.",
    },
    {
        "name": "GSM",
        "description": "A court-inspired sneaker with a clean, tennis-influenced look.",
    },
]


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", models=models)
