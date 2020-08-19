import opendssdirect
import opendss.class_opendss
import opendss.class_conn
import opendss.class_data

from opendss.class_conn import C_OpenDSSDirect_Conn

ListaBarras = C_OpenDSSDirect_Conn()
Listona = [ListaBarras.get_Circuit_AllBusNames()]
print(Listona)
