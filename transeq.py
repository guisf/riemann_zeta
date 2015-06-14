#!/usr/bin/env python

"""Generate a graph to explain how to deal with the transcendental equation.

author: Guilherme S. Franca <guifranca@gmail.com>
date: Jul, 29, 2013
Cornell University, Physics Department

"""

import optparse

from lib import graphs

def transcendental_plot(output):
    t = graphs.Transcendental()
    t.n = 573
    t.left = 10
    t.right = 10
    t.step = 0.02
    t.xmin = 895
    t.xmax = 914
    t.ymin = -8
    t.ymax = 8
    t.zoom_left = 0.30
    t.zoom_right = 0.2
    t.zoom_step = 0.005
    t.zoom_xmin = 904.6
    t.zoom_xmax = 904.8
    t.zoom_ymin = -0.7
    t.zoom_ymax = 0.7
    t.zoom_x = 0.5
    t.zoom_y = 0.125
    t.zoom_width = 0.4
    t.make_graph(output)

if __name__ == '__main__':
    usage = "%prog output.pdf"
    desc = """\
Plot the transcendental equation which provides the Riemann zeros.
Ilustrate how the exact solution is modified by the Arg(Zeta(0.5+iy))
term."""
    parser = optparse.OptionParser(usage=usage, description=desc)
    options, args = parser.parse_args()

    if not args:
        parser.error('No output file.')

    transcendental_plot(args[0])

