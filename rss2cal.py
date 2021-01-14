#! /usr/bin/env python

from ics import Calendar, Event
import feedparser
import arrow
import sys

c = Calendar(creator="rss2cal.py by raivivek")

def create_calendar(uri):
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

if __name__=="__main__":
    create_calendar(sys.argv[1])
    print(c, file=sys.stdout)