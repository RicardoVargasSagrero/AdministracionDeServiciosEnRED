import time
import rrdtool
from getSNMP import consultaSNMP

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

def monitorioAgente(comAgente,ipAgente):
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
            monitorioAgente(comunidadAgentes[i],ipAgentes[i])
        else:
            print("Agente ",i+1, "= Down")
    agentesFile.close()
    print("\tINGRESE LA OPCION QUE DESEA REALIZAR","\n1.- Agregar dispositivo\n2.- Eliminar dispositivo",
        "\n3.-Reporte de informacion del dispositivo")
    choice = input("")
    if int(choice) == 1:
        agregarAgenteBD(totalAgentes)
    elif int(choice) == 2:
        eliminarAgente(totalAgentes,comunidadAgentes,ipAgentes)
