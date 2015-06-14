#!/usr/bin/env python

"""Construct the prime number counting formula with Riemann zeros.

author: Guilherme S. Franca <guifranca@gmail.com>
date: Jul, 29, 2013
Cornell University, Physics Department

"""

import optparse

from lib import prime
from lib import graphs

if __name__ == '__main__':
    usage = """
%prog -i zeros.txt -n 50 -x 10 -d 0.01 output.txt
%prog -g -i table.txt output.txt
%prog -s -i zeros.txt -n 1000 10\
"""
    desc = """\
This program computes the number of primes less than -x. It generates
a table where the first column is x, the second the true pi(x) function,
the third pi(x) using numerical Riemann zeros in file zeros.txt, the fourth
is the approximation given by Lambert formula.
"""
    parser = optparse.OptionParser(usage=usage, description=desc)
    parser.add_option('-i', '--input', dest='input_file', 
                      action='store', 
                      help='Input file with zeros or table of prime counting'\
                      'to generate the graph with -g option.')
    parser.add_option('-n', '--numzeros', dest='numzeros', 
                      action='store', type='int',
                      help='Number of zeros used.')
    parser.add_option('-x', '--xvalue', dest='xvalue', action='store',
                      type='float', help='Primes less then x. '\
                      'Choose a number bigger than 2.')
    parser.add_option('-d', '--step', dest='step', action='store',
                      type='float', help='Step to go from 2...-x.')
    parser.add_option('-g', '--graph', dest='graph', action='store_true',
                      default=False, help='Make graph.')
    parser.add_option('-b', '--both', dest='both', action='store_true',
                      default=False, help='Plot both numerical and Lambert '\
                      'zeros in the same graph.')
    parser.add_option('-l', '--lambert', dest='lambert', action='store_true',
                      default=False, help='Plot only Lambert.')
    parser.add_option('-s', '--specific', dest='specific', action='store_true',
                      default=False, help='Compute the prime number to a '\
                      'specific value x passed as argument. Use -i file '\
                      'as the table of zeros. The -n option set the number '\
                      'of zeros used.')
    options, args = parser.parse_args()

    if options.graph:
        if not args:
            parser.error('No output file.')
        if not (options.input_file):
            parser.print_help()
            parser.exit()
        graphs.plot_prime(args[0], options.input_file, lambert=options.lambert,
                            both=options.both)
    elif options.specific:
        if not args or type(float(args[0])) != type(2.1):
            parser.error('The argument must be a float number.')
        if not (options.input_file and options.numzeros):
            parser.print_help()
            parser.exit()
        a, b = prime.single_pi(float(args[0]), options.numzeros, 
                               options.input_file)
        print "pi(x) from Riemann zeros: %.5f" % a
        print "pi(x) from other method: %.5f" % b
    else:
        if not args:
            parser.error('No output file.')
        if not (options.input_file and options.numzeros and options.xvalue \
                and options.step):
            parser.print_help()
            parser.exit()
        prime.table_pi(options.xvalue, options.step, options.input_file, 
                       options.numzeros, args[0])
 
