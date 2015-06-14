#!/usr/bin/env python

"""Generate graph of Lambert based formula with Riemann zeros dots.

author: Guilherme S. Franca <guifranca@gmail.com>
date: Jul, 29, 2013
Cornell University, Physics Department

"""

import optparse

from lib import graphs

def zeros_graph(input_file, output, m, n, jump, ticks, zoom_n, left, right): 
    """m: the first zero, n: the last zero, jump: the interval to create
    the dots, jump_ticks: the interval to show ticks, zoom_n: the number
    of roots in the zoom graph.
    
    """
    z = graphs.Zeros(input_file)
    z.m = m
    z.n = n
    z.jump = jump
    z.jump_ticks = ticks
    z.zoom_n = zoom_n
    z.zoom_x = 0.45
    z.zoom_width = 0.45
    z.margin_left = left
    z.margin_right = right
    z.make_graph(output)


if __name__ == '__main__':
    usage = """
%prog -i zeros.txt -m 1 -n 500 -j 10 -t 50 -z 10 output.pdf

This is just an example of parameters. See the complete description
for details."""
    desc = """\
This program plot the zeros predicted by an exact solution, Lambert
formula, and the numerical solution of the transcendental equation."""
    parser = optparse.OptionParser(usage=usage, description=desc)
    parser.add_option('-i', '--input', dest='input_file', 
                      action='store', 
                      help='Filename for input. Must contain zeros.')
    parser.add_option('-m', '--lowest', dest='lowest', action='store',
                      type='int', 
                      help='The index of lowest zero.')
    parser.add_option('-n', '--highest', dest='highest', action='store', 
                      type='int',
                      help='The index of highest zero.')
    parser.add_option('-j', '--jump', dest='jump', action='store', 
                      type='int',
                      help='The interval between dots.')
    parser.add_option('-t', '--ticks', dest='ticks', action='store', 
                      type='int',
                      help='The interval between ticks.')
    parser.add_option('-z', '--zoom', dest='zoom', action='store', 
                      type='int',
                      help='The number of roots in the zoom graph.')
    parser.add_option('-l', '--left', dest='left', action='store', 
                      type='float', default=0.0,
                      help='Margin left.')
    parser.add_option('-r', '--right', dest='right', action='store', 
                      type='float', default=0.0,
                      help='Margin right.')
    parser.add_option('-p', '--xhalf', dest='xhalf', action='store_true', 
                      default=False, help='Graph of x=1/2.')
    parser.add_option('-q', '--mbounded', dest='mbounded', action='store_true', 
                      default=False, help='Graph to show that m is bounded.')
    parser.add_option('-x', '--cos', dest='cos', action='store_true', 
                      default=False, help='Graph to show the cos/sin.')
    options, args = parser.parse_args()

    if not args:
        parser.error('No output file.')

    if options.xhalf:
        graphs.proof_xhalf(args[0])
    elif options.mbounded:
        graphs.proof_mbounded(args[0])
    elif options.cos:
        graphs.plot_cos_sin(args[0])
    else:
        if not (options.input_file and options.lowest and \
                options.highest and options.jump and \
                options.ticks and options.zoom):
            parser.print_help()
            parser.exit()
        zeros_graph(options.input_file, args[0], options.lowest, 
                    options.highest, options.jump, options.ticks, 
                    options.zoom, options.left, options.right)

