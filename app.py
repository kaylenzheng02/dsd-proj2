from flask import Flask, render_template

app = Flask(__name__)

shoes = [
    {
        "brand": "Birkenstock",
        "style": "Arizona Soft Footbed",
        "colorway": "Faded Khaki",
        "material": "Oiled leather",
        "colors": ["#77715c", "#bda17a"],
        "image": "images/birkenstock-arizona.jpg",
        "source": "https://www.birkenstock.com/us/arizona-soft-footbed-natural-leather-oiled/arizona-core-oiledleather-softfootbed-eva-u_1624.html",
    },
    {
        "brand": "Onitsuka Tiger",
        "style": "Mexico 66",
        "image": "images/mexico-66-pure-silver-black.jpg",
        "source": "https://www.sneakers4u.nl/sneaker/onitsuka-tiger-mexico-66-pure-silver-black-1183b566-020/",
        "colorway": "Pure Silver / Black",
        "colors": ["#c5c8cd", "#191919"],
    },
    {
        "brand": "Havaianas",
        "style": "Classic flip-flops",
        "image": "images/havaianas-navy.png",
        "source": "https://www.next.com.au/en/style/sv011595/v56420",
        "colorway": "Navy",
        "colors": ["#202d49", "#202d49"],
    },
    {
        "brand": "Onitsuka Tiger",
        "style": "Ballet flats",
        "image": "images/ballet-birch-navy.jpg",
        "source": "https://dvshopcebu.com/products/onitsuka-tiger-mexico-66-tgrs-birch-peacoat-1182a678-200",
        "colorway": "Birch / Navy",
        "colors": ["#e8dfcd", "#202d49"],
    },
]


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/index")
@app.route("/inventory")
def index():
    return render_template("index.html", shoes=shoes)


