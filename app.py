import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
#import urllib2
import urllib
from urllib.request import urlopen
from urllib.parse import quote

app = Flask(__name__)

# App constants
CURRENCY_API_KEY = "9d7312182bb34c328344dc83d1acc2c0"
WEATHER_API_KEY = "cb932829eacb6a0e9ee4f38bfbf112ed"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=" + CURRENCY_API_KEY
FEED_RSS = {"bbc": 'http://feeds.bbci.co.uk/news/rss.xml',
            "cnn": 'http://rss.cnn.com/rss/edition.rss',
            "fox": 'http://feeds.foxnews.com/foxnews/latest',
            "iol": 'http://www.iol.co.za/cmlink/1.640',
            "kor": 'http://k.img.com.ua/rss/ru/all_news2.0.xml'}
DEFAULTS = {"channel": 'bbc',
            "city": 'London,UK',
            "currency_from": 'GBP',
            "currency_to": 'USD'}

@app.route('/')
def home():
    #RSS feed
    channel = request.args.get("channel")
    if not channel:
        channel = DEFAULTS["channel"]
    articles = get_news(channel)
    #Weather
    city = request.args.get("city")
    if not city:
        city = DEFAULTS["city"]
    weather = get_weather(city)
    #Currency rates
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS["currency_from"]
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS["currency_to"]
    rate, currencies = get_rate(currency_from, currency_to)

    return render_template("home.html", articles=articles, weather=weather, currency_from=currency_from, currency_to=currency_to, rate=rate, currencies=currencies)

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed"
    query = quote(query)
    url = api_url.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data.decode("utf-8"))
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],"temperature":int(parsed["main"]["temp"]),"city":parsed["name"],'country': parsed['sys']['country']}
    return weather

def get_news(channel):
    if not channel or channel.lower() not in FEED_RSS:
        channel = DEFAULTS["channel"]
    else:
        channel = channel.lower()
    feed = feedparser.parse(FEED_RSS[channel])
    return feed['entries']

def get_rate(frm, to):
    all_currency = urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency.decode("utf-8")).get("rates")
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (round(to_rate/frm_rate,2),parsed.keys())


if __name__ == '__main__':
    app.run(port=5000, debug=True)
