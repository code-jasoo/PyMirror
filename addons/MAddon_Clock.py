import pyglet as pg
import datetime
class Main:
    def __init__(self, window):
        self.window = window
        self.lblTime = pg.text.Label("",
                          font_name="Montserrat",
                          font_size=50,
                          x=self.window.width - 20, y=self.window.height - 10,
                          anchor_x='right', anchor_y='top')
        self.lblM = pg.text.Label("",
                          font_name="Montserrat",
                          font_size=25,
                          x=self.window.width - 20, y=self.window.height - 10,
                          anchor_x='right', anchor_y='top',
                          align="right",
                          color = (64, 64, 64),
                          )
        self.lblS = pg.text.Label("",
                          font_name="Montserrat",
                          font_size=25,
                          x=self.window.width - 20, y=self.window.height - 10,
                          anchor_x='right', anchor_y='top',
                          align="right",
                          color = (64, 64, 64),
                          )
        self.lblDate = pg.text.Label("",
                          font_name="Montserrat",
                          font_size=30,
                          x=self.window.width - 20, y=self.window.height - 10,
                          anchor_x='right', anchor_y='top',
                          color = (128, 128, 128))
        self.x = 98
        self.y = 98
    def update(self, dt):
        self.lblTime.x = self.getX(self.x) - 55
        self.lblTime.y = self.getY(self.y)
        self.lblM.x = self.getX(self.x)
        self.lblM.y = self.getY(self.y) - 35
        self.lblS.x = self.getX(self.x) - 10
        self.lblS.y = self.getY(self.y)
        self.lblDate.x = self.getX(self.x)
        self.lblDate.y = self.getY(self.y) - 70
        self.lblTime.text = datetime.datetime.now().strftime("%I:%M")
        if self.lblTime.text.startswith("0"):
            self.lblTime.text = self.lblTime.text[1:]
        self.lblM.text = datetime.datetime.now().strftime("%p")
        self.lblS.text = datetime.datetime.now().strftime("%S")
        self.lblDate.text = datetime.datetime.now().strftime("%d %B %Y")
        if self.lblDate.text.startswith("0"):
            self.lblDate.text = self.lblDate.text[1:]
        self.lblDate.text = datetime.datetime.now().strftime("%A, ") + self.lblDate.text
    def draw(self):
        self.lblTime.draw()
        self.lblM.draw()
        self.lblS.draw()
        self.lblDate.draw()

    def getX(self, xP):
        return self.window.width * (xP / 100)
    def getY(self, yP):
        return self.window.height * (yP / 100)