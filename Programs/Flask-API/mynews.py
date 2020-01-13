from flask import Flask, render_template, request
import feedparser, json
import urllib, urllib.parse
from urllib.request import urlopen

app = Flask(__name__)

# different news channel
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'
             }

# api used from openweathermap.com to display weather. Need to register to get APIID
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=5c2e69ebebb59661b227e7e9007f4172"

# api used from openexchangerates.com to display currency. Need to register to get APIID
CURRENCY_URL ="https://openexchangerates.org//api/latest.json?app_id=fea11218798f4c03a36c1b3df98241ec"

# set default values for -news, city, currency
DEFAULTS = {'publication': 'bbc',
            'city': 'London,UK,Mumbai,Japan,Paris',
            'currency_from':'GBP',
            'currency_to':'USD'
            }


@app.route('/')
def home():
    # command line arguments passed on browser(key-value parameters)
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
        # Get news for BBC
    articles=get_news(publication)
    # Get the city information to display weather
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    # Get currency
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate,currencies = get_rate(currency_from, currency_to)

    return render_template("home.html", articles=articles, weather=weather,
                           currency_from=currency_from,currency_to=currency_to,rate=rate,
                           currencies=sorted(currencies))


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_rate(frm, to):
    all_currency = urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate / frm_rate, parsed.keys()


def get_weather(query):
    query = urllib.parse.quote(query)       # quote = convert space to %20 to represent in browser
    url = WEATHER_URL.format(query)         # format the url
    urldata = urlopen(url)                  # open the url
    data = urldata.read()                   # the read the (feeds) news from the url
    parsed = json.loads(data)               # load the data in json format
    weather = None
    if parsed.get("weather"):
        # get details of weather save in dictionary format
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"]
                   }
    return weather


if __name__ == '__main__':
    app.run(debug=True)
