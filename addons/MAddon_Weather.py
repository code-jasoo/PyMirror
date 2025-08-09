import pyglet as pg
import requests
import json
import threading
import arrow

# Config setup
config_file = {}
with open("config.json", "r") as f:
    config_file = json.load(f)

class Main:
    def __init__(self, window):
        self.window = window
        self.url = config_file["nws-api"]
        self.data = []

        self.animation = 0
        self.pAnimation = 0
        self.currentCard = 2

        self.refreshP = 0
        self.cycleP = 0

        self.x = 95
        self.y = 35

        self.mcard = MainCard(self.getX(self.x) - 300, self.getY(self.y))
        self.subCard = SubCard(self.getX(self.x), self.getY(self.y))
        self.subCard.setAlpha(0)

        self.seperator = pg.shapes.Line(self.getX(self.x) - 100, self.getY(self.y) + 100, self.getX(self.x) - 100, self.getY(self.y) - 50, thickness = 1, color = (255, 255, 255))

        self.t1 = threading.Thread(target = self.handleRequest, args = (config_file["nws-api"],), daemon = True)
        self.t1.start()

    def update(self, dt):
        self.refreshP += dt
        self.cycleP += dt
        if self.animation == 1:
            self.pAnimation += dt * 1
            self.subCard.setAlpha(int(self.pAnimation * 255))
            if self.pAnimation >= 0.95:
                self.subCard.setAlpha(255)
                self.animation = 2
                
        if self.animation == 2:
            self.pAnimation = 0
            self.subCard.update(arrow.get(self.data[self.currentCard]["startTime"]).strftime("%a"),
                    self.data[self.currentCard]["temperature"], 
                    self.data[self.currentCard]["probabilityOfPrecipitation"]["value"], 
                    self.data[self.currentCard]["detailedForecast"].lower())
            self.animation = 3
        if self.animation == 3:
            self.pAnimation += dt * 1
            self.subCard.setAlpha(int((1 - self.pAnimation) * 255))
            if self.pAnimation >= 0.95:
                self.subCard.setAlpha(0)
                self.animation = 0

        if self.data == [] or self.animation != 0:
            return
        self.mcard.update(self.data[0]["temperature"], 
                          self.data[0]["probabilityOfPrecipitation"]["value"], 
                          self.data[1]["temperature"], 
                          self.data[1]["probabilityOfPrecipitation"]["value"],
                          self.data[0]["detailedForecast"].lower(), 
                          self.data[1]["detailedForecast"].lower())
        
        if self.refreshP >= 300:
            self.refreshP = 0
            self.t1 = threading.Thread(target = self.handleRequest, args = (config_file["nws-api"],), daemon = True)
            self.t1.start()
        
        if self.cycleP >= 5:
            self.cycleP = 0
            self.cycleCard()
        
    def draw(self):
        self.subCard.draw()
        self.mcard.draw()
        self.seperator.draw()
        
    def getX(self, xP):
        return self.window.width * (xP / 100)
    def getY(self, yP):
        return self.window.height * (yP / 100)
    
    def handleRequest(self, url):
        data = requests.get(url)
        data = json.loads(data.content)
        self.data = data["properties"]["periods"]
    
    def cycleCard(self):
        self.animation = 1
        self.pAnimation = 0
        self.currentCard += 2
        if self.currentCard > 6:
            self.currentCard = 0

class MainCard:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.rain = pg.image.load("images/rain.png")
        self.drop = pg.image.load("images/drop.png")
        self.storm = pg.image.load("images/storm.png")
        self.cloud = pg.image.load("images/cloud.png")
        self.moon = pg.image.load("images/moon.png")
        self.sun = pg.image.load("images/sun.png")

        self.lblDay = pg.text.Label("Today", 
                                      x = 0, 
                                      y = 0, 
                                      font_name="Montserrat", 
                                      font_size=20, 
                                      anchor_x="center", 
                                      anchor_y="center", 
                                      align="center", 
                                      color = (128, 128, 128))

        self.lbl1Temp = pg.text.Label("", 
                                      x = 0, 
                                      y = 0, 
                                      font_name="Montserrat", 
                                      font_size=20, 
                                      anchor_x="center", 
                                      anchor_y="center", 
                                      align="center", 
                                      color = (255, 255, 255))
        
        self.lbl1Rain = pg.text.Label("", 
                                      x = 0, 
                                      y = 0, 
                                      font_name="Montserrat", 
                                      font_size=20, 
                                      anchor_x="center", 
                                      anchor_y="center", 
                                      align="center", 
                                      color = (255, 255, 255))
        
        self.lbl2Temp = pg.text.Label("", 
                                      x = 0, 
                                      y = 0, 
                                      font_name="Montserrat", 
                                      font_size=20, 
                                      anchor_x="center", 
                                      anchor_y="center", 
                                      align="center", 
                                      color = (255, 255, 255))
        
        self.lbl2Rain = pg.text.Label("", 
                                      x = 0, 
                                      y = 0, 
                                      font_name="Montserrat", 
                                      font_size=20, 
                                      anchor_x="center", 
                                      anchor_y="center", 
                                      align="center", 
                                      color = (255, 255, 255))
        
        self.rain1Icon = pg.sprite.Sprite(self.rain)
        self.rain1Icon.width = 30
        self.rain1Icon.height = 30
        self.rain2Icon = pg.sprite.Sprite(self.rain)
        self.rain2Icon.width = 30
        self.rain2Icon.height = 30
        self.sunIcon = pg.sprite.Sprite(self.sun)
        self.sunIcon.width = 30
        self.sunIcon.height = 30
        self.moonIcon = pg.sprite.Sprite(self.moon)
        self.moonIcon.width = 30
        self.moonIcon.height = 30

    def draw(self):
        self.lblDay.draw()
        self.lbl1Temp.draw()
        self.lbl1Rain.draw()
        self.lbl2Temp.draw()
        self.lbl2Rain.draw()
        self.rain1Icon.draw()
        self.rain2Icon.draw()
        self.sunIcon.draw()
        self.moonIcon.draw()

    def update(self, t1, r1, t2, r2, d1, d2):
        self.lbl1Temp.text = str(t1) + "°F"
        self.lbl1Rain.text = str(r1) + "%"
        self.lbl2Temp.text = str(t2) + "°F"
        self.lbl2Rain.text = str(r2) + "%"
        
        self.lblDay.y = 100 + self.y
        self.lblDay.x = 50 + self.x

        self.lbl1Temp.x = self.x
        self.lbl1Rain.x = self.x
        self.lbl1Temp.y = 50 + self.y
        self.lbl1Rain.y = self.y
        
        self.lbl2Temp.x = 150 + self.x
        self.lbl2Rain.x = 150 + self.x
        self.lbl2Temp.y = 50 + self.y
        self.lbl2Rain.y = self.y

        self.rain1Icon.x = self.lbl1Rain.x - 70
        self.rain2Icon.x = self.lbl2Rain.x - 70
        self.rain1Icon.y = self.lbl1Rain.y - 15
        self.rain2Icon.y = self.lbl2Rain.y - 15

        self.sunIcon.x = self.lbl1Temp.x - 70
        self.moonIcon.x = self.lbl2Temp.x - 70
        self.sunIcon.y = self.lbl1Temp.y - 15
        self.moonIcon.y = self.lbl2Temp.y - 15

        if "cloudy" in d1:
            self.rain1Icon.image = self.cloud
        if "showers" in d1:
            self.rain1Icon.image = self.rain
        if "storm" in d1:
            self.rain1Icon.image = self.storm
        
        if "cloudy" in d2:
            self.rain2Icon.image = self.cloud
        if "showers" in d2:
            self.rain2Icon.image = self.rain
        if "storm" in d2:
            self.rain2Icon.image = self.storm
        


class SubCard:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.rect = pg.shapes.Rectangle(x = self.x - 90, y = self.y - 30, width = 150, height = 150, color = (0, 0, 0, 255))

        self.rain = pg.image.load("images/rain.png")
        self.drop = pg.image.load("images/drop.png")
        self.storm = pg.image.load("images/storm.png")
        self.cloud = pg.image.load("images/cloud.png")

        self.lblDay = pg.text.Label("", 
                                      x = 0, 
                                      y = 0, 
                                      font_name="Montserrat", 
                                      font_size=20, 
                                      anchor_x="center", 
                                      anchor_y="center", 
                                      align="center", 
                                      color = (128, 128, 128))

        self.lbl1Temp = pg.text.Label("", 
                                      x = 0, 
                                      y = 0, 
                                      font_name="Montserrat", 
                                      font_size=20, 
                                      anchor_x="center", 
                                      anchor_y="center", 
                                      align="center", 
                                      color = (255, 255, 255))
        
        self.lbl1Rain = pg.text.Label("", 
                                      x = 0, 
                                      y = 0, 
                                      font_name="Montserrat", 
                                      font_size=20, 
                                      anchor_x="center", 
                                      anchor_y="center", 
                                      align="center", 
                                      color = (255, 255, 255))

        
        self.rain1Icon = pg.sprite.Sprite(self.rain)
        self.rain1Icon.width = 30
        self.rain1Icon.height = 30
        self.rain1Icon.x = self.lbl1Rain.x - 70
        self.rain1Icon.y = self.lbl1Rain.y - 15

    def draw(self):
        self.lblDay.draw()
        self.lbl1Temp.draw()
        self.lbl1Rain.draw()
        self.rain1Icon.draw()
        self.rect.draw()


    def update(self, day, t1, r1, d1):
        self.lblDay.text = day
        self.lbl1Temp.text = str(t1) + "°F"
        self.lbl1Rain.text = str(r1) + "%"
        
        self.lblDay.y = 100 + self.y
        self.lblDay.x = self.x - 20

        self.lbl1Temp.x = self.x
        self.lbl1Rain.x = self.x
        self.lbl1Temp.y = 50 + self.y
        self.lbl1Rain.y = self.y

        self.rain1Icon.x = self.lbl1Rain.x - 70
        self.rain1Icon.y = self.lbl1Rain.y - 15

        if "cloudy" in d1:
            self.rain1Icon.image = self.cloud
        if "showers" in d1:
            self.rain1Icon.image = self.rain
        if "storm" in d1:
            self.rain1Icon.image = self.storm
    
    def setAlpha(self, value):
        self.rect.color = (self.rect.color[0], self.rect.color[1], self.rect.color[2], value)