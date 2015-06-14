#!/usr/bin/env python

"""
This file contains the classes to generate our plots.

Guilherme S. Franca <guifranca@gmail.com>
June 25 2013
Cornell University, Physics Department

"""

import matplotlib
#matplotlib.use('PDF') # in case we run on a remote computer
import functools
import pylab
import mpmath

import zeros


pylab.rc('lines', linewidth=1, antialiased=True, markeredgewidth=0.1)
pylab.rc('font', family='computer modern roman', style='normal', 
         weight='normal', serif='computer modern sans serif', size=10)
pylab.rc('text', usetex=True)
pylab.rc('text.latex', preamble=[
        '\usepackage{amsmath,amsfonts,amssymb,relsize,cancel}'])
pylab.rc('axes', linewidth=0.5, labelsize=10)
pylab.rc('xtick', labelsize=10)
pylab.rc('ytick', labelsize=10)
#pylab.rc('legend', numpoints=1, fontsize=10, handlelength=0.5)
pylab.rc('legend', numpoints=1, fontsize=12)
fig_width_pt = 455.0 / 1.5 # take this from LaTeX \textwidth in points
inches_per_pt = 1.0/72.27
golden_mean = (mpmath.sqrt(5.0)-1.0)/2.0
fig_width = fig_width_pt*inches_per_pt
fig_height = fig_width*golden_mean
pylab.rc('figure', figsize=(fig_width, fig_height))
legend_line = 0.5

class Transcendental:
    """Plot various parts of the transcendental equation to show
    the role of the Arg(Zeta) term. We can see how the exact solution
    given by the Lambert formula is corrected by this term.

    The transcendental equation is plotted for a given `n`, corresponding
    to the n-th Riemann zero.

    Adjust the parameters properly. You can see them in __init__ function.
    
    """

    def __init__(self):
        self.n = 573
        self.left = 10
        self.right = 10
        self.step = 0.05
        self.xmin = 0
        self.xmax = 0
        self.ymin = -8
        self.ymax = 8
        
        self.zoom_left = 0.15
        self.zoom_right = 0.1
        self.zoom_step = 0.005
        self.zoom_xmin = 0
        self.zoom_xmax = 0
        self.zoom_ymin = -0.6
        self.zoom_ymax = 0.6
        self.zoom_x = 0.58
        self.zoom_y = 0.125
        self.zoom_width = 0.33
        
        #self.color_partial = '#708DFF'
        #self.color_arg = '#8CFF6F'
        #self.color_complete = '#FF0000'
        self.color_partial = 'b'
        self.color_arg = 'g'
        self.color_complete = 'r'
        
    def make_graph(self, output):
        approx = zeros.zerow(self.n)
        better = zeros.findzero(self.n)
        if not self.xmin:
            self.xmin = approx - self.left
            self.xmax = self.approx + self.right
        if not self.zoom_xmin:
            self.zoom_xmin = self.approx - self.zoom_left
            self.zoom_xmax = self.approx + self.zoom_right
        zoom_position = [self.zoom_x, self.zoom_y, 
                         self.zoom_width, self.zoom_width*golden_mean]
        
        complete = functools.partial(zeros.transeq, self.n)
        partial = functools.partial(zeros.transeq_first, self.n)
        arg = zeros.argzeta
        
        xvalues = pylab.arange(approx-self.left, 
                               approx+self.right, 
                               self.step)
        ypartial = [partial(y) for y in xvalues]
        ycomplete = [complete(y) for y in xvalues]
        argument = [arg(y) for y in xvalues]
        
        fig = pylab.figure()
        ax = fig.add_subplot(111)
        ax.plot(xvalues, ypartial, color=self.color_partial)
        ax.plot(xvalues, argument, color=self.color_arg)
        ax.plot(xvalues, ycomplete, color=self.color_complete)
        
        ax.set_title(r'$n=%i,\ \tilde{y}_n=%.2f,\ y_n=%.12f$'% \
                        (self.n, approx, better))
        l = ax.legend([
    #r'$\tfrac{y}{2\pi}\log\left(\tfrac{y}{2\pi e}\right)+\tfrac{11}{8}-n$', 
        r'$F_n(y)$', 
        r'$S(y)$', 
        r'$F_n(y)+S(y)$'], loc=2)
        l.get_frame().set_linewidth(0.0)
        l.get_frame().set_fill(False)
        #ax.grid(True)
        
        ax.annotate('', xy=(approx, 0), xycoords='data', 
                    xytext=(20,-20), textcoords='offset points',
                    arrowprops=dict(arrowstyle='->'))
        
        ax.spines['left'].set_position(('outward', 10))
        ax.spines['bottom'].set_position(('outward', 10))
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        
        ax.set_xlim(float(self.xmin), float(self.xmax))
        ax.xaxis.set_ticks([self.xmin, approx, self.xmax])
        ax.xaxis.set_ticklabels([r'$%i$' % self.xmin,
                                 r'$\tilde{y}_n$', 
                                 r'$%i$' % self.xmax])
        if self.ymin and self.ymax:
            ax.set_ylim(self.ymin, self.ymax)
        
        xvalues = pylab.arange(approx-self.zoom_left, 
                               approx+self.zoom_right, 
                               self.zoom_step)
        ypartial = [partial(y) for y in xvalues]
        ycomplete = [complete(y) for y in xvalues]
        argument = [arg(y) for y in xvalues]
        
        axins = pylab.axes(zoom_position)
        axins.grid(True)
        axins.set_axisbelow(True)
        axins.plot(xvalues, ypartial, color=self.color_partial)
        axins.plot(xvalues, argument, color=self.color_arg)
        axins.plot(xvalues, ycomplete, color=self.color_complete)
        axins.xaxis.set_ticks([approx, better])
        axins.xaxis.set_ticklabels([r'$\tilde{y}_n$', r'$y_n$'])
        axins.set_xlim(float(self.zoom_xmin), float(self.zoom_xmax))
        if self.zoom_ymin and self.zoom_ymax:
            axins.yaxis.set_ticks([self.zoom_ymin, 0.0, self.zoom_ymax])
        pylab.savefig(output, bbox_inches='tight')


class Zeros:
    """Plot zeros comparison between Lambert formula and 
    numerical solution of transcendental equation.

    We can see the zeros oscillating around the line.
    
    """

    def __init__(self, input_file):
        self.m = 1
        self.n = 35
        self.input_file = input_file
        self.jump = 5
        self.jump_ticks = 10
        self.symbol = 'o'
        self.zoom_n = 10
        self.zoom_x = 0.42
        self.zoom_y = 0.13
        self.zoom_width = 0.4
        self.margin_left = 5
        self.margin_right = 5
        
    def make_graph(self, output):
        xtrans = range(self.m, self.n+1, 1)
        ytrans = []
        for i, l in enumerate(open(self.input_file)):
            if i + 1 < self.m:
                continue
            elif i + 1 > self.n:
                break
            ytrans.append(mpmath.mpf(l.strip()))
        xlambert = pylab.arange(self.m-0.4, self.n+1+0.4, 0.2)
        ylambert = [zeros.zerow(a) for a in xlambert]
        
        fig = pylab.figure()
        ax = fig.add_subplot(111)
        ax.plot(xlambert, ylambert, '-', color='b') 
        ax.plot([xtrans[i] for i in range(len(xtrans)) 
                 if (i+1)%self.jump==0 or i==0], 
                [ytrans[i] for i in range(len(ytrans)) 
                 if (i+1)%self.jump==0 or i==0], self.symbol, 
                color='r', markersize=4)
        ax.set_title(r'$n=%i \dotsc %i$' % (self.m, self.n))
        #l = ax.legend([r'($20$)', r'($11$)'], loc=0)
        #l.get_frame().set_linewidth(0.1)
        #l.get_frame().set_linewidth(0.0)
        #l.get_frame().set_fill(False)
        #l.get_frame().set_alpha(0)

        ax.spines['left'].set_position(('outward', 10))
        ax.spines['bottom'].set_position(('outward', 10))
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.grid(True)
        ax.set_axisbelow(True)
        ax.set_xlim(self.m-self.margin_left, self.n+self.margin_right)
        ax.xaxis.set_ticks(range(self.m, self.n, self.jump_ticks))
        ypoints = [ytrans[i] 
                   for i in range(self.m-1, self.n, self.jump_ticks)]
        ax.yaxis.set_ticks(ypoints)
        ax.yaxis.set_ticklabels([r'$%.4f$' % i for i in ypoints])
    
        first = self.n - self.zoom_n
        last = self.n
        zoom_height = golden_mean * self.zoom_width
        zoom_position = [self.zoom_x, self.zoom_y, 
                         self.zoom_width, zoom_height]
        xlambert = pylab.arange(first-0.2, last+1, 0.5)
        ylambert = [zeros.zerow(a) for a in xlambert]
        xtrans = range(first, last+1, 1)
        ytrans = ytrans[first-1:last+1]
        axins = pylab.axes(zoom_position)
        axins.plot(xlambert, ylambert, '-', color='b')
        axins.plot(xtrans, ytrans, self.symbol, color='r', markersize=4)
        axins.xaxis.set_ticks([])
        axins.yaxis.set_ticks([])
        axins.set_xlim(first-0.2, last+0.2)
        pylab.savefig(output, bbox_inches='tight')


def lambert_dots(output, input_file, m=1, n=400, jump=25, jump_ticks=45,
                 symbol='o', margin_left=5, margin_right=2):
    # take points for the transcendental equation solutions
    # the y values are taken from `input_file`
    xtrans = range(m, n+1, 1)
    ytrans = []
    for i, l in enumerate(open(input_file)):
        if i + 1 < m:
            continue
        elif i + 1 > n:
            break
        ytrans.append(mpmath.mpf(l.strip()))
    
    # take points for lambert approximation
    xmin = m-margin_left
    if xmin < 0:
        xmin = 0.4
    xmax = n+1+margin_right
    xlambert = pylab.arange(xmin, xmax, 0.2)
    ylambert = [zeros.zerow(a) for a in xlambert]
   
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    ax.plot(xlambert, ylambert, '-', color='b') 
    ax.plot([xtrans[i] for i in range(len(xtrans)) if (i+1)%jump==0 or i==0], 
            [ytrans[i] for i in range(len(ytrans)) if (i+1)%jump==0 or i==0], 
            symbol, color='r', markersize=4)
    #ax.set_title(r'$n=%i \dotsc %i$' % (self.m, self.n))
    #ax.xaxis.set_ticks_position('bottom')
    #ax.yaxis.set_ticks_position('left')
    pylab.fill_between(xlambert, ylambert[0], ylambert, color='b', alpha=.10)
    ax.grid(True)
    ax.set_axisbelow(True)
    ax.set_xlim(xmin, xmax-1)
    ax.set_ylim(float(ylambert[0]), float(ylambert[-1]))
    ax.xaxis.set_ticks(range(m, n, jump_ticks))
    ypoints = [ytrans[i] for i in range(0, n-m, jump_ticks)]
    ax.yaxis.set_ticks(ypoints)
    ax.yaxis.set_ticklabels([r'$%.3f$' % i for i in ypoints])
    pylab.savefig(output, bbox_inches='tight')


#lambert_dots('lambert_dots.pdf', 
#             '../data/final_zeros_105/ourzeros105_final.txt')

#lambert_dots('lambert_dots_zoom.pdf', 
#             '../data/final_zeros_105/ourzeros105_final.txt',
#             m=99984, n=100000, jump=1, jump_ticks=3,
#             symbol='o', margin_left=1, margin_right=1)


class Montgomery:
    """Plot Montgomery's conjecture.
    We take the data from some file instead of generating them
    here because it takes considerable time.
    
    """
    def __init__(self, input_file):
        self.input_file = input_file
        self.sep = '\t'
        self.color_gue = '#708DFF'
        self.color_points = '#FF0000'
        self.markersize = 5
        self.linewidth = 2
        self.symbol = 'o'
        self.legend1 = ''
        self.legend2 = ''
        self.title = r'$m=9.0\times 10^4, \ n=1.0\times 10^5$'
        self.xmax = 0 
        self.xmin = 0
        self.ymax = 0
        self.ymin = 0
        self.loc = 4

    def make_graph(self, output):
        f = open(self.input_file)
        values = [[], [], []]
        for l in f:
            a = [mpmath.mpf(x) for x in l.strip().split(self.sep)]
            values[0].append(a[0])
            values[1].append(a[1])
            values[2].append(a[2])
        fig = pylab.figure()
        ax = fig.add_subplot(111)
        ax.plot(values[0], values[2], '-', color=self.color_gue,
                linewidth=self.linewidth)
        ax.plot(values[0], values[1], self.symbol, color=self.color_points, 
                markersize=self.markersize)
        pylab.fill_between(values[0], 0, values[2], color=self.color_gue, 
                           alpha=.10)
        if self.title:
            ax.set_title(r'%s' % self.title)
        leg = []
        if self.legend1:
            leg.append(r'%s' % self.legend1)
        if self.legend2:
            leg.append(r'%s' % self.legend2)
        if leg:
            l = ax.legend([r'RHS (??)', r'LHS (??)'], loc=self.loc, 
                            shadow=True)
            l.get_frame().set_linewidth(0.1)
        if self.xmax:
            ax.set_xlim(self.xmin, self.xmax)
        if self.ymax:
            ax.set_ylim(self.ymin, self.ymax)
        pylab.savefig(output)

def proof_xhalf(output):
    """Graph to show that x=1/2 in RH."""
    f = zeros.xhalf
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    xaxis = pylab.arange(0.0, 1.1, 0.0005)
    yaxis1 = [f(279.2, x) for x in xaxis]
    p1 = ax.plot(xaxis, yaxis1)
    p2 = ax.plot(xaxis, [x-0.5 for x in xaxis], color='r')
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-1.7, 1.7)
    ax.grid(True)
    ax.set_axisbelow(True)
    ax.xaxis.set_ticks([0, 0.4, 0.5, 0.6, 1])
    ax.xaxis.set_ticklabels([r'$0$', r'$x-\epsilon$', r'$\tfrac{1}{2}$', 
                             r'$x+\epsilon$', r'$1$'])
    ax.yaxis.set_ticks([0])
    ax.yaxis.set_ticklabels([r'$0$'])
    l = ax.legend([r'RHS ($19$)', r'LHS ($19$)'], loc=0)
    l.get_frame().set_linewidth(0.0)
    l.get_frame().set_fill(False)
    pylab.savefig(output)

def proof_mbounded(output):
    """Show that m is bounded."""
    f = zeros.almost_transeq
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    xaxis = pylab.arange(0.0, 1.0, 0.0001)
    yaxis1 = [f(x) for x in xaxis]
    p1 = ax.plot(xaxis, yaxis1)
    ax.set_xlim(0, 1.0)
    #ax.xaxis.set_ticks([0, 0.5, 1.0])
    #ax.xaxis.set_ticklabels([r'$0$', r'$\tfrac{1}{2}$', r'$1$'])
    l = ax.legend([r'RHS ($20$)'], loc=0)
    l.get_frame().set_linewidth(0.0)
    l.get_frame().set_fill(False)
    pylab.savefig(output)

def plot_arg(output):
    f = zeros.argzeta
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    xaxis = pylab.arange(0.1, 40.0, 0.1)
    yaxis1 = [f(x) for x in xaxis]
    pylab.fill_between(xaxis, 0, yaxis1, color='b', alpha=.10)
    p1 = ax.plot(xaxis, yaxis1)
    ax.set_xlim(0.0, 40)
    ax.set_ylim(-1, 1)
    #ax.xaxis.set_ticks([0, 0.5, 1.0])
    #ax.xaxis.set_ticklabels([r'$0$', r'$\tfrac{1}{2}$', r'$1$'])
    l = pylab.legend(
    [r'$\tfrac{1}{\pi}\mbox{arg\,}\zeta\left(\tfrac{1}{2}+it\right)$'], 
        loc=2)
    pylab.gca().add_artist(l)
    l.get_frame().set_linewidth(0.0)
    pylab.savefig(output)

def plot_cos_sin(output):
    c = functools.partial(zeros.costheta, 0.5+0.05)
    s = functools.partial(zeros.sintheta, 0.5+0.01)
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    #xaxis = pylab.arange(13.75, 14.5, 0.001)
    xaxis = pylab.arange(20.5, 21.5, 0.001)
    yaxis1 = [c(x) for x in xaxis]
    yaxis2 = [s(x) for x in xaxis]
    p1 = ax.plot(xaxis, yaxis1)
    p2 = ax.plot(xaxis, yaxis2, color='r')
    #ax.set_xlim(13.75, 14.5)
    ax.set_xlim(20.5, 21.5)
    ax.set_ylim(-1.2, 1.2)
    #ax.xaxis.set_ticks([14.1347])
    ax.xaxis.set_ticks([21.022])
    ax.yaxis.set_ticks([-1, 0, 1])
    ax.grid(True)
    ax.set_axisbelow(True)
    #ax.xaxis.set_ticklabels([r'$0$', r'$\tfrac{1}{2}$', r'$1$'])
    #l = ax.legend([r'$\cos\theta(\tfrac{1}{2}+\delta,y)$', 
    #               r'$\sin\theta(\tfrac{1}{2}+\delta,y)$'], loc=(0.0, 0.6))
    l = ax.legend([r'$\cos\theta(\tfrac{1}{2}+\delta,y)$', 
                   r'$\sin\theta(\tfrac{1}{2}+\delta,y)$'], loc=(0.0, 0.1))
    l.get_frame().set_linewidth(0.0)
    l.get_frame().set_fill(False)
    pylab.savefig(output)

def plot_counting(output):
    f = zeros.counting_function
    g = zeros.counting_function_smooth
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    xaxis = pylab.arange(0.0, 40.0, 0.05)
    yaxis1 = [f(x) for x in xaxis]
    yaxis2 = [g(x) for x in xaxis]
    p1 = ax.plot(xaxis, yaxis1)
    p2 = ax.plot(xaxis, yaxis2, '--', color='r')
    pylab.fill_between(xaxis, -0.5, yaxis1, color='b', alpha=.10)
    ax.set_xlim(0.0, 40)
    ax.set_ylim(-0.5, 6.4)
    #ax.xaxis.set_ticks([0, 0.5, 1.0])
    #ax.xaxis.set_ticklabels([r'$0$', r'$\tfrac{1}{2}$', r'$1$'])
    l = pylab.legend([r'$N_0(T)$', r'\tfrac{T}{2\pi}\log\left(\tfrac{T}{2\pi e}\right) + \tfrac{7}{8}$'], loc=0)
    pylab.gca().add_artist(l)
    l.get_frame().set_linewidth(0.0)
    pylab.savefig(output)

plot_counting("counting_func.pdf")

def plot_arge(output):
    f = zeros.argzeta
    fe = functools.partial(zeros.argzetae, 1.0/20.0)
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    xaxis = pylab.arange(1004, 1011, 0.02)
    yaxis1 = [f(x) for x in xaxis]
    yaxis2 = [fe(x) for x in xaxis]
    p1 = ax.plot(xaxis, yaxis1)
    p2 = ax.plot(xaxis, yaxis2, '--', color='r')
    #ax.set_xlim(0.0, 40)
    ax.set_ylim(-1.2, 1.2)
    ax.xaxis.set_ticks([1006, 1008, 1010])
    ax.xaxis.set_ticklabels([r'$1006$', r'$1008$', r'$1010$'])
    #l = pylab.legend(
    #[r'$\tfrac{1}{\pi}\arg\zeta\left(\tfrac{1}{2}+iy\right)$',
    # r'$\tfrac{1}{\pi}\arg\zeta\left(\tfrac{1}{2}+\delta+iy\right)$'], loc=3)
    #pylab.gca().add_artist(l)
    #l.get_frame().set_linewidth(0.0)
    #l.get_frame().set_fill(False)
    pylab.savefig(output)

def plot_tricky(output):
    n = 655
    f = functools.partial(zeros.transeq, n)
    fe = functools.partial(zeros.transeqe, n, 1.0/100.0)
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    xaxis = pylab.arange(1007.2, 1008.7, 0.005)
    yaxis1 = [f(x) for x in xaxis]
    yaxis2 = [fe(x) for x in xaxis]
    p1 = ax.plot(xaxis, yaxis1)
    p2 = ax.plot(xaxis, yaxis2, '--', color='r')
    ax.set_xlim(1007.2, 1008.7)
    ax.set_ylim(-0.65, 1.6)
    ax.xaxis.set_ticks([1007.2866, 1007.905353, 1008.006704])
    ax.xaxis.set_ticklabels([r'$\tilde{y}_n$', r'$\cancel{y_n}$', r'$y_n$'])
    #ax.grid(True)
    l = pylab.legend([r'($13$)', r'($13$) with $\delta$'], loc=1)
    #[r'$\tfrac{1}{\pi}\arg\zeta\left(\tfrac{1}{2}+iy\right)$',
    # r'$\tfrac{1}{\pi}\arg\zeta\left(\tfrac{1}{2}+\delta+iy\right)$'], loc=3)
    #pylab.gca().add_artist(l)
    l.get_frame().set_linewidth(0.0)
    l.get_frame().set_fill(False)
    pylab.savefig(output)

def plot_prime(output, input_table, lambert=False, both=False):
    f = open(input_table)
    xvals = []; pitvals = []; pizvals = []; pilvals = []
    for l in f:
        x, pit, piz, pil = l.split('\t')
        xvals.append(float(x))
        pitvals.append(float(pit))
        pizvals.append(float(piz))
        pilvals.append(float(pil))
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    p1 = ax.plot(xvals, pitvals, color='b')
    pylab.fill_between(xvals, 0, pitvals, color='b', alpha=0.10)
    if both:
        p2 = ax.plot(xvals, pizvals, color='r')
        p3 = ax.plot(xvals, pilvals, color='m')
    elif lambert:
        p2 = ax.plot(xvals, pilvals, color='m')
    else:
        p2 = ax.plot(xvals, pizvals, color='r')
    maxx = int(xvals[-1])
    ax.set_xlim(2, int(maxx))
    #maxy = int(max(pilvals)) + 0.5
    maxy = 8.5
    ax.set_ylim(0, maxy)
    ax.xaxis.set_ticks(range(2, maxx+1, 2))
    ax.xaxis.set_ticklabels([r'$%i$' % i for i in range(2, maxx+1, 2)])
    ax.yaxis.set_ticks(pylab.arange(0, maxy, 1))
    ax.yaxis.set_ticklabels([r'$%i$' % i for i in pylab.arange(0, maxy, 1)])
    #ax.grid(True)
    ax.text(4,7.5, r'$100$ zeros')
    #l = pylab.legend([r'$5$ zeros'], borderaxespad=0, loc=2)
    #l.get_frame().set_linewidth(0.0)
    #l.get_frame().set_fill(False)

    #[r'$\tfrac{1}{\pi}\arg\zeta\left(\tfrac{1}{2}+iy\right)$',
    # r'$\tfrac{1}{\pi}\arg\zeta\left(\tfrac{1}{2}+\delta+iy\right)$'], loc=3)
    #pylab.gca().add_artist(l)
    #l.get_frame().set_linewidth(0.0)
    #l.get_frame().set_fill(False)
    pylab.savefig(output)

#plot_prime('zeta_prime_20.pdf', 'table20')
#plot_prime('zeta_prime_50.pdf', 'table50')
#plot_prime('zeta_prime_100.pdf', 'table100')

def plot_gamma_zeta(output):
    f = functools.partial(zeros.ratio_gamma, 14.1)
    g = functools.partial(zeros.ratio_zeta, 14.1)
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    xaxis = pylab.arange(0, 1, 0.0005)
    #yaxis1 = [mpmath.re(f(x)) for x in xaxis]
    #yaxis2 = [mpmath.re(g(x)) for x in xaxis]
    yaxis1 = [mpmath.im(f(x)) for x in xaxis]
    yaxis2 = [mpmath.im(g(x)) for x in xaxis]
    p1 = ax.plot(xaxis, yaxis1)
    p2 = ax.plot(xaxis, yaxis2, color='r')
    #ax.set_ylim(-1.2, 1.2)
    ax.xaxis.set_ticks([0, 0.5, 1])
    #ax.yaxis.set_ticks([0, 1])
    ax.yaxis.set_ticks([0])
    ax.grid(True)
    ax.set_axisbelow(True)
    ax.xaxis.set_ticklabels([r'$0$', r'$\tfrac{1}{2}$', r'$1$'])
    #l1 = ax.legend(p1,
    #    #[r'$\Re\left[\dfrac{\Gamma(\rho/2)}{\Gamma((1-\rho^*)/2)}\right]$'],
    #    [r'$\Im\left[ \mbox{LHS} (25) \right]$'],
    #    loc=(0.0, 0.84))
    #l2 = ax.legend(p2,
    #    #[r'$\Re\left[\dfrac{\zeta(1-\rho^*)}{\zeta(\rho)}\right]$'], 
    #    [r'$\Im\left[ \mbox{RHS} (25) \right]$'], 
    #    loc=(0.0, 0.71))
    #l1.get_frame().set_linewidth(0.0)
    #l1.get_frame().set_fill(False)
    #l2.get_frame().set_linewidth(0.0)
    #l2.get_frame().set_fill(False)
    #pylab.gca().add_artist(l1)
    #pylab.gca().add_artist(l2)
    l = ax.legend(
        [r'$\Im\left[ \mbox{LHS} (25) \right]$',
         r'$\Im\left[ \mbox{RHS} (25) \right]$'],
        loc=2)
    l.get_frame().set_linewidth(0.0)
    l.get_frame().set_fill(False)
    pylab.savefig(output)

def plot_ratio_chi(output):
    f = functools.partial(zeros.ratio_func_eq, 14.1)
    g = zeros.piexp
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    xaxis = pylab.arange(0, 1, 0.0005)
    yaxis1 = [mpmath.re(f(x)) for x in xaxis]
    yaxis2 = [mpmath.im(f(x)) for x in xaxis]
    yaxis3 = [g(x) for x in xaxis]
    p1 = ax.plot(xaxis, yaxis1)
    p2 = ax.plot(xaxis, yaxis2, color='r')
    p3 = ax.plot(xaxis, yaxis3, color='g')
    ax.xaxis.set_ticks([0, 0.5, 1])
    #ax.yaxis.set_ticks([0, 1])
    ax.yaxis.set_ticks([0, 1])
    ax.set_ylim(-1.2, 1.8)
    ax.grid(True)
    ax.set_axisbelow(True)
    ax.xaxis.set_ticklabels([r'$0$', r'$\tfrac{1}{2}$', r'$1$'])
    #l1 = pylab.legend(p1,
    #    r'$\Re\left[\dfrac{\Gamma(\rho/2)}{\Gamma((1-\rho^*)/2)}\right]$',
    #    loc=(0, 0.7))
    #l2 = pylab.legend(p2,
    #    r'$\Re\left[\dfrac{\zeta(1-\rho^*)}{\zeta(\rho)}\right]$', 
    #    loc=(0.8, 0.2))
    #l1.get_frame().set_linewidth(0.0)
    #l1.get_frame().set_fill(False)
    #l2.get_frame().set_linewidth(0.0)
    #l2.get_frame().set_fill(False)
    pylab.savefig(output)


###############################################################################
# Below we have some plots used in the Germany Lectures
###############################################################################

import prime

def plot_prime_li(output, n):
    """Comparison of PrimePi function and Li."""
    x = pylab.arange(0, n, 0.05)
    y = [prime.pi_true(i) for i in x]
    z = [mpmath.li(i) for i in x]
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    p1 = ax.plot(x, y, color='b')
    p2 = ax.plot(x, z, color='r')
    pylab.fill_between(x, 0, y, color='b', alpha=0.10)
    ax.set_ylim(0, 200)
    l = ax.legend([r'$\pi(x)$', r'$\rm{Li}(x)$'], loc=2)
    l.get_frame().set_linewidth(0.0)
    l.get_frame().set_fill(False)
    pylab.savefig(output)

def plot_j(output, x):
    """Comparison of PrimePi function and Li."""
    xvals = pylab.arange(0, x, 0.005)
    yvals = [prime.j_mangoldt(i) for i in xvals]
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    p1 = ax.plot(xvals, yvals, color='b')
    pylab.fill_between(xvals, 0, yvals, color='b', alpha=0.10)
    ax.set_xlim(0, 11)
    l = ax.legend([r'$J(x)$'], loc=2)
    l.get_frame().set_linewidth(0.0)
    l.get_frame().set_fill(False)
    pylab.savefig(output)

def plot_ratio_zeta(output, y):
    """Comparison of PrimePi function and Li."""
    from mpmath import zeta
    from mpmath import mpc 
    xvals = pylab.arange(0.01, y, 0.05)
    yvals = [zeta(mpc(.5,i)).real / zeta(mpc(.5, i)).imag for i in xvals]
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim(-10, 10)
    p1 = ax.plot(xvals, yvals, color='b')
    #p2 = ax.plot(xvals, [0]*len(xvals), '--', linewidth=.5, color='k')
    ax.set_ylabel(r'$\Re\left(\zeta(\tfrac{1}{2}+iy)\right) / '\
                  r'\Im\left( \zeta(\tfrac{1}{2}+iy) \right)$')
    ax.set_xlabel(r'$y$')
    ax.xaxis.set_ticks_position('bottom')
    pylab.tight_layout()
    pylab.savefig(output)

def plot_arg_zeta(output):
    f = open('~/output.txt')

    f = zeros.argzetae
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    xaxis = pylab.arange(1437, 1442, 0.02)
    yaxis1 = [f(0.000001, x) for x in xaxis]
    #yaxis2 = [f(0.01, x) for x in xaxis]
    #pylab.fill_between(xaxis, 0, yaxis1, color='b', alpha=.10)
    p1 = ax.plot(xaxis, yaxis1)
    p2 = ax.plot(xaxis, [0]*len(xaxis), '--', color='k', linewidth=.5)
    #p2 = ax.plot(xaxis, [0]*len(xaxis), '--', linewidth=.5, color='k')
    #p3 = ax.plot(xaxis, yaxis2, '--', color='r')
    #ax.set_xlim(277, 290)
    #ax.set_ylim(-1, 1)
    #ax.xaxis.set_ticks([0, 0.5, 1.0])
    #ax.xaxis.set_ticklabels([r'$0$', r'$\tfrac{1}{2}$', r'$1$'])
    l = pylab.legend(
        [r'$\tfrac{1}{\pi}{\rm arg}\,\zeta\left(\tfrac{1}{2}+iy\right)$'], 
        loc=1)
    #ax.set_xlim(277,290)
    pylab.gca().add_artist(l)
    l.get_frame().set_linewidth(0.0)
    l.get_frame().set_fill(False)
    pylab.savefig(output)

def plot_dots_gue(output):
    zeros = [float(l) for l in open('zeros.dat')]
    randoms = [float(l) for l in open('randoms.dat')]
    eigs = [float(l) for l in open('eigs.dat')]
    fig = pylab.figure()
    fig.set_size_inches(6.5, 1.5)
    ax = fig.add_subplot(111)
    ax.plot(randoms, [.45]*len(randoms), 'rv', ms=4, label='Random numbers')
    ax.plot(zeros, [.5]*len(zeros), 'bo', ms=4, label='Riemann zeros')
    ax.plot(eigs, [.55]*len(eigs), 'ys', ms=3.5, label='Eigenvalues')
    ax.set_ylim(0.40, 0.68)
    ax.set_xlim(-5, 145)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    #ax.xaxis.set_ticks_position('bottom')
    #ax.yaxis.set_ticks_position('none')
    ax.tick_params(axis='y', which='both', left='off', right='off', 
                    labelleft='off', labelright='off')   
    ax.tick_params(axis='x', which='both', top='off',  
                    labeltop='off')   
    #l = pylab.legend(
    #    [r'Random numbers', r'Riemann zeros', r'Eigenvalues'])
    l = pylab.legend(bbox_to_anchor=(0., 0.7, 1., 0.102), loc=3,
               ncol=3, mode="expand", borderaxespad=0.)
    pylab.gca().add_artist(l)
    l.get_frame().set_linewidth(0.4)
    l.get_frame().set_fill(False)
    pylab.tight_layout()
    pylab.savefig(output)

#plot_dots_gue('/home/gui/Dropbox/RiemannLectures/Lect3/figs/dots_gue.pdf')



