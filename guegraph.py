#!/usr/bin/env python

"""Generate GUE graph based on a text file with the data.

author: Guilherme S. Franca <guifranca@gmail.com>
date: Jul, 29, 2013
Cornell University, Physics Department

"""

import optparse

from lib import graphs

def gue_graph(input_file, output, title, xmin=0.01, xmax=1.9, ymin=0, 
              ymax=1.2, colorline='#708DFF', colordot='#FF0000', linewidth=2,
              dotsize=5, symbol='o', legend1='', legend2=''):
    m = graphs.Montgomery(input_file)
    m.title = r'%s' % title
    m.xmin = xmin
    m.xmax = xmax
    m.ymin = ymin
    m.ymax = ymax
    m.color_gue = colorline
    m.color_points = colordot
    m.markersize = dotsize
    m.linewidth = linewidth
    m.symbol = symbol
    m.legend1 = legend1
    m.legend2 = legend2
    m.make_graph(output)


if __name__ == '__main__':
    usage = """
%prog -i gue.txt -t '$n=1\dotsc 10^3$' -a 0 -b 3 -c 0 -d 1.2 -s 3 graph.pdf

See the description for a list of complete options."""
    desc = """Make a plot of GUE pair correlation conjecture."""
    parser = optparse.OptionParser(usage=usage, description=desc)
    parser.add_option('-i', '--input', dest='input_file', 
                      action='store', 
                      help='Input file with GUE data table.')
    parser.add_option('-t', '--title', dest='title', action='store',
                      type='str', help='Title for the graph (LaTeX format).')
    parser.add_option('-a', '--xmin', dest='xmin', default=0.02,
                        action='store', type='float',
                        help='The value of x-axis minimum.')
    parser.add_option('-b', '--xmax', dest='xmax', default=1.9,
                        action='store', type='float', 
                        help='The value of x-axis maximum.')
    parser.add_option('-c', '--ymin', dest='ymin', default=0,
                        action='store', type='float', 
                        help='The value of y-axis minimum.')
    parser.add_option('-d', '--ymax', dest='ymax', default=1.2,
                        action='store', type='float', 
                        help='The value of y-axis maximum.')
    parser.add_option('-l', '--colorline', dest='colorline', action='store',
                      default='b', help="Color of the line (optional).")
    parser.add_option('-w', '--linewidth', dest='linewidth', action='store',
                      default=1, type=float, 
                      help="Width of the line (optional).")
    parser.add_option('-p', '--colordots', dest='colordots', action='store',
                      default='r', help="Color of the dots (optional).")
    parser.add_option('-s', '--dotssize', dest='dotssize', action='store',
                      default=4, type=float,
                      help="Size of the dots (optional).")
    parser.add_option('-m', '--marker', dest='marker', action='store',
                      default='o',
                      help="The symbol for the dots (optional).")
    parser.add_option('-x', '--legend1', dest='legend1', action='store',
                      default='',
                      help="Legend for the curve (optional).")
    parser.add_option('-y', '--legend2', dest='legend2', action='store',
                      default='',
                      help="Legend for the dots (optional).")
    options, args = parser.parse_args()

    if not args:
        parser.error('No output file. Must be PDF.')
    if not (options.input_file and options.title):
        parser.print_help()
        parser.exit()

    gue_graph(options.input_file, args[0], options.title, options.xmin, 
              options.xmax, options.ymin, options.ymax, options.colorline,
              options.colordots, options.linewidth, options.dotssize,
              options.marker, options.legend1, options.legend2)

