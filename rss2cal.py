#! /usr/bin/env python

import os
import tempfile

import arrow
import feedparser
from flask import Flask, render_template, send_file, request
from ics import Calendar, Event


app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

def create_calendar(uri):
    c = Calendar(creator="rss2cal.py by raivivek")
    parsed_feed = feedparser.parse(uri)
    for entry in parsed_feed.entries:
        e = Event()
        e.name = entry.title
        e.begin = arrow.get(entry.ev_startdate)
        e.end = arrow.get(entry.ev_enddate)
        e.description = entry.description
        e.location = entry.ev_location
        e.url = entry.link
        e.categories = [entry.category]

        c.events.add(e)
    return c


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/download', methods=['POST'])
def download():
    with tempfile.NamedTemporaryFile(mode='w') as f:
        f.writelines(create_calendar(request.form['url']))

        return send_file(f.name, mimetype="text/calendar", as_attachment=True)


if __name__=="__main__":
    app.run(host='0.0.0.0', port=port, debug=False)