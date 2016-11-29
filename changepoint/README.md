[View the tutorial here](http://nbviewer.jupyter.org/github/adam-paul/ONC/blob/master/changepoint/cpaTutorial.html)

The change point analysis tool is used as follows:

`cpa_instance = cpa.changepoint(data=dataArray, filter_on=True, trend_on=False, f=240)`

The arguments a cpa instance takes are:
* data: A numpy array containing data to be analyzed
* filter_on: A boolean representing whether or not post-analysis bandpass filtering should be done
* trend_on: A boolean representing whether or not post-analysis trend filtering should be done
* f: A "frequency" representing the cutof for bandpass filtering; units need to be whatever timescale the data is presented in (e.g. 240 minutes for minute-averaged data, in this case)
* C: A scale constant which has defaults hardcoded in but can be user defined (tunes the sensitivity of change point analysis)
