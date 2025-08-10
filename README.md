# PyMirror
A simple, performant python script for your DIY smart mirror.<br>
![PyMirror Icon](https://github.com/code-jasoo/PyMirror/blob/main/images/PyMirrorLogo%20256.png)
<br>
**This project is a work in progress!**<br><br>
PyMirror uses *pyglet* as its rendering engine to enable smooth, high-performance graphics while being simple and easy to customize.


### Dependencies
- [pyglet](https://pypi.org/project/pyglet/) >= 2.0.0
- [requests](https://pypi.org/project/requests/)
- [ics](https://pypi.org/project/ics/) (needed for MAddon_Calendar.py)
- [arrow](https://pypi.org/project/arrow/) (needed for MAddon_Calendar.py and MAddon_Weather.py)

### Installation
1. Clone repository
2. Download and install dependecies using pip
3. Run main.py

Or run the auto-install.sh script!

### Usage on RPi
Raspiberry Pis run OpenGL ES while pyglet runs OpenGL by default. To run the script on a Raspiberry Pi, simply edit the config.json file and change `open-gl-es` to `true`. If config.json does not show up, make sure to run the script first to auto generate the config file. More information can be found [here](https://pyglet.readthedocs.io/en/latest/programming_guide/opengles.html#programming-guide-opengles).

### Developing addons
Developing addons is made easy with pyglet and a provided template found in the [examples folder](https://github.com/code-jasoo/PyMirror/tree/main/examples).<br>
The template consists of one class, `Main`, but is not limited to only one.
- The `update` function is the "logic loop" of your addon. Things such as animations or updating labels should be done here.
- The `draw` function is the "draw loop" of your addon. This is where sprites, shapes, labels, etc. should be drawn.
- `getX` and `getY` are functions to convert percent values to coordinates. `getX(50)` would indicate 50% of the user's screen which would be the center of their screen horizontally. This is PyMirror's current way of scaling to different screens.

[Documentation for pyglet in general can be found here.](https://pyglet.readthedocs.io/en/latest/index.html)

### Naming scheme
<u>All addons must have</u> `MAddon_` <u>at the start of their file name to be recognized by PyMirror!</u>


