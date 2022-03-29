
# coding: utf-8

# ###   IoT Data Preprocess
# 
# 
# 기기고유번호;위도;경도;시간;기압;기압QC;온도;온도QC;습도;습도QC;강수;강수QC;PM10;PM10 QC;PM25;PM25 보정;PM25 QC;
# 
# 2019091800000159;37.360305;126.708330;000826;1010.4;Y;26.9;Y;69.4;Y;330.0;Y;3.1;Y;3.1;3.1;Y;
# 
# 2019091800000160;37.314565;126.708051;000802;1011.3;Y;26.2;Y;74.3;Y;303.0;Y;3.2;Y;3.1;3.1;Y;

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix


import seaborn as sns
# import missingno as msno
import datetime as dt
import os

from scipy.stats import pearsonr
import sklearn.metrics as metrics


# In[5]:



df=pd.read_csv("fd_sensor_qc_data_temp_202107201413.csv", encoding='cp949')

# station info  - lat/lon 

df_stn = df.filter(['k1', 'k2', 'k3', 'k18']) 
df_stn.columns = ['id', 'lat', 'lon', 'date']
df_stn['sensor_id']=df_stn.id.astype('str').str.split('0000').str[1]

# Sorting by date

df_stn = df_stn.sort_values(by=["date"], ascending=[True]) 

# drop duplicates 

stn = df_stn.drop_duplicates(['sensor_id', 'lat', 'lon'], keep = 'first')
stn = stn.sort_values(by=["sensor_id", "date"], ascending=[True, True]) 
stn.to_csv('station_info.csv')

df["time"] = df['k4'].astype('str').str.zfill(6)

df['date']=df.k18.astype('str')+" "+df.time

df1 = df.filter(['date', 'k1', 'k7', 'k9', 'k16', 'k5', 'k11'])
df1.columns = ['date','sensor_id','T', 'RH','PM25', 'MSLP', 'RAIN' ]
df1['date'] = pd.to_datetime(df1['date'], format="%Y%m%d %H%M%S")

df2=df1.set_index('date')

## remove error data

#  T  -30~ 40 ,  # Ps  900~ 1050 , # RH   5~100 

df3 = df2[(df2['T'] <= 40) & (df2['T'] >= -30) & (df2['RH'] >5) & (df2['RH'] <= 100) & (df2['MSLP'] > 900) & (df2['MSLP'] < 1050)
         & (df2['PM25'] > 3)  & (df2['RAIN'] > 5)]

#df3.head()

plt.figure(figsize=(15,5))
plt.plot(df3['T'])
#plt.ylim(-40,40)

plt.figure(figsize=(15,5))
plt.plot(df3['RH'])

plt.figure(figsize=(15,5))
plt.plot(df3['MSLP'])

plt.figure(figsize=(15,5))
plt.plot(df3['PM25'])

plt.figure(figsize=(15,5))
plt.plot(df3['RAIN'])

# make new id

df3['new_id']=df3.sensor_id.astype('str').str.split('0000').str[1]

df4 = df3.sort_values(by=["sensor_id", "date"], ascending=[True, True]) 
df4.to_csv("IoT_Data_min_qc.csv")
#df4.head()

#  Average

dfh = df3.groupby('new_id').resample('H').mean()

dfh = dfh.round(decimals=1) 
dfh.to_csv("IoT_Data_hour_case1.csv")
#dfh.head()

