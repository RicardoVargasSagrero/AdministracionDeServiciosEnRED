import time
import rrdtool
from getSNMP import consultaSNMP
import threading
from pdfCreator import crearPDF
from pysnmp.hlapi import *
import time

def extraerAgentesTxt(comunidadAgentes,ipAgentes):
    totalAgentes = 0
    for linea in agentesFile.readlines():
        if linea.find('#') != -1:
            totalAgentes +=1
        elif linea.find('nombre =') != -1:
            x = linea.split('=')
            y = x[1].split('\n')
            comunidadAgentes.append(y[0])
        elif linea.find('direccion =') != -1:
            x = linea.split('=')
            y = x[1].split('\n')
            ipAgentes.append(y[0])
    return totalAgentes

def inicioAgente(comAgente, ipAgente):
    # Numero de puertos disponibles por agente
    print("\tNumero de puertos diponibles")
    interfaces = []
    idTable = 1
    oid = "1.3.6.1.2.1.2.2.1.2." + str(idTable)
    result = consultaSNMP(comAgente, ipAgente, oid)
    while result.find("No") == -1 and result.find("noSuchName") == -1:
        interfaces.append(result)
        idTable += 1
        oid = "1.3.6.1.2.1.2.2.1.2." + str(idTable)
        result = consultaSNMP(comAgente, ipAgente, oid)
    print(*interfaces,sep="\n")


def agregarAgenteBD(totalAgentes):
    totalAgentes +=1
    host = str(input("Ingrese el nombre del host o direccion IP:\n"))
    version = str(input("Ingrese la version SNMP:\n"))
    comunidad = str(input("Ingrese el nombre de la comunidad:\n"))
    puerto = input("Ingrese el puerto:\n")
    agentesFile = open("agentes.txt","a+")

    agentesFile.write("\n#Agente ")
    agentesFile.write(str(totalAgentes))
    agentesFile.write("\nnombre =")
    agentesFile.write(comunidad)
    agentesFile.write("\n")
    agentesFile.write("direccion =")
    agentesFile.write(host)
    agentesFile.close()

def eliminarAgente(totalAgentes,comunidadAgentes,ipAgentes):
    nombre = str(input("Ingrese el nombre del host o dirrecion IPv4 del agente:\n"))
    for i in range(totalAgentes):
        print(i)
        if ipAgentes[i].find(nombre) != -1:
            j = ipAgentes.index(nombre)
    ipAgentes.remove(nombre)
    comunidadAgentes.remove(comunidadAgentes[j])
    totalAgentes -= 1
    agentesFile = open("agentes.txt","w")
    for i in range(totalAgentes):
        agentesFile.write("#Agente ")
        agentesFile.write(str(i+1))
        agentesFile.write("\nnombre =")
        agentesFile.write(comunidadAgentes[i])
        agentesFile.write("\ndireccion =")
        agentesFile.write(ipAgentes[i])
        agentesFile.write("\n")
    agentesFile.close()

def updateAgenteComun1(com,host):
    total_output_received= 0

    while True:
        # print("IP_UpdateRRD.py_ ")
        #Consulta multicast
        total_input_deliveries = int(
            consultaSNMP(com, host, "1.3.6.1.2.1.2.2.1.12.5"))
        valor = "N:" +str(total_input_deliveries)
        rrdtool.update("Multicast_paquetes_1.rrd", valor)
        rrdtool.dump("Multicast_paquetes_1.rrd", "Multicast_paquetes_1.xml")

        total_output_deliveries = 0
        #Consulta IP
        total_input_deliveries = int(
            consultaSNMP(com, host,
                         "1.3.6.1.2.1.4.9.0"))
        total_output_received = int(
            consultaSNMP(com, host,
                         "1.3.6.1.2.1.4.3.0"))
        valor = "N:" + str(total_input_deliveries) + ':' + str(total_output_received)
        rrdtool.update("IP_paquetes_1.rrd", valor)
        rrdtool.dump("IP_paquetes_1.rrd", "IP_update_1.xml")

        total_output_deliveries = 0
        #Consultas ICMP
        total_input_deliveries = int(consultaSNMP(com, host,
                                                  "1.3.6.1.2.1.5.14.0"))
        valor = "N:" + str(total_input_deliveries)
        rrdtool.update("ICMP_mensajes_1.rrd", valor)
        rrdtool.dump("ICMP_mensajes_1.rrd", "ICMP_update_1.xml")

        total_output_deliveries = 0
        #Consulta TCP
        total_input_deliveries = int(consultaSNMP(com, host,
                                                  "1.3.6.1.2.1.6.11.0"))
        valor = "N:" + str(total_input_deliveries)
        rrdtool.update("TCP_segmentos_1.rrd", valor)
        rrdtool.dump("TCP_segmentos_1.rrd", "TCP_segmentos_1.xml")

        total_output_deliveries = 0
        #Consulta UDP
        total_input_deliveries = int(consultaSNMP(com, host,
                                                  "1.3.6.1.2.1.7.3.0"))
        valor = "N:" + str(total_input_deliveries)
        rrdtool.update("UDP_datagram_1.rrd", valor)
        rrdtool.dump("UDP_datagram_1.rrd", "UDP_datagramas_1.xml")
        time.sleep(1)



def updateAgenteComun2(com, host, DB, oid, xml):
    total_output_received = 0

    while True:
        # print("IP_UpdateRRD.py_ ")
        # Consulta multicast
        total_input_deliveries = int(
            consultaSNMP(com, host, oid))
        valor = "N:" + str(total_input_deliveries)
        rrdtool.update("Multicast_paquetes_2.rrd", valor)
        rrdtool.dump("Multicast_paquetes_2.rrd", "Multicast_paquetes_2.xml")
        total_output_deliveries = 0
        # Consulta IP
        total_input_deliveries = int(
            consultaSNMP(com, host,
                         '1.3.6.1.2.1.4.9.0'))
        total_output_received = int(
            consultaSNMP(com, host,
                         '1.3.6.1.2.1.4.3.0'))
        valor = "N:" + str(total_input_deliveries) + ':' + str(total_output_received)
        rrdtool.update("IP_paquetes_2.rrd", valor)
        rrdtool.dump("IP_paquetes_2.rrd", "IP_update_2.xml")

        total_output_deliveries = 0
        # Consultas ICMP
        total_input_deliveries = int(consultaSNMP(com, host,
                                                  "1.3.6.1.2.1.5.14.0"))
        valor = "N:" + str(total_input_deliveries)
        rrdtool.update("ICMP_mensajes_2.rrd", valor)
        rrdtool.dump("ICMP_mensajes_2.rrd", "ICMP_update_2.xml")

        total_output_deliveries = 0
        # Consulta TCP
        total_input_deliveries = int(consultaSNMP(com, host,
                                                  "1.3.6.1.2.1.6.11.0"))
        valor = "N:" + str(total_input_deliveries)
        rrdtool.update("TCP_segmentos_2.rrd", valor)
        rrdtool.dump("TCP_segmentos_2.rrd", "TCP_segmentos_2.xml")

        total_output_deliveries = 0
        # Consulta UDP

        total_input_deliveries = int(consultaSNMP(com, host,
                                                  "1.3.6.1.2.1.7.3.0"))
        valor = "N:" + str(total_input_deliveries)
        rrdtool.update("UDP_datagram_2.rrd", valor)
        rrdtool.dump("UDP_datagram_2.rrd", "UDP_datagramas_2.xml")
        time.sleep(1)


def crearGraficaDoble(segundos, nombreImagen, etiquetaVertical, tituloTabla, DB):
    tiempo_actual = int(time.time())
    tiempo_final = tiempo_actual - int(segundos)
    tiempo_inicial = tiempo_final - 25920000

    ret = rrdtool.graph(nombreImagen,
                        "--start="+ str(tiempo_final),
#                       "--end","N",
                        "--vertical-label="+str(etiquetaVertical),
                        "--title="+str(tituloTabla),
                        "DEF:inoctets="+str(DB)+":inoctets:AVERAGE",
                        "DEF:outoctets="+str(DB)+":outoctets:AVERAGE",
                        "AREA:inoctets#00FF00:In traffic",
                        "LINE1:outoctets#0000FF:Out traffic")


def crearGraficaSencilla(segundos, nombreImagen, etiquetaVertical, tituloTabla, DB):
    tiempo_actual = int(time.time())
    tiempo_final = tiempo_actual - int(segundos)
    tiempo_inicial = tiempo_final - 25920000

    ret = rrdtool.graph(nombreImagen,
                        "--start=" + str(tiempo_final),
                        #                       "--end","N",
                        "--vertical-label=" + str(etiquetaVertical),
                        "--title=" + str(tituloTabla),
                        "DEF:inoctets=" + str(DB) + ":inoctets:AVERAGE",
                        "AREA:inoctets#00FF00:In traffic")


# MAIN
while True:
    agentesFile = open("agentes.txt","r")
    comunidadAgentes = []
    ipAgentes = []
    totalAgentes = extraerAgentesTxt(comunidadAgentes,ipAgentes)
    result = ""
    print("\t INICIO SNMP\n Numero de dispositivos que se estan monitoriando\n\t",totalAgentes)
    for i in range(totalAgentes):
        result = consultaSNMP(comunidadAgentes[i],ipAgentes[i],"1.3.6.1.2.1.1.1.0")
        if result.find("No SNMP response") == -1:
            print("Agente ",i+1,"=",result, "Up")
            inicioAgente(comunidadAgentes[i], ipAgentes[i])
            # Para este agente se selecciono la interfaz 5

            t1 = threading.Thread(name="hilo_TCP_Agente_1", target=updateAgenteComun1,
                                  args=(comunidadAgentes[i],
                                        ipAgentes[i]))
            # Segundo agente, se selecciona la interfaz 9 para la primera pregunta
            t2 = threading.Thread(name="hilo_TCP_Agente_2", target=updateAgenteComun2,
                                  args=(comunidadAgentes[1],
                                        ipAgentes[1],
                                        "TCP_segmentos_2.rrd",
                                        "1.3.6.1.2.1.6.11.0",
                                        "TCP_segmentos_2.xml"))

            # Con esta funcion estamos activando los hilos de dos agentes estaticos
            if not t1.is_alive() and not t2.is_alive():
                t1.start()
                t2.start()
        else:
            print("Agente ",i+1, "= Down")
    agentesFile.close()
    print("\tINGRESE LA OPCION QUE DESEA REALIZAR","\n1.- Agregar dispositivo\n2.- Eliminar dispositivo",
        "\n3.-Reporte de informacion del dispositivo")
    choice = input("")
    if int(choice) == 1:
        agregarAgenteBD(totalAgentes)
    elif int(choice) == 2:
        eliminarAgente(totalAgentes, comunidadAgentes, ipAgentes)
    elif int(choice) == 3:
        segundos = int(input("Ingrese el tiempo incial en segundos:\n"))
        crearGraficaSencilla(segundos,"Multicast_paquetes_1.png","Trafico de RED Multicast recibido",
                             "Trafico de RED Multicast recibido","Multicast_paquetes_1.rrd")
        crearGraficaDoble(segundos, "IP_paquetes_1.png", "Paquetes", "Paquetes IP recibido exitosamente",
                          "IP_paquetes_1.rrd")
        crearGraficaSencilla(segundos, "ICMP_mensajes_1.png", "Mensajes", "Mensajes de respuesta ICMP",
                             "ICMP_mensajes_1.rrd")
        crearGraficaSencilla(segundos, "TCP_segmentos_1.png", "Segmentos", "Segmentos enviados TCP",
                             "TCP_segmentos_1.rrd")
        crearGraficaSencilla(segundos, "UDP_datagramas_1.png", "Datagramas","Datagramas recibidos que no puedieron UDP",
                             "UDP_datagram_1.rrd")
        # Segunda
        crearGraficaSencilla(segundos, "Multicast_paquetes_2.png", "Trafico de RED Multicast recibido",
                             "Trafico de RED Multicast recibido", "Multicast_paquetes_2.rrd")
        crearGraficaDoble(segundos, "IP_paquetes_2.png", "Paquetes", "Paquetes IP recibido exitosamente",
                          "IP_paquetes_2.rrd")
        crearGraficaSencilla(segundos, "ICMP_mensajes_2.png", "Mensajes", "Mensajes de respuesta ICMP",
                             "ICMP_mensajes_2.rrd")
        crearGraficaSencilla(segundos, "TCP_segmentos_2.png", "Segmentos", "Segmentos enviados TCP",
                             "TCP_segmentos_2.rrd")
        crearGraficaSencilla(segundos, "UDP_datagramas_2.png", "Datagramas", "Datagramas recibidos que no puedieron UDP",
                             "UDP_datagram_2.rrd")
        crearPDF(comunidadAgentes[0],ipAgentes[0],1)
        crearPDF(comunidadAgentes[1],ipAgentes[1],2)

    else:
        print("Operacion aun no soportada")
