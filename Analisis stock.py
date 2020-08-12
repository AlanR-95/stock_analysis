# api key obtenida de alphavantage.co y el código de la stock que queramos analizar

api_key = "4PA4GRCEZKV1KYH8"
stock_symbol = "TSLA"  #en este caso es para la acción de Tesla

# importando librerías necesarias

from alpha_vantage.timeseries import TimeSeries
import time
import pandas as pd


# Creando la serie de tiempo, usando la key obtenida y seteando la salida a formato pandas

ts = TimeSeries(key=api_key, output_format="pandas")


# Loop infinito para obtener los datos cada 3 minutos
# NOTA: Alpha_vantage solo te permite realizar hasta 5 llamados por minuto, y 500 llamados por día. (Cada 5 min = 288 llamados diarios)

while True:
    data, meta_data = ts.get_intraday(symbol=stock_symbol, interval="5min", outputsize="full")
    per_change = data["4. close"].pct_change() # Para tomar solo los valores de cierre de la acción.
    time.sleep(300) #cada 5 min
    print(per_change)  # cambio porcentual en el valor de cierre de la acción
    last_change = per_change[-1]
    if abs(last_change) > 0.0005: #alerta cuando varía segun lo que queramos
        print(stock_symbol + " Alerta:" + str(last_change))