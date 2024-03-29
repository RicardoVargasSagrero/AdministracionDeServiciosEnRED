"""
SNMPv2c
+++++++

Send SNMP GET request using the following options:

* with SNMPv2c, community 'SNMPcom'
* over IPv4/UDP
* to an Agent at localhost
* for two OIDs in string form 

Functionally similar to:

| $ snmpget -v2c -c SNMPcom localhost 1.3.6.1.2.1.1.1.0 1.3.6.1.2.1.1.6.0

"""#
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('comunidad4cm3'),
           UdpTransportTarget(('localhost', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),
           ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0')))
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))