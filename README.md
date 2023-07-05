# TFG-PY-Power_consumption_estimate

En este proyecto se llevará a cabo el estudio de los datos de consumo eléctrico de clientes pertenecientes a una comercializadora.

Los datos se obtienen de una página donde se encuentran públicados (https://www.ucd.ie/issda/data/commissionforenergyregulationcer/). En ellos se muestran millones de filas con los siguientes datos anonimizados:

- Id de usuarios

- Marca de tiempo definida de la siguiente forma (5 dígitos):
    - Los primeros 3 dígitos muestran la cantidad de días que han pasado desde el 1 de enero del año 2009.
    - Los últimos 2 dígitos muestran el tramo horario del día en el que se ha realizado la medida. Los tramos se dividen en medias horas, es decir,
      van desde las 00:00-00:29, 00:30-00:59, etc, hasta las 23:30-23:59 y se representan con números, siendo el 00 el primer tramo, el 01 el segundo, y así hasta el 47 que sería el último, respectivamente.

- Consumo en kWh del usuario


Para el estudio y análisis de los datos, primero procederemos con la preparación de estos:

  - Se cogerán todos los datos de cada usuario y se unificarán por horas en lugar de medias horas, por lo que para cada tramo deberían juntarse dos valores, teniendo así 24 datos cada día de cada usuario.

  - Posteriormente se unificarán los datos de forma que se muestre cada tramo horario con el sumatorio de consumo eléctrico y el número total de usuarios de los que se tienen datos en la correspondiente fecha.

  - Una vez conseguido esta preparación de los datos, se juntarán todos los 6 archivos disponibles ya procesados y se juntará toda la información en un único archivo con el que trabajaremos.

Una vez preparados los datos, contamos con 12864 filas útiles, lo que se traduce en 536 días con 24 valores de consumo cada uno.