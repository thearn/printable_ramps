import cv2
import numpy as np
import pylab
from scipy.ndimage.filters import gaussian_filter1d
from fit import fit_multiple
from IPython.display import HTML
from cycloid import get_times

def Animate_frame(Ys, x, t, names, times=[]):
    colors = ["b", "g", "r", "y", "k"]
    for i, y in enumerate(Ys):
        name = names[i]
        color = colors[i]
        if len(times):
            T = times[i]
        else:
            T = get_times(x, y)
        idx = np.searchsorted(T,t)
        xx,yy = x[idx], y[idx]

        pylab.title("$t=%2.3f$" % t)
        pylab.plot(x,y, "%s-" % color)
        markers = False
        if xx != x[-1]:
            pylab.plot(xx, yy, "%so" % color, markersize=10, label=name,
                        markeredgecolor="k", markeredgewidth=2)
            markers=True
    if markers:
        pylab.legend(numpoints=1)


def show_stl(fn):
    """
    Helper method for the notebook to display STL files inline.
    """

    input_form = """
        <canvas id="cv" style="border: 1px solid;" width="750" height="400">
            It seems you are using an outdated browser that does not support canvas :-(
        </canvas>
    """

    javascript = """
    <script type="text/javascript" src="static/jsc3d/jsc3d.js"></script>
    <script type="text/javascript" src="static/jsc3d/jsc3d.webgl.js"></script>
    <script type="text/javascript" src="static/jsc3d/jsc3d.touch.js"></script>
    <script type="text/javascript">
            var viewer = new JSC3D.Viewer(document.getElementById('cv'));
            viewer.setParameter('SceneUrl',         '%s.stl');
            viewer.setParameter('ModelColor',       '#CAA618');
            viewer.setParameter('BackgroundColor1', '#E5D7BA');
            viewer.setParameter('BackgroundColor2', '#383840');
            viewer.setParameter('RenderMode',       'flat');
            viewer.init();
            viewer.update();
        </script>
    """ % fn

    return HTML(input_form + javascript)

def smooth_plot(x, y, a, A, B):
    """
    Helper function for the notebook smoothing widget.
    """
    x = np.linspace(A[0], B[0], x.size)
    fig = pylab.figure()
    y_smooth = gaussian_filter1d(np.array(y), a, mode="nearest")
    y, y_smooth = fit_multiple([y, y_smooth], A, B, offset=False)

    pylab.plot(x, y, label="Drawn")
    pylab.plot(x, y_smooth, "k--", label="Smoothed")
    pylab.legend()
    mn = min([y.min(), y_smooth.min()])
    mx = max([y.max(), y_smooth.max()])
    pylab.text(A[0], A[1], "A", fontsize=20)
    pylab.text(B[0], B[1], "B", fontsize=20)
    #axes = pylab.gca()
    #axes.get_xaxis().set_visible(False)
    #axes.get_yaxis().set_visible(False)

    pylab.ylim(mn-15, mx+15)
    pylab.xlim(A[0]-15, B[0]+15)
    return y_smooth


drawing = False # true if mouse is pressed
def get_sketch(A, B, n_points):
    """
    Function to grab the mouse-driven curve, using OpenCV.
    """

    run = B[0] - A[0]
    drop = A[1] - B[1]

    a1, a2 = 15, 100
    b1, b2 = 485, 400
    run0 = b1 - a1
    drop0 = b2 - a2
    m = drop/float(run)

    if m < drop0/float(run0):
        scale = run0/float(run)
        b1 = int(a1 + scale*run)
        b2 = int(a2 + scale*drop)
    else:
        scale = drop0/float(drop)
        b1 = int(a1 + scale*run)
        b2 = int(a2 + scale*drop)

    ix,iy = -1,-1

    X,Y = [],[]

    def draw_circle(event,x,y,flags,param):
        """
        Mouse handler callback
        """
        global ix,iy,drawing,mode

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            X.append(x)
            Y.append(y)

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                cv2.circle(img,(x,y),3,(0,0,0),-1)
                X.append(x)
                Y.append(y)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            cv2.circle(img,(x,y),3,(0,0,0),-1)
            X.append(x)
            Y.append(y)

    N, M = 512, 700
    img = 255*np.ones((M,N,3), np.uint8)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_circle)

    cv2.circle(img,(a1,a2),5,(0,255,0),-1)
    cv2.circle(img,(b1,b2),5,(0,255,0),-1)

    instr = " - Sketch a path between A and B"
    instr_done = " - Press `Esc` when finished"
    del_instr = "- Press `d` to start over"
    cv2.putText(img,instr, (50,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0))
    cv2.putText(img,instr_done, (50,45), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0))
    cv2.putText(img,del_instr, (61,70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0))

    cv2.putText(img,"A", (a1,a2), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
    cv2.putText(img,"B", (b1,b2), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

    while(1):
        cv2.imshow('image',img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        elif k == 100:
            X, Y = [], []
            img = 255*np.ones((M,N,3), np.uint8)
            cv2.circle(img,(a1,a2),5,(0,255,0),-1)
            cv2.circle(img,(b1,b2),5,(0,255,0),-1)

            cv2.putText(img,instr, (50,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0))
            cv2.putText(img,instr_done, (50,45), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0))
            cv2.putText(img,del_instr, (61,70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0))

            cv2.putText(img,"A", (a1,a2), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
            cv2.putText(img,"B", (b1,b2), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

    cv2.destroyAllWindows()

    X, Y = zip(*sorted(zip(X, Y)))
    X = np.array(X)
    Y = np.array(Y)

    # resample the collected points uniformly in x
    x = np.linspace(X.min(), X.max(), n_points)
    y = np.interp(x, X, Y)

    return x, y

if __name__ == "__main__":
    A = [0, 95.0] # Start point
    B = [529, 1.0] # End point
    x,y = get_sketch(A, B, 1000)
    pylab.plot(x,-y)
    pylab.show()