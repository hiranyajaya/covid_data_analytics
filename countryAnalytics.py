# -*- coding: utf-8 -*-
"""
covid data analytics code
Author: Hiranya Jayakody. March 2020

This code requires csse_covid_19_dataset found at: https://github.com/CSSEGISandData/COVID-19
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime 


""" modify following three lines to point to COVID-19 dataset """
covid_confirmed_csv = 'csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
covid_death_csv = 'csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
covid_recovered_csv = 'csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'


""" create a class for analytics """
class CountryAnalytics:
    """class to extract data as needed from covid-19 dataset"""
    
    def __init__(self, country_name):
        
        self._country = country_name
        
        covid_confirmed = pd.read_csv(covid_confirmed_csv)
        covid_deaths = pd.read_csv(covid_death_csv)
        covid_recovered = pd.read_csv(covid_recovered_csv)
        
        confirmed = covid_confirmed[covid_confirmed["Country/Region"]==self._country]
        self._confirmed_count = self._convert_to_df(confirmed.sum(axis = 0, skipna = True))
        
        deaths = covid_deaths[covid_deaths["Country/Region"]==self._country]
        self._death_count = self._convert_to_df(deaths.sum(axis = 0, skipna = True))
        
        recovered = covid_recovered[covid_recovered["Country/Region"]==self._country]
        self._recovered_count = self._convert_to_df(recovered.sum(axis = 0, skipna = True))
        
    def _convert_to_df(self,dataset):
        """ Converts series to dataframe """
        dataset = dataset.to_frame()
        dataset = dataset[4:] #first 4 elements removed (state/country/)
        return dataset[0]
        
    def get_country_name(self):
        """ get country name """
        return self._country
        
        
    def get_confirmed_timeseries(self):
        """ returns confirmed COVID-19 time series data for a given country """
        return self._confirmed_count
            
    def get_death_timeseries(self):
        """ returns COVID-19 deaths time series data for a given country """
        return self._death_count
    
    def get_recovered_timeseries(self):
        """ returns COVID-19 recoveries time series data for a given country """
        return self._recovered_count
        
   
    def get_current_data(self):
        """ returns total number of confirmed cases, deaths and recoveries as of today """
        return [self._confirmed_count[-1],self._death_count[-1],self._recovered_count[-1]]
    
    def get_growth_rate_timeseries(self):
        """ returns the average growth rate for a given country """
        data = self._confirmed_count
        val = []
        
        for i in range(1,len(data)):
            if (data[i-1]>0):
                val.append(data[i]/data[i-1])
            else:
                val.append(1)

        return val
    
    def get_growth_factor_timeseries(self):
        """ returns the average growth rate for a given country """
        data = self._confirmed_count
        val = []
        
        for i in range(2,len(data)):
            if ((data[i-1]-data[i-2])>0 and (data[i]-data[i-1]) > 0):
                val.append((data[i]-data[i-1])/(data[i-1]-data[i-2]))
            else:
                val.append(1)

        return val
    
    def get_avg_growth_rate(self):
        return np.mean(self.get_growth_rate_timeseries())
        
    
    def predict(self,rate,days):
        """ predict the expected number of cases in x days. x is the input """
        return self.get_current_data()[0]*np.power(rate,days)
        
   
    
    
if __name__ == '__main__':
    
    country_list = ['US', 'Italy','China','Sri Lanka'] #list the countries 
    countries = [] #holds object list
    data = [] #holds timeseries data for each object
    growth_factor = [] #holds timeseries for growth rate
    
    # create objects for each country
    for idx,val in enumerate(country_list):
        countries.append(CountryAnalytics(val))
     
    # retrieved data for each country
    for idx,val in enumerate(countries):
        data.append(val.get_confirmed_timeseries())
        growth_factor.append(val.get_growth_factor_timeseries())
        

        
        
    #example 1: get virus growth rate for xth country in the list.
    rate = countries[2].get_avg_growth_rate()
    
    #example 2: Predict the expected number of cases in x days for the yth country.
    prediction = countries[2].predict(rate,23)
      
    """plot data"""
    
    #example 3: plot data for a single country
    """ for a single country """
    # c_id = 0
    # dates = range(0,len(data[c_id]))
    # country_lbl, = plt.plot(dates, data[c_id], label= str(countries[c_id].get_country_name()),color='orange')
    # plt.xlabel('days since 22 Jan 2020',size=16)
    # plt.ylabel('confirmed cases',size=16)
    # plt.title('Confirmed cases for {} as of {}'.format(countries[c_id].get_country_name(),datetime.datetime.today()-datetime.timedelta(days=1)))
    # plt.grid(color='black', linestyle='--', linewidth=0.5)
    # plt.legend(handles=[country_lbl],prop={'size': 12})
    # plt.show()
    
    #example 4: plot data for multiple countries
    """for multiple countries """
    # dates = range(0,len(data[0]))
    # c0, = plt.plot(dates, data[0], label= str(countries[0].get_country_name()), color='b')
    # c1, = plt.plot(dates, data[1], label= str(countries[1].get_country_name()), color='r')
    # c2, = plt.plot(dates, data[2], label= str(countries[2].get_country_name()), color='g')
    # #c3, = plt.plot(dates, data[3], label= str(countries[3].get_country_name()), color='orange')
    # plt.xlabel('days since 22 Jan 2020',size=16)
    # plt.ylabel('confirmed cases',size=16)
    # plt.title('Confirmed COVID-19 cases as of {}'.format(datetime.date.today()),size=16)
    # plt.grid(color='black', linestyle='--', linewidth=0.5)
    # plt.legend(handles=[c0,c1,c2],prop={'size': 12})
    # plt.show()
    
    #example 5: get day by day growth rates for a given country
    
    #Feel free to try out different operations by calling other methods 
    c_id = 3
    dates = range(0,len(growth_factor[c_id]))
    country_lbl, = plt.plot(dates, growth_factor[c_id], label= str(countries[c_id].get_country_name()),color='b')
    plt.xlabel('days since 22 Jan 2020',size=16)
    plt.ylabel('growth rate',size=16)
    plt.title('COVID-19 growth factor for {} as of {}'.format(countries[c_id].get_country_name(),datetime.datetime.today()-datetime.timedelta(days=1)))
    plt.grid(color='black', linestyle='--', linewidth=0.5)
    plt.legend(handles=[country_lbl],prop={'size': 12})
    plt.show()
