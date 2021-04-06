import urllib
import urllib.request
import datetime
import pandas as pd
import glob


def download_vhi():
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
    
def get_frame():
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']
    new = [22, 24, 23, 25, 3, 4, 8, 19, 20, 21, 9, 9.1, 10, 11, 12, 13, 14, 5, 15, 16, 26, 17, 18, 6, 1, 2, 7]
   #отримуємо файли по патерну 
    files = glob.glob('csv-raw/*.csv')
    dfs = []
    i = 0
    for f in files:
        df = pd.read_csv(f, index_col=False, skiprows=1, skipfooter=1, engine="python", names=headers)
        df = df.drop(df.loc[df['VHI'] == -1].index)
        df['area'] = new[i]
        i += 1
        dfs.append(df)
    return pd.concat(dfs) #повертаємо дані


# download_vhi()
#записуємо у фрейм
frame = get_frame()


def max_min(year, index):
    df = frame[(frame['Year'] == year) & (frame['area'] == index)]['VHI']
    print('min', df.min(), 'max', df.max(), 'For year', year, 'Index', index)


def get_extreme_drought(index):
    df_drought = frame[(frame['area'] == index) & (frame['VHI'] <= 15)]['Year'].unique()
    print(df_drought)

def get_middle_drought(index):
    df_drought = frame[(frame['area'] == index) & (frame['VHI'] > 15) & (frame['VHI'] <= 30)]['Year'].unique()
    print(df_drought)

max_min(2000, 7)
get_extreme_drought(7)
get_middle_drought(7)

