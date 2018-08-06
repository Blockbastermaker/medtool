# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

class Correlations(object) :

    def __init__(self, df):

        self.df = df

        self.corr_method = 'pearson' # other options: spearman

    def pairwiseCorrelations(self, dat=None):

        if dat :
            return dat.corr(method=self.corr_method)
        else :
            return self.df.corr(method=self.corr_method)

    def drawCorrelationMap(self, corrs_matrix, cmap='seismic',
                           xlab="X", ylab="Y", title="Title",
                           figname="",
                           ):

        plt.pcolor(corrs_matrix, cmap=cm.get_cmap(cmap))

        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)

        plt.colorbar()

        if figname :
            plt.savefig(figname, dpi=2000)

        plt.show()

