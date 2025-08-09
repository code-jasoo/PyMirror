import pyglet as pg
import requests
import json
import threading

# Config setup
config_file = {}
with open("config.json", "r") as f:
    config_file = json.load(f)

class Main:
    def __init__(self, window):
        self.window = window
        self.url = "https://newsapi.org/v2/top-headlines?country=us&apiKey="
        self.apiKey = config_file["news-api-key"]

        self.tCycle = 0
        self.tRefresh = 0
        self.articles = []
        self.currentArticle = 0

        self.Animation = 0
        self.tAnimation = 0

        self.lblSource = pg.text.Label("", font_name="Montserrat", font_size=20, anchor_x="center", anchor_y="center", x = 0, y = 0, color=(64, 64, 64))
        self.lblTitle = pg.text.Label("", font_name="Montserrat", font_size=24, anchor_x="center", anchor_y="center", x = 0, y = 0, align = "center", multiline = True, width = self.window.width * .75, height = 0)

        self.t1 = threading.Thread(target = self.handleRequest, args = (self.url + self.apiKey,), daemon = True)
        self.t1.start()

        self.cycleNews()
        

    def update(self, dt):
        self.tCycle += dt
        self.tRefresh += dt

        self.lblSource.x = self.getX(50)
        self.lblSource.y = self.getY(20)
        self.lblTitle.x = self.getX(50)
        self.lblTitle.y = self.getY(20) - self.lblTitle.height - 20
        self.lblTitle.width = self.window.width * .75

        if self.Animation == 1:
            self.tAnimation += dt
            self.lblSource.color = self.setAlpha(self.lblSource.color, int((1 - self.tAnimation) * 255))
            self.lblTitle.color = self.setAlpha(self.lblTitle.color, int((1 - self.tAnimation) * 255))
            if self.tAnimation >= 0.95:
                self.Animation = 2
                self.lblSource.color = self.setAlpha(self.lblSource.color, 0)
                self.lblTitle.color = self.setAlpha(self.lblTitle.color, 0)
        elif self.Animation == 2:
            self.tAnimation = 0
            self.cycleNews()
            self.Animation = 3
        elif self.Animation == 3:
            self.tAnimation += dt
            self.lblSource.color = self.setAlpha(self.lblSource.color, int(self.tAnimation * 255))
            self.lblTitle.color = self.setAlpha(self.lblTitle.color, int(self.tAnimation * 255))
            if self.tAnimation >= 0.99:
                self.Animation = 0
                self.tAnimation = 0
                self.lblSource.color = self.setAlpha(self.lblSource.color, 255)
                self.lblTitle.color = self.setAlpha(self.lblTitle.color, 255)
                
        if self.tCycle >= 30 and self.Animation == 0: # every five seconds
            self.tCycle = 0
            self.Animation = 1
        if self.tRefresh >= 300: # every five minutes
            self.tRefresh = 0
            self.t1 = threading.Thread(target = self.handleRequest, args = (self.url + self.apiKey,), daemon = True)
            self.t1.start()

    def draw(self):
        self.lblSource.draw()
        self.lblTitle.draw()
    def getX(self, xP):
        return self.window.width * (xP / 100)
    def getY(self, yP):
        return self.window.height * (yP / 100)
    
    def cycleNews(self):
        if self.t1.is_alive():
            return
        source = self.articles[self.currentArticle]["source"]["name"]
        title = self.articles[self.currentArticle]["title"].split(" - ")[0]
        self.lblSource.text = source
        self.lblTitle.text = title
        self.currentArticle += 1
        if self.currentArticle >= len(self.articles):
            self.currentArticle = 0

    def setAlpha(self, tup, value):
        tmp = list(tup)
        tmp[3] = value
        return tuple(tmp)
    
    def handleRequest(self, url):
        data = requests.get(url)
        data = json.loads(data.content)
        self.articles = data["articles"]
