from pysnmp.hlapi import *
import time

def consultaSNMP(comunidad,host,oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        # print(errorIndication)
        resultado = str(errorIndication)
    elif errorStatus:
        resultado = '%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
    elif errorIndex:
        resultado = str(errorIndex)
    else:
        try:
            for varBind in varBinds:
                varB = (' = '.join([x.prettyPrint() for x in varBind]))
                resultado = varB.split()[2]
        except IndexError as error:
            resultado = "No encontrado"
    return resultado


# while True:
    # print(consultaSNMP("comunidad4cm3","localhost","1.3.6.1.2.1.5.1.0"))
    """Consulta SNMP a grupo interfaces 1.3.6.1.2.1.2"""

    # print(consultaSNMP("comunidad4cm3","localhost","1.3.6.1.2.1.1.1.0"))
    """for i in range(1,8):
        cadena = "1.3.6.1.2.1.1."
        cadena+= str(i)+".0";
        print("Consulta ", i, " = ",consultaSNMP("comunidad4cm3","localhost",cadena))"""
    # time.sleep(1)