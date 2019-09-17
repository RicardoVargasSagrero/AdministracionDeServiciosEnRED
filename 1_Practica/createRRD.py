#!/usr/bin/env python

import rrdtool
ret = rrdtool.create("IP_paquetes_2.rrd",
                     "--start",'N',
                     "--step",'60',
                     "DS:inoctets:COUNTER:600:U:U",
                     "DS:outoctets:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:1:600",
                     "RRA:AVERAGE:0.5:1:600")

if ret:
    print (rrdtool.error())
