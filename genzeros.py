#!/usr/bin/env python

"""This file uses mainly the zeros module to generate Riemann zeros.

It can generate a file with the Riemann zeros by solving the transcendental
equation or the Lambert based formula. It can generate zeros starting
from the middle of the critical line. It can also compare two files
of zeros, generate specific Riemann zeros, replace bad zeros in a file, etc.
See --help for a full description.

author: Guilherme S. Franca <guifranca@gmail.com>
date: Jul, 29, 2013
Cornell University, Physics Department

"""

import optparse

from lib import zeros

if __name__ == '__main__':
    usage = """
%prog -m 1 -n 50 goodzeros50.txt
%prog -m 1 -n 50 -l lambert50.txt
%prog -o -p 584758 -f zeros3.txt odlyzko_zeros.txt
%prog -c -d 4 -q 1 zeros1.txt zeros2.txt diff_file.txt
%prog -s -i list_zeros.txt output.txt
%prog -r -q 1 -x line_numbers.txt -y new_zeros.txt original.txt new_one.txt
%prog -z -f zeros.txt -i indexes.txt output.txt

See the description for a list of complete options."""
    desc = """\
This program generate zeros through the Lambert formula or by
calculating the numerical solution the the y-Arg transcendental equation.
It can also have other options. See the description of each one.
"""
    parser = optparse.OptionParser(usage=usage, description=desc)
    parser.add_option('-m', '--lowest', dest='lowest', 
                      action='store', type='int',
                      help='Lowest index of the first zero.')
    parser.add_option('-n', '--highest', dest='highest', 
                      action='store', type='int',
                      help='Highest index of the last zero.')
    parser.add_option('-l', '--lambert', dest='lambert', action='store_true',
                      default=False, 
                      help='Compute using Lambert based formula.')
    parser.add_option('-o', '--odlyzko', dest='odlyzko', action='store_true',
                      default=False, 
                      help='Build zeros from Odlyzko.')
    parser.add_option('-p', '--prefix', dest='prefix', action='store',
                      type='float', default=0, help='Prefix to sum Odlyzko '\
                      'zeros. Should only be used with --odlyzko option.')
    parser.add_option('-f', '--file', dest='odlyzko_file', action='store',
                      help="Filename containing Odlyzko's zero. It is also "\
                      "used with -z option.")
    parser.add_option('-c', '--compare', dest='compare', action='store_true',
                      default=False, help="Compare two filenames to a given "\
                      "decimal place of precision.")
    parser.add_option('-d', '--decimal', dest='decimal', action='store',
                      default=4, help="Precision used with --compare option.")
    parser.add_option('-q', '--first', dest='first', action='store',
                      default=1, type='int', 
                      help="First index to compute the difference. Also "\
                      "used with -r option.")
    parser.add_option('-s', '--specific', dest='specific', action='store_true',
                      help="Find specific zeros. A file with which ones must "\
                      "be passed.")
    parser.add_option('-i', '--indexes', dest='indexes', action='store',
                      help="File name with the indexes to generate zeros for "\
                      "-s option. Also used with -z option.")
    parser.add_option('-r', '--replace', dest='replace', action='store_true',
                      default=False, help="Replace some lines in file "\
                      "containing zeros.")
    parser.add_option('-x', '--linenumbers', dest='linenumbers', action='store',
                      help="File name containing the line numbers to be "\
                      "replaced. Only use with -r option.")
    parser.add_option('-y', '--newzeros', dest='newzeros', action='store',
                      help="File name containing the new zeros corresponding "\
                      "to line numbers in file -x option.")
    parser.add_option('-z', '--pathological', dest='fix_pathological', 
                      action='store_true', default=False, 
                      help="Try to fix pathological zeros. Must set -f and "\
                      "-i options.")
    options, args = parser.parse_args()

    if options.odlyzko:
        if not options.prefix:
            parser.error('You must set the --prefix option.')
        if not options.odlyzko_file:
            parser.error('You must set --file option.')
        if not args:
            parser.error('You need to pass an output file name.')
        zeros.odlyzko(options.odlyzko_file, args[0], options.prefix)
    elif options.compare:
        if not options.decimal:
            print "Warning: you didn't specify --decimal so "\
                  "we are using 4 decimal places."
        if len(args) < 3:
            parser.error('You must pass file1 and file2 and file3 '\
                         'as arguments.')
        zeros.diff_zeros(args[0], args[1], args[2], first_index=options.first)
    elif options.specific:
        if not options.indexes:
            parser.error("You must pass a file with the indexes.")
        if not args:
            parser.error("No output file.")
        indexes_list = [int(x) for x in open(options.indexes)]
        zeros.good_specific(indexes_list, args[0])
    elif options.replace:
        if not (options.linenumbers and options.newzeros):
            parser.error("You must pass a file with the line "\
            "numbers and the corresponding file with new zeros. "\
            "See -x and -y options.")
        if len(args) < 2:
            parser.error("No files. You must pass the original file with "\
            "zeros and the name of new file for output, in this order.")
        zeros.replace_badones(args[0], args[1], 
                              options.linenumbers, options.newzeros,
                              options.first)
    elif options.fix_pathological:
        if not (options.odlyzko_file and options.indexes):
            parser.error("You must set -f and -i options.")
        if len(args) < 1:
            parser.error("No output file chosen.")
        zeros.fix_pathological(options.odlyzko_file, options.indexes, args[0])
    else:
        if not (options.lowest and options.highest):
            parser.error('You must set --lowest and --highest options.')
        if not args:
            parser.error('You must pass a filename for output.')
        if options.lambert:
            zeros.approxzeros(options.lowest, options.highest, args[0])
        else:
            zeros.goodzeros(options.lowest, options.highest, args[0])

