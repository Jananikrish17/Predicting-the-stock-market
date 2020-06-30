import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

stock_df = pd.read_csv("sphist.csv")


stock_df.info()
stock_df['Date'] = pd.to_datetime(stock_df['Date'])

stock_df.sort_values(by='Date',ascending=True,inplace=True)
stock_df.reset_index(drop=True, inplace=True)
print(stock_df.head())
### Generating Indicators
stock_df['Av_days_5'] = stock_df["Close"].rolling(5).mean().shift(1)
stock_df['Av_days_30'] = stock_df['Close'].rolling(30).mean().shift(1)
stock_df['Av_days_365'] = stock_df['Close'].rolling(365).mean().shift(1)
##finding Standard deviation
stock_df["std_5"] = stock_df["Close"].rolling(5).std().shift(1)
stock_df["std365"] = stock_df["Close"].rolling(5).std().shift(1)


## Average ratio
stock_df["avg_ratio_5_365"] = stock_df['Av_days_5'] / stock_df['Av_days_365']
stock_df["ratio_std5_std365"]= stock_df["std_5"] / stock_df["std365"] 

#drop NAN values

stock_df.dropna(axis=0, inplace=True)
stock_df.isnull().sum()

##Create train and test dataframes
train_df = stock_df[stock_df['Date'] < datetime(year=2013, month=1,day=1)]
test_df = stock_df[stock_df['Date']>= datetime(year=2013, month=1,day=1)]

lr=LinearRegression()
features = ['Av_days_5','Av_days_30','Av_days_365','std_5','std365','avg_ratio_5_365']
target= 'Close'
lr.fit(train_df[features], train_df[target])
predictions= lr.predict(test_df[features])
## Calculate error metrics
mse= mean_squared_error(predictions, test_df[target])
mae = mean_absolute_error(test_df[target], predictions)
print("MAE: ", mae)
print("MSE: ", mse)

### Improving errors¶
stock_df["ave_volume_5d"] =  stock_df['Av_days_5'].rolling(5).mean().shift(1)
stock_df["ave_5yrs"]= stock_df['Close'].rolling(5).mean().shift(1)
stock_df["ave_volume_5yr"] = stock_df["ave_5yrs"].rolling(5).mean().shift(1)

#Standard deviation

stock_df['std_5days_vol'] = stock_df["ave_volume_5d"].rolling(5).std().shift(1)
stock_df['std_5years_vol'] = stock_df["ave_volume_5yr"].rolling(5).std().shift(1)


## Average ratio

stock_df['ratio_ave_vol'] = stock_df['ave_volume_5d'] / stock_df['ave_volume_5yr']


stock_df['ratio_std_vol'] = stock_df['std_5days_vol'] / stock_df['std_5years_vol']

stock_df.dropna(axis=0, inplace=True)

## Create train and test dataframes
train = stock_df[stock_df['Date'] < datetime(year=2013, month=1, day=1)]
test = stock_df[stock_df['Date']>= datetime(year=2013, month=1,day=1)]


lr = LinearRegression()
features = ['Av_days_5','Av_days_30','Av_days_365','std_5','std365','avg_ratio_5_365','ave_volume_5d','ave_volume_5yr','std_5days_vol','std_5years_vol','ratio_ave_vol']
target =['Close']
lr.fit(train[features], train[target])
predict = lr.predict(test[features])

## calculating mse

mse = mean_squared_error(test[target],predict)
mae = mean_absolute_error(test_df[target], predictions)
print("MAE: " , mae)
print("MSE: ", mse)




