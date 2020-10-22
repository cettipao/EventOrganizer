import openpyxl
from config.settings import BASE_DIR

def genExcel(invitados):

    doc = openpyxl.load_workbook(BASE_DIR + '/static/' + 'sheet.xlsx')

    sheets = doc.sheetnames #.sheetnames accede a las hojas dentro del doc y las convierte en lista

    hoja1 = doc['Hoja 1']#Guardamos en una variable la info de una hoja

    hoja1['A1'] = "Nombre"
    hoja1['B1'] = "Numero"

    for i in range(len(invitados)):
        hoja1['A' + str(i+2)] = invitados[i].nombre
        hoja1['B' + str(i+2)] = invitados[i].numero

    doc.save(BASE_DIR + '/static/' + 'InvitadosEvento.xlsx')