import rrdtool


# Para tomar el tiempo actual
timeActual = time.time()

# El tiempo de incio menos 300s (5 minutos)
timeInicial = timeActual - 300

ret = rrdtool.create("test.rrd",
                     "--start", '920804400',
                     "DS:speed:COUNTER:600:U:U", #Especifica los limites U:U (Nombre:tipo de dato:
                     "RRA:AVERAGE:0.5:1:24", #Round Robin: promedio: al menos la mitad: periodicidad de 1 step (300s):tomara 24 datos
                     "RRA:AVERAGE:0.5:6:10") #Round Robin:promedio:al menos la mitad de los datos: cada 6 steps: tomata 10 datos

"""Esta funcion actualizar la base de datos"""
upd = rrdtool.update('test.rrd','920804700:12345',
                     '920805000:12357','920805300:12363',
                     '920805600:12363','920805900:12363',
                     '920806200:12373','920806500:12383',
                     '920806800:12393', '920807100:12399',
                     '920807400:12405', '920807700:12411',
                     '920808000:12415','920808300:12420',
                     '920808600:12422','920808900:12423')
rrdtool.dump('test.rrd','test.xml');
print (rrdtool.fetch('test.rrd','AVERAGE',
                    "--start", '920804400',
                    "--end",'920809200'))

gra= rrdtool.graph("speed.png",
                   "--start", "920804400",
                   "--end", "920808000",
                   "DEF:myspeed=test.rrd:speed:AVERAGE", #Define la variable myspeed

                   "LINE1:myspeed#FF0000")