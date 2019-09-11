import time
import rrdtool
from getSNMP import consultaSNMP
total_input_traffic_mul = 0
total_output_traffic = 0

while 1:
    print("UpdateRRD.py_ ")
    total_input_traffic_mul = int(
        consultaSNMP('comunidad4cm3', 'localhost',
                     '1.3.6.1.2.1.2.2.1.10.3'))
    valor = "N:" + str(total_input_traffic_mul)
    print (valor)
    rrdtool.update('traficoMulticastRED.rrd', valor)
    rrdtool.dump('traficoMulticastRED.rrd', 'traficoMulticastRED.xml')
    time.sleep(1)

if ret:
    print (rrdtool.error())
    time.sleep(300)