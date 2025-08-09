import pyglet as pg
import ics
import arrow
import requests
import json
import threading
import datetime

# Config setup
config_file = {}
with open("config.json", "r") as f:
    config_file = json.load(f)

class Main:
    def __init__(self, window):
        self.lblDates = []
        self.window = window
        self.x = 98
        self.y = 80
        self.urls = config_file["ical"]
        self.urls.append("https://ics.calendarlabs.com/76/51531e26/US_Holidays.ics")
        self.calendar = ics.Calendar()

        self.t1 = threading.Thread(target = self.handleRequest, args = (self.urls,), daemon = True)
        self.t1.start()

        for i in range(4):
            self.lblDates.append(pg.text.Label("", x = self.getX(self.x), y = self.getY(self.y - (i * 5)), color=(255 - (i * 64), 255 - (i * 64), 255 - (i * 64)), font_name="Montserrat", font_size=20, anchor_x="right", anchor_y="top", align="right", multiline=True, width=self.getX(50)))
    def update(self, dt):
        i = 0
        if self.getFutureEvents() == []:
            return
        for lbl in self.lblDates:
            lbl.text = self.getFutureEvents()[i].name + "\n" + self.getFutureEvents()[i].begin.strftime("%A. %d %B %Y")
            lbl.x = self.getX(self.x)
            lbl.y = self.getY(self.y - (i * 8))
            i += 1
    def draw(self):
        for lbl in self.lblDates:
            lbl.draw()
    def getX(self, xP):
        return self.window.width * (xP / 100)
    def getY(self, yP):
        return self.window.height * (yP / 100)
    def getFutureEvents(self):
        tmp = []
        for evnt in list(self.calendar.timeline):
            if not datetime.datetime.now().timestamp() > evnt.end.timestamp():
                tmp.append(evnt)
        return tmp
    def handleRequest(self, urls):
        for u in urls:
            for e in ics.Calendar(requests.get(u, headers = {"User-Agent": config_file["user-agent"]}).text).events:
                self.calendar.events.add(e)