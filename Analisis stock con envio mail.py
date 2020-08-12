#### importando librerías necesarias ####

from alpha_vantage.timeseries import TimeSeries
import time
import pandas as pd
import os
import smtplib
from email.message import EmailMessage

#### Datos de API y Stock ####
# api key obtenida de alphavantage.co y el código de la stock que queramos analizar
api_key = "4PA4GRCEZKV1KYH8"
stock_symbol = "TSLA"  # en este caso es para la acción de Tesla
ts = TimeSeries(key=api_key, output_format="pandas") # Creando la serie de tiempo, usando la key obtenida y seteando la salida a formato pandas

#### datos de mail ####

EMAIL_ADDRESS = "--email-que-envía--"    #Email desde el cual enviamos la notificación
EMAIL_PASSWORD = "--contraseña--"          #Contraseña del mail
EMAIL_ADDRESS_TO = "--email-que-recibe--" #Email destinatario

# Loop infinito para obtener los datos cada 5 minutos (En caso de usar la función de enviar mail, cada 1 hora o más convendría poner)
# NOTA: Alpha_vantage solo te permite realizar hasta 5 llamados por minuto, y 500 llamados por día. (Cada 5 min = 288 llamados diarios)

while True:
    data, meta_data = ts.get_intraday(symbol=stock_symbol, interval="5min", outputsize="full")
    per_change = data["4. close"].pct_change() # Para tomar solo los valores de cierre de la acción.
    time.sleep(300) #cada 5 min
    print(per_change)  # cambio porcentual en el valor de cierre de la acción
    last_change = per_change[-1]
    if abs(last_change) > 0.0005: #alerta cuando varía segun lo que queramos, en este caso 0.0005
        print(stock_symbol + " Alerta:" + str(last_change))
        ############## Crea una instancia con los datos del msj a enviar
        msg = EmailMessage()
        msg["Subject"] = "Alerta " + stock_symbol
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS_TO
        msg.set_content("El stock ha tenido una variación porcentual de " + str(last_change))
        ############## Enviando el msj
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Notificación enviada al mail indicado.")


# NOTA: Los 2 primeros print dentro del while se encuentran para testear, si se piensa dejar funcionando solo el script pueden quitarse.
# NOTA: Las variables "EMAIL_ADDRESS", "EMAIL_PASSWORD" & "EMAIL_PASSWORD_TO" es conveniente utilizarlas como environment variables y usar la librería os para utilizarlas en el script.