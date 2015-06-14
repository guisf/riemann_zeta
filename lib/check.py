#!/usr/bin/env python 

from mpmath import *
import zeros
import sys


mp.dps = 200
#pretty = True

zeta_zeros = [zetazero(n).imag for n in range(1, 100+1)]

for n, zz in enumerate(zeta_zeros):
    print '%.10f' % zeros.transeqe(n+1, power(10, -8), zz)

