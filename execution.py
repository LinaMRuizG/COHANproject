"""
Proyecto: COAN facturación
Desarrollador: Lina M. Ruiz G. y Anderson A. Ruales B.
Contacto: lina.ruiz2@udea.edu.co
Empresa: iDAM
Version: 0.1.0
"""
import time

from datosFacturacion import datosFacturacion

if __name__ == "__main__":
    """

    Formato de fecha yyyy-mm-dd
    
    """
    fecha_init="2023-1-6"
    #fecha_end="2023-3-31"
    
    datos = datosFacturacion(fecha_init)
    datos.run()
    """intentos=0
    while intentos<1:
        print("Intento:{}".format(intentos))
        try:
            try:
                datos = datosFacturacion(fecha_init,fecha_end)
            except:
                datos = datosFacturacion(fecha_init)

            value=datos.run()
            intentos=4
            if value==1:
                intentos=0
        except:
            intentos+=1
        time.sleep(120)"""

    
    
    #datos = datosFacturacion(fecha_init,fecha_end)
    #datos.run()
    #print("init")
    #datos.fechas()
    #print("End")
    #datos.fechas_old()
    #datos.allFilesToDownload()
    #datos.filesMissingToDownload()
    #datos.loginPage()
    #datos.navigatingNextPages()
    #datos.mergingCsv()
    #datos.descargaCsv() 
    #datos.verifyingDownload()
    #datos.renamingFiles()
    #datos.removingFiles()

