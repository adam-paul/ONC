import numpy as np
import json
import datetime as dt
import pandas as pd
import urllib

class getScalarData():

    def __init__(self, method = 'getByStation', dateFrom = dt.datetime.today()-dt.timedelta(1), 
                 dateTo = dt.datetime.today(), token = '', stationCode = '', deviceCategory = '', 
                 sensors = '', metadata = 'full', rowLimit = []):
        '''
        
        Constructor

        '''

        self.method = method
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.token = token
        self.stationCode = stationCode
        self.deviceCategory = deviceCategory
        self.sensors = sensors
        self.metadata = metadata
        self.rowLimit = rowLimit

        print 'Retrieving data from web service...'

    def ScalarDataAPIService(self):
        '''
        Docstring
        '''

        endpoint = 'http://dmas.uvic.ca/api/scalardata'    
        params = {'method' : self.method,
                  'token' : self.token,
                  'station' : self.stationCode,
                  'deviceCategory' : self.deviceCategory,
                  'dateTo' : self.dateTo,
                  'dateFrom' : self.dateFrom,
                  'sensors' : self.sensors,
                  'metadata' : self.metadata,
                  'rowLimit' : self.rowLimit}
        link = urllib.urlencode(params)
        req = urllib.request(endpoint, link)
        response = urllib.urlopen(req)
        
        self.json_string = response.read()
            
    def json_parse(self):
        '''
        Docstring
        '''

        s = self.json_string
        s_parsed = json.JSONDecoder().decode(s)
        sensorData = dict()
        
        for sensor in s_parsed['sensorData']:
            sensorData[sensor['sensor']] = pd.DataFrame.from_dict(sensor['data'])
        
        self.sensorData = sensorData
