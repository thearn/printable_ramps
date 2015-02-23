from solid import *
import numpy as np
import subprocess

def multiple_ramp_strings(Rs):
    """
    Joins together source code strings for multiple ramps.
    """
    s = ''.join(Rs)

    cp = ['\ntranslate([0, %i, 0]) ramp%i();' % (i*30, i) for i in xrange(len(Rs))]

    return s + ''.join(cp)

def render_stl(openscad_path, code_filename, output_name):
    """
    Renders an STL using an OpenSCAD source file
    """
    with open("%s.scad" % output_name, "wb") as f:
        f.write(code_filename)

    subprocess.call([openscad_path, 
                     "-o", "%s.stl" % output_name, "%s.scad" % output_name])


def ramp(y, 
    x = None,
    length = 50, 
    n = 100,
    thickness = 2,
    start_backheight = 2,
    start_backdepth = 10,
    channel_width = 10,
    channel_depth = 3,
    name="ramp"):
    
    """
    Generate the OpenSCAD source code for a series of marble ramps with
    curvatures given by the points of input array y.

    y can be a single curve or list of curves.
    """

    if hasattr(y, '__iter__') and hasattr(y[0], '__iter__'):
        codes = []
        for i, y_ in enumerate(y[::-1]):
            code = ramp(y_, length=length, n=n, thickness=thickness,
                        start_backheight=start_backheight,
                        start_backdepth=start_backdepth,
                        channel_width=channel_width,
                        channel_depth=channel_depth,
                        name = name + str(i))
            codes.append(code)
        return multiple_ramp_strings(codes)
    
    if not isinstance(x, np.ndarray):
        x = np.linspace(0, length, n)

    if len(y) != n:
        small_x = np.linspace(0, length, len(y))
        y = np.interp(x, small_x, y)

    if y[0] >  y[1]:
        y = y[::-1]

    y += thickness
    chan2 = 2*channel_width
    chan3 = 3*channel_width
    stop = x[-1]

    pts = [list(i) for i in zip(x,y)]

    pts.extend([[x[-1], thickness], [x[-1], 0], [0,0]])

    d = polygon(pts)

    d = linear_extrude(height=channel_width)(d)

    d = rotate([90,0,0])(d)

    code1 = ("module %s_curve() { " % name) + scad_render( d) + " }"

    code2 = """
    module %s() {
     union() {
    
    translate([0, -%i, %f]) %s_curve();
    %s_curve();
    translate([0, %i, %f]) %s_curve();
    translate([0, -%i, 0]) cube([%f, %i, %f]);
    translate([%f, -%i, 0]) cube([%f, %i, %f]);
    }
    }\n
    """ % (name,  
           channel_width, 
           channel_depth, name, name,
           channel_width,
           channel_depth, name,
           chan2, 
           stop, 
           chan3, 
           channel_depth + 0.01,
           stop,  
           chan2, 
           start_backdepth, 
           chan3,  
           max(y) + start_backheight)


    return code1 + code2