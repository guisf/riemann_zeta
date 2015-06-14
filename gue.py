#!/usr/bin/env python

"""Compute stronger version of Montgomery's pair correlation conjecture.

author: Guilherme S. Franca <guifranca@gmail.com>
date: Jul, 29, 2013
Cornell University, Physics Department

"""

import optparse

from lib import gue2

if __name__ == '__main__':
    usage = """
%prog -i zeros.txt -m 1 -n 1000 -a 1.0 -b 3.05 -s 0.05 -f 1 gue_output.txt \
"""
    desc = """\
This program computes the pair correlation function and
the 2-point correlation function in GUE. A table is generated and printed
to the output file."""
    parser = optparse.OptionParser(usage=usage, description=desc)
    parser.add_option('-i', '--input', dest='input_file', 
                      action='store', 
                      help='Input file with zeros.')
    parser.add_option('-m', '--lowest', dest='lowest', 
                      action='store', type='int',
                      help='Lowest index of the first zero.')
    parser.add_option('-n', '--highest', dest='highest', 
                      action='store', type='int',
                      help='Highest index of the last zero.')
    parser.add_option('-a', '--alphamin', dest='alphamin', action='store',
                      type='float', help='Minimum value of alpha.', 
                      default=-1)
    parser.add_option('-b', '--alphamax', dest='alphamax', action='store',
                      type='float', help='Maximum value of alpha.')
    parser.add_option('-s', '--step', dest='step', action='store',
                      type='float', help='Step between beta and alpha.')
    parser.add_option('-f', '--first', dest='first', action='store',
                      default=0, type='int', 
                      help='The index of the first zero.')
    options, args = parser.parse_args()

    if not args:
        parser.error('No output file.')
    if not (options.input_file and options.lowest and options.highest and
            options.alphamin != -1 and options.alphamax and options.step):
        parser.print_help()
        parser.exit()

    gue2.main(options.highest, options.lowest, 
              [options.alphamin, options.alphamax], options.step, 
              options.input_file, args[0], options.first)
 
