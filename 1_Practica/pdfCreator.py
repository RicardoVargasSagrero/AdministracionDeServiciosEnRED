from fpdf import FPDF
from getSNMP import consultaSNMP
def numeroInterfaces(comunidadSNMP, host):
    idTable = 1
    oid = "1.3.6.1.2.1.2.2.1.2." + str(idTable)
    result = consultaSNMP(comunidadSNMP, host, oid)
    while result.find("No") == -1 and result.find("noSuchName") == -1:
        idTable += 1
        oid = "1.3.6.1.2.1.2.2.1.2." + str(idTable)
        result = consultaSNMP(comunidadSNMP, host, oid)
    return idTable

def crearPDF(comunidadSNMP, host,num):
    # ORDEN de PDF nombre, versión y logo del sistema operativo, la ubicación geográfica, el número de puertos,
    # el tiempo de actividad desde el último reinicio, comunidad, IP
    SO = consultaSNMP(comunidadSNMP, host, "1.3.6.1.2.1.1.1.0")
    version = consultaSNMP(comunidadSNMP, host, "1.3.6.1.2.1.1.5.0")
    ubicacion = consultaSNMP(comunidadSNMP, host, "1.3.6.1.2.1.1.6.0")
    totalInterfaces = numeroInterfaces(comunidadSNMP, host)
    ultimoReinicio = consultaSNMP(comunidadSNMP, host, "1.3.6.1.2.1.1.3.0")
    pdf = FPDF(orientation="P", unit="mm", format="letter")
    pdf.add_page()
    pdf.set_font("Arial", size=18, style="B")
    pdf.cell(200, 10, txt="Práctica 1 - Adquisición de información usando SNMP", ln=1, align="C")
    pdf.set_font("Arial", size=14)
    pdf.cell(100, 5, txt="", ln=1, align="C")
    pdf.cell(100, 5, txt="Nombre del Sistema Operativo = "+SO, ln=1, align="L")
    pdf.cell(100, 5, txt="Versión = "+version, ln=1, align="L")
    pdf.cell(100, 5, txt="Ubicacion geografica = "+ubicacion, ln=1, align="L")
    pdf.cell(100, 5, txt="Número total de puertos = "+str(totalInterfaces), ln=1, align="L")
    pdf.cell(100, 5, txt="Tiempo de actvidad desde el último reinicio = "+ultimoReinicio, ln=1, align="L")
    pdf.cell(100, 5, txt="Comunidad = "+comunidadSNMP, ln=1, align="L")
    pdf.cell(100, 5, txt="IP = "+host, ln=1,align="L")
    if SO.find("Hardware:") != -1:
        pdf.image("windows10.png", x=130, y=15, w=80, h=45)
    elif SO.find("Linux") != -1:
        pdf.image("ubuntu.png", x=150, y=25, w=50, h=20)
    else:
        pdf.image("mac.png", x=150, y=25, w=50, h=20)
    pdf.image("Multicast_paquetes_"+str(num)+".png", x=10, y=75, w=95, h=40)
    pdf.image("IP_paquetes_"+str(num)+".png", x=110, y=75, w=95, h=40)
    pdf.image("ICMP_mensajes_"+str(num)+".png", x=10, y=125, w=95, h=40)
    pdf.image("TCP_segmentos_"+str(num)+".png", x=110, y=125, w=95, h=40)
    pdf.image("UDP_datagramas_"+str(num)+".png",x=50, y=200, w=95, h=40)
    pdf.output("prueba"+str(SO)+"_Agente_"+str(num)+".pdf")
    print("prueba"+str(SO)+"_Agente_"+str(num)+".pdf")

#print("Inicio de creacion de PDF")
#comSNMP = "comunidad4cm3"
#host = "localhost"
#crearPDF(comSNMP, host)
# MODIFICACION EN EL NOMBRE DE SALIDA