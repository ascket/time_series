# %%
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

timestamp = pd.Timestamp(datetime(2023, 4, 24))

# %%
timestamp2 = pd.Timestamp("2023-04-24")
print(timestamp2)
print(timestamp2.year)
print(timestamp2.month_name())

# %%
period = pd.Period("2023-04")  # по умолчанию месяц
period2 = period.asfreq('D')
# 'D' - по дням
# 'M' - по месяцам
# 'B' - по рабочим дням (business days)

# %%
period_from_timestamp = timestamp.to_period("D")
timestamp_from_period = period.to_timestamp()

# %%
print(period + 2)

# %%
index = pd.date_range(start="2023-4-24", periods=12, freq='M')
print(index[0])
print(index.to_period())

# %%
df_time = pd.DataFrame({"data": index})
print(df_time.info())

# %%
import numpy as np

data_time = np.random.random(size=(12, 2))
df_time = pd.DataFrame(data=data_time, index=index)

# %%
google = pd.read_csv(
    r"G:\Alexey\Documents\Raznoe\Studium\Geek Brains\Python\PYTHON-MAIN\5. Data Science\14.DATACAMP\Time_Series\01_Manipulating_Time_Series_Data_in_Python\stock_data\google.csv")
google = google.dropna()
goolge.columns = ["date", "price"]
google["date"] = pd.to_datetime(google["date"])
google.set_index("date", inplace=True)

# %%
plt.plot(google["price"])
plt.title("Google")
plt.grid()
plt.show()

# %%
print(google.loc["2015":"2016"])

# %%
google_with_nan = google.asfreq(freq="D")  # выводит дни по порядку, т.е. на отсутствующие дни кладёт NaN
print(google_with_nan[google_with_nan["price"].isnull()])  # найдём дни, для которых нет инфы о цене

# %%
data_nyc = pd.read_csv(
    r"G:\Alexey\Documents\Raznoe\Studium\Geek Brains\Python\PYTHON-MAIN\5. Data Science\14.DATACAMP\Time_Series\01_Manipulating_Time_Series_Data_in_Python\air_quality_data\nyc.csv")

# %%
data_nyc["date"] = pd.to_datetime(data_nyc["date"])
data_nyc.set_index("date", inplace=True)

# %%
# import matplotlib.pyplot as plt
data_nyc.plot(subplots=True)
plt.tight_layout()
plt.show()

# %%
plt.plot(data_nyc.ozone)
plt.show()

# %%
yahoo = pd.read_csv(
    r"G:\Alexey\Documents\Raznoe\Studium\Geek Brains\Python\PYTHON-MAIN\5. Data Science\14.DATACAMP\Time_Series\01_Manipulating_Time_Series_Data_in_Python\stock_data\yahoo.csv")
yahoo["date"] = pd.to_datetime(yahoo["date"])

yahoo.set_index("date", inplace=True)

# %%
prices = pd.DataFrame()

for year in ["2013", "2014", "2015"]:
    price_per_year = yahoo.loc[year, ["price"]].reset_index(drop=True)
    price_per_year.rename(columns={"price": year}, inplace=True)
    prices = pd.concat([prices, price_per_year], axis=1)

# %%
prices.plot()
plt.show()

# %%
co = pd.read_csv(
    r"G:\Alexey\Documents\Raznoe\Studium\Geek Brains\Python\PYTHON-MAIN\5. Data Science\14.DATACAMP\Time_Series\01_Manipulating_Time_Series_Data_in_Python\air_quality_data\co_cities.csv")

co["date"] = pd.to_datetime(co["date"])
co.set_index("date", inplace=True)
co = co.asfreq('D')

# %%
co = co.asfreq("M")
co.plot(subplots=True)
plt.show()

# %%
# Get the total number of avocados sold of each size
import matplotlib.pyplot as plt

avocados = pd.read_pickle(
    r"G:\Alexey\Documents\Raznoe\Studium\Geek Brains\Python\PYTHON-MAIN\5. Data Science\14.DATACAMP\02.Data Manipulation with pandas\avoplotto.pkl")
nb_sold_by_size = avocados.groupby("size")["nb_sold"].sum()
nb_sold_by_size.plot(kind="bar", rot=45)
plt.show()

# %%
import pandas as pd

google = pd.read_csv(
    r"G:\Alexey\Documents\Raznoe\Studium\Geek Brains\Python\PYTHON-MAIN\5. Data Science\14.DATACAMP\Time_Series\01_Manipulating_Time_Series_Data_in_Python\stock_data\google.csv",
    parse_dates=["Date"], index_col="Date")

google = google.dropna()

google.rename(columns={"Close": "price"}, inplace=True)

google = google.asfreq("B")

# %%
google["shifted"] = google.price.shift()  # сдвиг на шаг вперёд
google["lagged"] = google.price.shift(periods=-1)  # сдвиг на шаг назад
google["change"] = google.price.div(
    google.shifted)  # x смещённый делённый на x предыдущий, т.е. получаем относительные изменения

google["return"] = google.change.sub(1).mul(100)  # получаем изменения в процентах
google["pct_change"] = google.price.pct_change().mul(100)  # тоже самое только через встроенную формулу
google["pct_change3d"] = google.price.pct_change(periods=3).mul(100)  # тоже самое изменение в процентах за 3 периода

google["diff_30"] = google.price.diff(30)  # x предыдущий минус х смещённый на 30, т.е. получаем изменение как разность
# Тот же самый результат можем получить так, т.е. столбцы diff_30 и change_30 будут совпадать:
google["shifted_30"] = google.price.shift(30)
google["change_30"] = google.price.sub(google.shifted_30)

# %%
# Можем посмотреть изменения цены по дням, месяцам и годам:
import matplotlib.pyplot as plt

# Create daily_return
google['daily_return'] = google.price.pct_change(1).mul(100)

# Create monthly_return
google['monthly_return'] = google.price.pct_change(30).mul(100)

# Create annual_return
google['annual_return'] = google.price.pct_change(360).mul(100)

# Plot the result
google[['price', 'daily_return', 'monthly_return', 'annual_return']].plot(subplots=True)
plt.show()

# %%
# Для сравнения тенденций временных рядов их нужно нормализовать, т.к. различные временные ряды могут начинаться на разных уровнях. Для нормализации делают так, чтобы, например, все ряды цен начинались с одного значения. Для этого делять каждую цену делять на первое значение в ряду и умножают на 100. В результате первая цена равна 1, а каждая последующая цена отражает относительное изменение начальной цены. Следовательно значение 120.99 значит, что цена выросла на 20.99%
first_price = google.price.iloc[0]
normalized = google.price.div(first_price).mul(100)
normalized.plot(title="Google Normalized Series")
plt.show()

# %%
stock_prices = pd.read_csv(
    r"G:\Alexey\Documents\Raznoe\Studium\Geek Brains\Python\PYTHON-MAIN\5. Data Science\14.DATACAMP\Time_Series\01_Manipulating_Time_Series_Data_in_Python\stock_data\stock_data.csv",
    parse_dates=["Date"], index_col="Date")
stock_prices3 = stock_prices[["AAPL", "AMGN", "AMZN"]]

# Нормализуем для трёх столбцов
stock_prices3_normalized = stock_prices3.div(stock_prices3.iloc[0])

# %%
# Загрузим показатели индекса S&P
sp_index = pd.read_csv(
    r"G:\Alexey\Documents\Raznoe\Studium\Geek Brains\Python\PYTHON-MAIN\5. Data Science\14.DATACAMP\Time_Series\01_Manipulating_Time_Series_Data_in_Python\stock_data\asset_classes.csv",
    parse_dates=["DATE"], index_col="DATE")

sp_index_sp = sp_index["SP500"]

# Объединяем:
prices = pd.concat([stock_prices3, sp_index_sp], axis=1).dropna()

# Нормализуем для всех столбцов
prices_normalize = prices.div(prices.iloc[0]).mul(100)

# Строим график и смотрим, как каждый показатель менялся относительно S&P и относительно друг друга
prices_normalize.plot()
plt.show()

# %%
# Можем посмотреть, как графики меняются относительно S&P. Для этого вычтем из них показатели S&P
diff = prices_normalize[["AAPL", "AMGN", "AMZN"]].sub(prices_normalize["SP500"], axis=0)  # axis = 0 выравнивает индекс
diff.plot()
plt.show()

# %%
# Ещё пример
stocks = pd.read_csv(
    r"G:\Alexey\Documents\Raznoe\Studium\Geek Brains\Python\PYTHON-MAIN\5. Data Science\14.DATACAMP\Time_Series\01_Manipulating_Time_Series_Data_in_Python\stock_data\nyse.csv",
    parse_dates=["date"], index_col="date")

dow_jones = pd.read_csv(
    r"G:\Alexey\Documents\Raznoe\Studium\Geek Brains\Python\PYTHON-MAIN\5. Data Science\14.DATACAMP\Time_Series\01_Manipulating_Time_Series_Data_in_Python\stock_data\dow_jones.csv",
    parse_dates=["date"], index_col="date")

data = pd.concat([stocks, dow_jones], axis=1)

data_normalize = data.div(data.iloc[0]).mul(100)
data_normalize.plot()
plt.show()

# %%
mfst_apple = pd.read_csv(
    r"G:\Alexey\Documents\Raznoe\Studium\Geek Brains\Python\PYTHON-MAIN\5. Data Science\14.DATACAMP\Time_Series\01_Manipulating_Time_Series_Data_in_Python\stock_data\msft_aapl.csv",
    parse_dates=["date"], index_col="date")
