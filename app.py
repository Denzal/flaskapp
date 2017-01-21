import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)

# Dictionary with feed links
FEED_RSS = {"bbc": 'http://feeds.bbci.co.uk/news/rss.xml',
            "cnn": 'http://rss.cnn.com/rss/edition.rss',
            "fox": 'http://feeds.foxnews.com/foxnews/latest',
            "iol": 'http://www.iol.co.za/cmlink/1.640',
            "kor": 'http://k.img.com.ua/rss/ru/all_news2.0.xml'}


@app.route('/')
@app.route('/<channel>')
def get_news(channel="bbc"):
    feed = feedparser.parse(FEED_RSS[channel])

    return render_template("home.html",
                           channel=channel,
                           articles=feed['entries'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)