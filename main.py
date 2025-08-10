import pyglet as pg
from pyglet import info
import json
import importlib
import os
import sys

# Config setup
config_file = {}

if not os.path.exists("config.json"):
    # Basic config file
    config_file = {
        "fps": 60, 
        "open-gl-es": False, 
        "vsync": False, 
        "user-agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36"
        }
    with open("config.json", "w") as f:
        f.write(config_file)

with open("config.json", "r") as f:
    config_file = json.load(f)

# Raspiberry Pi config
if config_file["open-gl-es"]:
    pg.options.shadow_window = False
    display = pg.display.get_display()
    screen = display.get_default_screen()
    config = screen.get_best_config()
    config.opengl_api = "gles"
    config.major_version = 3
    config.minor_version = 1
else:
    config = pg.gl.Config(double_buffer=True, samples = 4, sample_buffers = 1)

# Window setup
window = pg.window.Window(resizable=True, config=config)
window.set_fullscreen(True)
window.set_mouse_visible(False)
window.set_vsync(config_file["vsync"])

# Font setup
pg.options['win32_gdi_font'] = True
pg.font.add_file("fonts/Montserrat-Regular.ttf")
helvetica = pg.font.load("Montserrat")

# Notifications
lblErrorNotif = pg.text.Label("", x = 10, y = 10, anchor_x="left", anchor_y="bottom", align="center", color=(255, 0, 0), weight="bold", font_name="Montserrat", font_size=10)

fpsdisplay = pg.window.FPSDisplay(window=window)

# Addon setup
addons = []
sys.path.append(os.path.join(os.getcwd(), "addons"))

for d in os.listdir(os.getcwd() + "/addons"):
    if d.startswith("MAddon_"):
        print("Importing " + d + "...")
        try:
            addons.append(importlib.import_module(d[:-3]).Main(window))
        except Exception as e:
            lblErrorNotif.text = "Unable to load " + d + "!"

@window.event
def on_draw():
    window.clear()
    if lblErrorNotif.text != "":
        lblErrorNotif.draw()
    for a in addons:
        a.draw()
    fpsdisplay.draw()

def update(dt):
    for a in addons:
        try:
            a.update(dt)
        except Exception as e:
            lblErrorNotif.text = "Unable to load " + a.__module__ + "!"

@window.event
def on_key_press(s, m):
    if s == pg.window.key.ESCAPE:
        pg.app.exit()

#print(info.dump())
print("FPS [" + str(config_file["fps"]) + "]")
pg.clock.schedule_interval(update, 1/(config_file["fps"]))
pg.app.run(1/(config_file["fps"]))