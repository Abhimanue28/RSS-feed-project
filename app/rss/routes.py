from flask import Blueprint, render_template, request, redirect
import feedparser

from app.extensions import mongo


rss = Blueprint('myapp', __name__, url_prefix='/myapp')


# Homepage to add RSS Feed URL
@rss.route('/form')
def form():
    return render_template("index.html")


# Fuction to store URL in Mongodb
@rss.route('/add_new', methods=["POST", "GET"])
def add_new():

    mongo.db.rss_list.insert_one({'url': request.form['link']})
    return redirect('table')


# page to display list of all URLs
@rss.route('/table')
def table():
    data = mongo.db.rss_list.find()
    return render_template("table.html", content=data)


# page with latest content from RSS links
@rss.route('/updates')
def updates():
    temp_list = []
    data = mongo.db.rss_list.find()
    for i in data:
        feed = feedparser.parse(i['url'])
        article = feed['entries'][0]
        temp_list.append({'title': article.get('title'),
                          'link': article.get('link'),
                          'channel': feed['channel']['title']})
    return render_template("updates.html", content=temp_list)
