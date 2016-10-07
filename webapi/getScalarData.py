import numpy as np
import json
import datetime as dt
import pandas as pd
import urllib

class getScalarData():

    def __init__(self, method = 'getByStation', dateFrom = dt.datetime.today()-dt.timedelta(1), 
                 dateTo = dt.datetime.today(), token = '', stationCode = 'TWDP', 
                 deviceCategory = 'TSG', sensors = '', metadata = 'full', rowLimit = []):
        '''
        
        Constructor

        '''

        self.method = method

        if isinstance(dateFrom, dt.datetime):
            self.dateFrom = dateFrom.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        else:
            self.dateFrom = dateFrom
            
        if isinstance(dateTo, dt.datetime):
            self.dateTo = dateTo.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        else:
            self.dateTo = dateTo

        self.token = token
        self.stationCode = stationCode
        self.deviceCategory = deviceCategory
        self.sensors = sensors
        self.metadata = metadata
        self.rowLimit = rowLimit

        print 'Retrieving data from web service...'

        self.__ScalarDataAPIService()
        self.__JSON_parse()

    def __ScalarDataAPIService(self):
        '''
        Docstring
        '''

        endpoint = 'http://dmas.uvic.ca/api/scalardata?'
        params = {'method' : self.method,
                  'token' : self.token,
                  'stationCode' : self.stationCode,
                  'deviceCategory' : self.deviceCategory,
                  'dateTo' : self.dateTo,
                  'dateFrom' : self.dateFrom,
                  'sensors' : self.sensors,
                  'metadata' : self.metadata,
                  'rowLimit' : self.rowLimit}
        link = urllib.urlencode(params)

        try:
            response = urllib.urlopen(endpoint+link)
        except:
            # INCLUDE ERROR HANDLING FOR URL REQUESTS HERE
            pass

        self.json_string = response.read()

    def __JSON_parse(self):
        '''
        Docstring
        '''

        s = self.json_string
        s_parsed = json.JSONDecoder().decode(s)
        sensorData = dict()
        
        try:
            for sensor in s_parsed['sensorData']:
                sensorData[sensor['sensor']] = pd.DataFrame.from_dict(sensor['data'])
            
            self.sensorData = sensorData
        except KeyError, e:
            for error in s_parsed['errors']:
                print error
