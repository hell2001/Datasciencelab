from spyre import server
import urllib
import urllib.request
import datetime
import pandas as pd
import glob
from matplotlib import pyplot as plt

def download_vhi(i):
    for i in range(0, 27):
        # URL-адрес областей Украины (ID={})
        url = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2020&type=Mean'.format(
            i)
        vhi_url = urllib.request.urlopen(url)
        text = vhi_url.read()
        dt = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        #створюємо файл для запису
        out = open('csv-raw/vhi_id_{}_{}.csv'.format(i, dt), 'wb')
        out.write(text)
        out.close()
        print("Данные загружены в папку csv-raw, объект c ID: " + str(i) + " с текущей датой и временем:  " + dt)

class SimpleApp(server.App):
    title = "Data AnalysisLab 2"
    tabs = ["Plot","Table"]
    controls = [ {"type" : "button", "id" : "update_data", "label": "Calculate!"}]
    
    inputs = [
                {   "input_type":'dropdown',
                    "label": 'column', 
                    "options" : [ {"label": "VCI", "value":"VCI"},
                                  {"label": "TCI", "value":"TCI"},
                                  {"label": "VHI", "value":"VHI"}],
                    "key": 'column', 
                    "action_id": "update_data" },
                {    "input_type":'text',
                    "label": 'Year', 
                    "value":2021,
                    "key": "year_r",
                    "action_id": "update_data" },
                {   "input_type":'text',
                    "label": 'Week since', 
                    "value":1,
                    "key": "since", 
                    "action_id": "update_data" },
                  {     "input_type":'text',
                    "label": 'Week till', 
                    "value":52,
                    "key": "till",
                    "action_id": "update_data" },
                {
                    "input_type":'dropdown',
                    "label": 'Region', 
                    "key": "reg", 
                    "options" : [ {"label":"Cherkasy Oblast", "value":"1"},
                                  {"label":"Chernihiv Oblast", "value":"2"},
                                  {"label":"Chernivtsi Oblast", "value":"3"},
                                  {"label":"Crimea", "value":"4"},
                                  {"label":"Dnipropetrovsk Oblast", "value":"5"},
                                  {"label":"Donetsk Oblast", "value":"6"},
                                  {"label":"Ivano-Frankivsk Oblast", "value":"7"},
                                  {"label":"Kharkiv Oblast", "value":"8"},
                                  {"label":"Kherson Oblast", "value":"9"},
                                  {"label":"Khmelnytskyi Oblast", "value":"10"},
                                  {"label":"Kiev Oblast", "value":"11"},
                                  {"label":"Kiev City", "value":"12"},
                                  {"label":"Kirovohrad Oblast", "value":"13"},
                                  {"label":"Luhansk Oblast", "value":"14"},
                                  {"label":"Lviv Oblast", "value":"15"},
                                  {"label":"Mykolaiv Oblast", "value":"16"},
                                  {"label":"Odessa Oblast", "value":"17"},
                                  {"label":"Poltava Oblast", "value":"18"},
                                  {"label":"Rivne Oblast", "value":"19"},
                                  {"label":"Sevastopol`", "value":"20"},
                                  {"label":"Sumy Oblast", "value":"21"},
                                  {"label":"Ternopil Oblast", "value":"22"},
                                  {"label":"Transkarpathia Oblast", "value":"23"},
                                  {"label":"Vinnytsia Oblast", "value":"24"},
                                  {"label":"Volyn Oblast", "value":"25"},
                                  {"label":"Zaporizhia Oblast", "value":"26"},
                                  {"label":"Zhytomyr Oblast", "value":"27"}
                                ],
                    "action_id": "update_data"
    }]
    outputs = [{    
                    "output_type" : "plot",
                    "output_id" : "plot",
                    "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                {    "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True 
                }
            ]
   
    def getData(self,params):
        #download_vhi(params['reg'])
        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']
        new = [24, 25, 5, 6, 27, 23, 26, 7, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 8, 29, 10, 1, 3, 2, 4, 12, 20 ]
       #отримуємо файли по патерну 
        files = glob.glob('csv-raw/*.csv')
        dfs = []
        i = 0
        for f in files:
            df = pd.read_csv(f, index_col=False, skiprows=1, skipfooter=1, engine="python", names=headers)
            df = df.loc[(df['Year'] == int(params['year_r']))]
            df = df.loc[(df['Week'] >= int(params['since']))]
            df = df.loc[(df['Week'] <= int(params['till']))]
            df = df.drop(df.loc[df['VHI'] == -1].index)
            df['area'] = new[i]
            df = df.loc[(df['area'] == int(params['reg']))]
            i += 1
            dfs.append(df)
        return pd.concat(dfs) #повертаємо дані
    
    def getPlot(self,params):
        #df = pd.read_csv('csv-raw/vhi_id_0_2021-04-04_18-12.csv', index_col=False, header=1)
        frame = self.getData(params)
        y_axis = frame[params['column']]
        x_axis = frame['Week']
        plt.plot(x_axis, y_axis)
        plt.xlabel('week')
        plt.ylabel('column')
        print(plt)
        return plt.gcf()
# download_vhi()
#записуємо у фрейм
#frame = getData()


app = SimpleApp()
app.launch()
a = {"since": 2014, "till": 2021}
frame = app.getData(a)