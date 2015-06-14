#!/usr/bin/env python

"""
Compute pair correlation function for Riemann zeros.
Raw implementation of Montgomery's conjecture.

Guilherme S. Franca <guifranca@gmail.com>
12 Jun 2013
Physics Department, Cornell University

"""

from mpmath import *
from numpy import arange

import zeros


def get_zeros(n, filename):
    """We get n zeros from the file."""
    f = open(filename)
    zeros = []
    for i, line in enumerate(f):
        if i >= n:
            break
        zeros.append(mpf(line.strip()))
    return zeros

def bound(t, x):
    """This function is used to define the upper and lower bound
    on the difference of the pair. This comes from the formula
    proposed in Montgomery's conjecture.
    
    """
    return 2.0*pi*x/log(t/2.0/pi/e)

def pair_correlation(zeros, t, alpha, beta):
    """Compute the pairs according to Montgomery's conjecture.
    Left hand side of his equation.
    
    """
    summatory = 0
    minimum = bound(t, alpha)
    maximum = bound(t, beta)
    m = len(zeros)
    for i in range(m-1):
        for j in range(i+1, m):
            delta = zeros[j] - zeros[i]
            if  minimum < delta <= maximum:
                summatory += 1
            elif delta > maximum:
                break
    #x = (alpha + beta)/2.0
    return summatory

def gue_correlation(alpha, beta):
    """Compute the GUE 2-point correlation function."""
    f = lambda x: 1.0 - power(sin(pi*x)/(pi*x), 2)
    res = quad(f, [alpha, beta])
    #x = (alpha + beta)/2.0
    return res

def main(n, alpha, step, zeros_file, outfile):
    """Generate a table with the values to be ploted.
    We have three columns corresponding to 
        
        x, pair_correlation, gue_correlation

    Arguments: 
    
        n (integer) -> the number of last root
        alpha (2 element list) -> range of values to compute the difference
        step (float) -> defines beta = alpha + step
        zeros_file (string) -> filename to take the roots from
        outfile (string) -> filename to output the table

    Exemple of good values to plot:
        n = 1000
        alpha = (0.00, 1.95)
        step = 0.05
        ifile = 'zeros1.txt'
        ofile = 'pair_corr.txt'
    
    """    
    o = open(outfile, 'w')
    alphas = arange(alpha[0], alpha[1], step)
    betas = arange(alpha[0]+step, alpha[1]+step, step)
    somezeros = get_zeros(n, zeros_file)
    t = zeros.zerow(n)
    for a, b in zip(alphas, betas):
        x = (a+b)/2.0
        corr = mpf(pair_correlation(somezeros, t, a, b))/mpf(n)/step
        gue = gue_correlation(a, b)/step
        o.write('%.4f\t%.10f\t%.10f\n' % (x, corr, gue))
        print x

