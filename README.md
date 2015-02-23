## 3D printable candidate solutions to the brachistochrone problem

Consider the problem of finding a curve that connects two points A and B,
such that an object rolling down the curve from A to B takes the least amount of time to
make the trip

![Alt text](static/Brachistochrone.png)

This is called the [Brachistochrone problem](http://en.wikipedia.org/wiki/Brachistochrone_curve), a classic problem in the [Calculus of Variations](http://en.wikipedia.org/wiki/Calculus_of_variations).

This repository contains functions which will let you set up your own version of the problem, sketch out your own solution using your mouse, then generate a 3D-printable ramp to roll marbles down in order to test your design.

Run `Ramps.ipynb` using IPython Notebook (with the --pylab=inline argument) to
interactively walk through the process.

### Requirements

The functions of this notebook require:

- [repository of source files associated with this notebook](https://github.com/thearn/printable_ramps)
- ipython
- numpy
- scipy
- matplotlib
- solidpython
- OpenCV, with python `cv2` bindings
- OpenSCAD

The python libraries can be installed by running `pip install -r requirements.txt` within the directory that contains this notebook file. 

The computer vision library OpenCV can be installed [by following their installation instructions](http://docs.opencv.org/doc/tutorials/introduction/table_of_content_introduction/table_of_content_introduction.html). OpenCV can be tricky to install. I'd recommend using a system package manager like apt-get or homebrew if possible. On Windows, the easiest way to get started with OpenCV and Python is to use either [Python(x,y)](https://code.google.com/p/pythonxy/) or the [Anaconda Python Distribution](https://store.continuum.io/cshop/anaconda/)

The CAD program OpenSCAD can be [downloaded from here](http://www.openscad.org/downloads.html). This notebook involves calling OpenSCAD from the command line. To make this work, the path to the OpenSCAD binary will need to be given in the first code cell of the notebook.