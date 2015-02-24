from solid import *
import numpy as np
import subprocess

def multiple_ramp_strings(Rs, width=30):
    """
    Joins together source code strings for multiple ramps.
    """
    s = ''.join(Rs)

    cp = ['\ntranslate([0, %i, 0]) ramp%i();' % (i*width, i) for i in xrange(len(Rs))]

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
    wall_width = 5,
    length = 50, 
    n = 100,
    thickness = 2,
    start_backheight = 2,
    start_backdepth = 10,
    channel_width = 10,
    channel_depth = 3,
    endstop_thickness=5,
    endstop_height=16,
    name="ramp"):
    
    """
    Generate the OpenSCAD source code for a series of marble ramps with
    curvatures given by the points of input array y.

    y can be a single curve or list of curves.
    """

    if hasattr(y, '__iter__') and hasattr(y[0], '__iter__'):
        codes = []
        max_y = max([y_[-1] for y_ in y])
        for i, y_ in enumerate(y[::-1]):
            code = ramp(y_, length=length, n=n, thickness=thickness,
                        start_backheight=start_backheight,
                        start_backdepth=start_backdepth,
                        channel_width=channel_width,
                        channel_depth=channel_depth,
                        endstop_thickness = endstop_thickness,
                        endstop_height = max_y + endstop_height,
                        wall_width = wall_width,
                        name = name + str(i))
            codes.append(code)
        return multiple_ramp_strings(codes, width = channel_width + 2*wall_width)
    
    if not isinstance(x, np.ndarray):
        x = np.linspace(0, length, n)

    if len(y) != n:
        small_x = np.linspace(0, length, len(y))
        y = np.interp(x, small_x, y)

    if y[0] >  y[1]:
        y = y[::-1]

    y += thickness
    stop = x[-1]

    pts = [list(i) for i in zip(x,y)]

    pts.extend([[x[-1], thickness], [x[-1], 0], [0,0]])

    d = polygon(pts)

    d = linear_extrude(height="wall_width")(d)

    d = rotate([90,0,0])(d)

    code1 = ("module %s_curve(wall_width) { " % name) + scad_render( d) + " }\n\n"
    code1 = code1.replace('"wall_width"', "wall_width")

    code2 = "module %s() {\n union() {\n"  % name
    code2 += "   translate([0, -%f, %f]) %s_curve(%f);\n" % (channel_width, channel_depth, name, wall_width)
    code2 += "   %s_curve(%f);\n" % (name, channel_width)
    code2 += "   translate([0, %f, %f]) %s_curve(%f);\n" % (wall_width, channel_depth, name, wall_width)
    code2 += "   translate([0, %f, 0]) cube([%f, %f, %f]);\n" % (-(channel_width + wall_width), stop, channel_width + 2*wall_width, channel_depth + 0.01)
    code2 += "   translate([%f, %f, 0]) cube([%f, %f, %f]);\n" % (stop, -(channel_width + wall_width), start_backdepth, channel_width + 2*wall_width, max(y) + start_backheight)
    code2 += "   translate([-%f, -%f, 0]) cube([%f, %f, %f]); }\n}\n\n" % (endstop_thickness, (channel_width + wall_width), endstop_thickness, channel_width + 2*wall_width, endstop_height)

    return code1 + code2

if __name__ == "__main__":
    from cycloid import cycloid
    A = [0, 95.0] # Start point
    B = [229, 1.0] # End point
    from fit import fit_multiple
    x,y = cycloid(A,B,100)
    y2 = np.linspace(A[0], B[0], 100)

    y,y2 = fit_multiple([y,y2], A, B)
    print ramp([y,y2], length = B[0] - A[0], thickness = 10, channel_depth=1.5, wall_width=2, channel_width=10, endstop_height=40)




