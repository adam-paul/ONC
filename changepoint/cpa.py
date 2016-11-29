# This is the change point analysis python module
# It contains the changepoint class, which can be called from a module instance
# See README and documentation on GitHub for more information

import numpy as np
import matplotlib.pyplot as plt
import pyper
from mk_test import mk_test

class changepoint():

    ##############################################
    #                Constructor                 #
    ##############################################

    def __init__(self, data=np.array([]), f=300., C='', filter_on=True, trend_on=False):
        '''
        This is the constructor for the changepoint class

        Parameters
        ----------
        data : numpy.ndarray 
            A numpy array containing the data (i.e. time series) upon which change point analysis is performed
        f : int, optional
            Cutoff frequency (in minutes) for change point filtering
        C : int, optional
            Scaling constant for WBS analysis, defaults set by algorithm, can be manually declared
        filter_on : Boolean, optional
            Turns bandpass filtering on (True) or off (False)
        trend_on : Boolean, optional
            Turns trend analysis on (True) or off (False)

        '''

        # Declare instances of global variables
        self.data = data
        self.scale = len(data)
        self.trend_on = trend_on
        self.C = C
        self.f = f
        self.filter_on = filter_on

        # Run the analysis
        self.__pipeData()
        self.__cpa()
        
        # Perform trend analysis between change points and rule out similarities
        if trend_on == True: 
            self.trend()
        
        # Perform low-pass filtering of change point candidates if more than one change point detected
        if (len(self.cpts)>1 and filter_on==True):
            self.__lowPass()

    ###########################################
    #                Analysis                 #
    ###########################################

    def __pipeData(self):
        '''
        This function pipes data to R environment and declares R variables

        NOTE: R must be installed in this script's environment

        '''

        try:
            self.r = pyper.R(use_numpy = True) # For data input as numpy array
            self.r("chooseCRANmirror(ind=10)") # Choose Canadian host as R mirror (for package downloads)
            self.r.assign('data', self.data)
        except:
            print 'There was an error piping data to R environment. Please ensure that R is properly installed and all PATH variables are correct.'

    def __cpa(self):
        '''
        This function performs the change point analysis on the data in the R environment

        NOTE: R package 'wbs' must be installed for this analysis to succeed

        '''

        self.r('library("wbs")')
        self.r('wbsdata <- wbs(data)')
        
        # The scaling constant for the WBS change point threshold is defined based on the data set size
        # If a scaling constant has been manually defined it will be used instead
        if self.C:
            C = self.C
        else:
            if self.scale < 10000:
                self.C = 97.
            elif 10000 < self.scale < 50000:
                self.C = 308.
            else: 
                self.C = 1038.
        
        # The analysis is performed and the result is converted to a python dictionary
        self.r('wbsdata.cpt <- changepoints(wbsdata, th.const={0})'.format(self.C))
        wbsdata = self.r.get('wbsdata.cpt')
        
        # Retrieve change points from dictionary
        # If only one change point is present, convert it to a 1-length array
        # If no change points are detected, print a warning
        if isinstance(wbsdata['cpt.th'][0], np.ndarray):
            cpts = wbsdata['cpt.th'][0]
        elif isinstance(wbsdata['cpt.th'][0], int):
            cpts = np.asarray([wbsdata['cpt.th'][0]])
        else:
            cpts = np.asarray([])
            print 'WARNING: No change points detected'

        self.cpts = sorted(cpts)

    ##############################################
    #             Post-analysis tools            #
    ##############################################

    def __trend(self):
        '''
        NOTE: THIS FUNCTION IS EXPERIMENTAL AND IS TURNED OFF BY DEFAULT

        Perform trend analysis between change points and remove those which have similar trends
        
        '''
        
        splitdata = np.split(data, cpts)
        
        trend = []
        for sec in splitdata:
            trend = mk_test(sec)
            trends.append(trend)

        slopes = [el[3] for el in trends]
        absdiff = np.abs(np.diff(slopes))
        
        bad_cpts = []
        for ind, diff in enumerate(absdiff):
            if diff < np.abs(slopes[ind]/2):
                bad_cpts.append(cpts[ind])

        new_cpts = np.delete(cpts, bad_cpts)

        self.cpts = sorted(new_cpts)

    def __lowPass(self):
        '''
        Filter the results of the WBS analysis to remove change points that occur
            above a user-specified frequency
        '''
        
        timediff = np.diff(self.cpts)
        
        bad_cpts = []
        for ind, diff in enumerate(timediff):
            if diff < self.f:
                bad_cpts.append(ind)
                                    
        new_cpts = np.delete(self.cpts, bad_cpts)
        self.cpts = sorted(new_cpts)

    ###########################################
    #             Plotting tools              #
    ###########################################

    def plotPreview(self):
        '''
        This function can be used to quickly preview the change point results

        '''
        
        wbsfig = plt.figure(figsize=(12, 10))

        ax1 = wbsfig.add_subplot(2, 1, 1)
        ax1.plot(self.data)
        ax1.set_title('Raw data before change point analysis')

        ax2 = wbsfig.add_subplot(2, 1, 2)
        ax2.plot(self.data)
        ax2.set_title('Raw data with change point analysis applied')

        for i in self.cpts:
            ax2.axvline(i, color='r', linestyle='--')

