from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import os
import glob
import pandas as pd
import calendar
from dateutil.relativedelta import relativedelta


class datosFacturacion:


    def __init__(self,fecha_init,fecha_end=datetime.datetime.now().strftime("%Y-%m-%d")):
       
        #stting driver
        self.loginWeb = "https://www.herinco.com/herinco/index.jsp?m=l"
        self.PATH = "/home/lina/chromedriver_linux64/chromedriver" # I do not know if this is necesary
        self.downloadPATH = "/Users/linaruiz/Documents/COHANproject/csv"

        self.time_star=fecha_init
        self.time_end=fecha_end
       
        self.driver = webdriver.Chrome()
        
        #ajustar preferencias de la ruta de descarga
        
        self.driverOptions = Options()
        self.driverOptions.add_experimental_option("prefs",{"download.default_directory" : self.downloadPATH})
       
        # fechas
        self.today0 = datetime.datetime.today()
        self.fechaIni = {"year": 0 ,"month":0,"day": 0 }
        self.fechaFin = {"year": 0 ,"month":0,"day": 0 }
        self.listFechasIniPorMes = []
        self.listFechasFinPorMes = []
        self.monthsCode = { "0": "Enero", 
                           "1":"Febrero", 
                           "2":"Marzo", 
                           "3":"Abril", 
                           "4":"Mayo", 
                           "5":"Junio", 
                           "6":"Julio", 
                           "7":"Agosto", 
                           "8":"Septiembre", 
                           "9":"Octubre", 
                           "10":"Noviembre", 
                           "11":"Diciembre"}
        self.filesNames = []
        self.fileNamesPos = []
        self.missingFiles = []
    
    def fechas(self):

        date_time_star=datetime.datetime.strptime(self.time_star, '%Y-%m-%d') #time init
        date_time_end=datetime.datetime.strptime(self.time_end, '%Y-%m-%d') # time end
        #diff = relativedelta(date_time_end,date_time_star)
        diff_in_months = len(pd.date_range(self.time_star,self.time_end,freq="MS").strftime("%Y-%m"))# diff.months + diff.years * 12
        
        if(date_time_star.month==date_time_end.month-diff_in_months) :
            diff_in_months=diff_in_months+1
        if(date_time_star.year==date_time_end.year-1) & (diff_in_months==1):
            diff_in_months=2

        list_fecha_star=[]
        list_fecha_end=[]
        for i in range(int(diff_in_months)+1):
            day = (date_time_star + relativedelta(months=+i))#.strftime("%Y-%m-%d")
            #print(day)
            if i==0:
                start = datetime.date(date_time_star.year,date_time_star.month,date_time_star.day)
                list_fecha_star.append(start)
                # end
                last_day = calendar.monthrange (date_time_star.year, date_time_star.month) [1]
                end = datetime.date(date_time_star.year,date_time_star.month,last_day)
                list_fecha_end.append(end)
                #print(start,end)

            elif i==int(diff_in_months)-1:
                start = datetime.date(date_time_end.year,date_time_end.month,1)
                list_fecha_star.append(start)
                # end
                end = datetime.date(date_time_end.year,date_time_end.month,date_time_end.day)
                list_fecha_end.append(end)
                #print(start,end)

            else:
                start = datetime.date(day.year,day.month,1)
                list_fecha_star.append(start)
                # end
                last_day = calendar.monthrange (day.year, day.month) [1]
                end = datetime.date(day.year,day.month,last_day)
                list_fecha_end.append(end)

        #self.listFechasIniPorMes = []
        #self.listFechasFinPorMes = []
        

        for i in range(len(list_fecha_star)):
            self.listFechasIniPorMes.append({"year": list_fecha_star[i].strftime("%Y") ,\
                                             "month":str(int(list_fecha_star[i].month)-1),\
                                            "day":str(list_fecha_star[i].day)})
            
            self.listFechasFinPorMes.append({"year": list_fecha_end[i].strftime("%Y") ,\
                                             "month":str(int(list_fecha_end[i].month)-1),\
                                            "day":str(list_fecha_end[i].day)})


        #print(self.listFechasIniPorMes)
        #print("..........")
        #print(self.listFechasFinPorMes)

    def fechas_old(self):

        """this builds the list of initial and final day of each months. The months are from january 2023 until today"""
        
        today = self.today0
        months = int(today.strftime("%m"))
        
        self.listFechasIniPorMes = [{"year": today.strftime("%Y") ,"month":str(months-1),"day":"1"}]
        self.listFechasFinPorMes = [{"year": today.strftime("%Y") ,"month":str(months-1),"day":str(int(today.strftime("%d")))}]
        
        for i in range(months-1,0,-1):
            self.listFechasIniPorMes.append({"year": today.strftime("%Y") ,"month":str(i-1),"day":"1"})
            last = datetime.datetime(2023,i+1,1)-datetime.timedelta(days = 1)
            self.listFechasFinPorMes.append({"year": last.strftime("%Y") ,"month":str(int(last.strftime("%m"))-1),"day":str(int(last.strftime("%d")))})


    def loginPage (self):

        """this sing into login page. Be careful because it has the user and password information"""

        # navigate to the login page
        self.driver.get(self.loginWeb)


        # fill in the login form
        
        username_input = self.driver.find_element(by=By.ID, value ="username")
        username_input.send_keys("USER")

        password_input = self.driver.find_element(by=By.ID, value = "password")
        password_input.send_keys("PASSWORD")
        password_input.send_keys(Keys.RETURN)

        #Maximizing the window
        self.driver.maximize_window()

    def navigatingNextPages(self):

        """this click a consecutive set of elements until get into the Auditorias page"""

        #page1: selecting an option and click button INGRESAR
        select = self.driver.find_element(By.XPATH, "//select[@id='cmbEmpresa']")
        Select(select).select_by_value("1")
        
        buttonIngresar = self.driver.find_element(by = By.ID, value = "btnGuardar")
        buttonIngresar.click()

        #page2: consecutive clicking to get into the Auditorias page. Is there a way to make the next code more short ?
        #because it repeats each time the same

        time.sleep(7)# KEEP THIS: It gives enough time to attach the next elements to the page 

        wait = WebDriverWait(self.driver, 10)
        button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='toggle-menu']")))
        self.driver.implicitly_wait(100)
        ActionChains(self.driver).move_to_element(button).click(button).perform()

        time.sleep(7)

        wait = WebDriverWait(self.driver, 60)
        button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='#mm-m0-p2']")))
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()

        time.sleep(7)
        
        wait = WebDriverWait(self.driver, 60)
        button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='frm_Auditorias.jsp']")))
        self.driver.implicitly_wait(10)
        ActionChains(self.driver).move_to_element(button).click(button).perform()

        #time.sleep(2)

    def autidoriasPageDescarga(self):

        """it set the dates to generate a report from Auditorias page"""

        #setting fecha inicial
        time.sleep(2)
        buttonfechaInicial = self.driver.find_element(by=By.ID, value = "txtFechaInicial")
        buttonfechaInicial.click()

        time.sleep(2)
        selectYear = self.driver.find_element(By.XPATH, "//select[@class='ui-datepicker-year']")
        Select(selectYear).select_by_value(self.fechaIni["year"])#year
        
        time.sleep(2)
        selectMonth = self.driver.find_element(By.XPATH, "//select[@class='ui-datepicker-month']")
        Select(selectMonth).select_by_value(self.fechaIni["month"])#month
        
        time.sleep(2)
        buttonDay = self.driver.find_element(By.LINK_TEXT,self.fechaIni["day"])#day
        buttonDay.click()

        #setting fecha final
        time.sleep(2)
        buttonfechaFinal = self.driver.find_element(by=By.ID, value = "txtFechaFinal")
        buttonfechaFinal.click()
        time.sleep(2)
        selectYear = self.driver.find_element(By.XPATH, "//select[@class='ui-datepicker-year']")
        Select(selectYear).select_by_value(self.fechaFin["year"])#year
        time.sleep(2)
        selectMonth = self.driver.find_element(By.XPATH, "//select[@class='ui-datepicker-month']")
        Select(selectMonth).select_by_value(self.fechaFin["month"])#month: 0:Jan, 1:Feb, 2:Mar, 3:Apr, 4:May, 5:Jun, 6:Jul, 7:Aug, 8:Sep, 9:Oct, 10:Nov, 11:Dec
        time.sleep(2)
        buttonDay = self.driver.find_element(By.LINK_TEXT,self.fechaFin["day"])#day
        buttonDay.click()

        time.sleep(2)

        buttonGenerarRepo= self.driver.find_element(by = By.ID, value = "generarReporte")
        buttonGenerarRepo.click()

        #time.sleep(5)


    def verifyingDownload(self):

        """it allows to give some time (until maxTime) for a full download"""

        maxTime = 300#5 minutes is the maximum time set to download
        seconds = 0
        partiallyDownload = True
        while partiallyDownload and seconds < maxTime: 
            time.sleep(1)
            partiallyDownload = False
            for fname in os.listdir(self.downloadPATH):
                if fname.endswith('.crdownload'):
                    partiallyDownload = True
            seconds += 1
            #print(seconds)
        
        if seconds == maxTime:
            print("se excedio el tiempo maximo de espera para la descarga")

    def renamingFiles(self):
        
        oldFileName = self.downloadPATH + "/ReporteAuditoria.csv"
        
        y = self.fechaFin["year"]
        m = str(int(self.fechaFin["month"])+1)
        dIni = self.fechaIni["day"]
        dEnd = self.fechaFin["day"]
        t = self.today0.strftime("%Y%m%d")

        newFileName = self.downloadPATH + "/{}-{}-{}-{}_{}.csv".format(y,m,dIni,dEnd,t)
        
        os.rename(oldFileName,newFileName)
         

    def removingFiles(self):

        """Se hizo para: elminar los archivos con .crdownload y con el nombre default: 
        ReporteAuditoria.csv asi evitamos esperar a que se descarguen cosas viejas que ya no
          van a descargarse y renombrar cosas viejas que no se renombraron previamente"""
        
        partiallyDow = glob.glob(self.downloadPATH + "/*.crdownload")
        withoutName = glob.glob(self.downloadPATH + "/Reporte*.csv")
        for i in partiallyDow+withoutName:
            os.remove(i)
      
    def allFilesToDownload(self):

        """it requires fechas() to be run before it. it gives a list with the names of the files that
        should be download the day in which the code runs"""

        
        listFechasIn = self.listFechasIniPorMes #it is a list of dictionaries each with keys: year, month, day
        listFechasEn = self.listFechasFinPorMes #it is a list of dictionaries each with keys: year, month, day

        #print(listFechasIn)
        #print(listFechasEn)

        for i in range(0,len(listFechasIn)):
            fechaIn = listFechasIn[i]
            fechaEn = listFechasEn[i]
            y = fechaIn["year"]
            m = str(int(fechaIn["month"])+1)
            dIni = fechaIn["day"]
            dEnd = fechaEn["day"]
            t = self.today0.strftime("%Y%m%d")
            self.filesNames.append("{}-{}-{}-{}_{}.csv".format(y,m,dIni,dEnd,t))
            self.fileNamesPos.append(i) 
        


    def filesMissingToDownload(self):
        
        """it requires fechas() and allFilesToDownload() to run before it"""

        filesInFolder = os.listdir(self.downloadPATH)
        filesToBeInFolderKey = self.fileNamesPos
        filesToBeInFolderValue = self.filesNames
        
        self.missingFiles = [filesToBeInFolderKey[i] for i in range(0,len(filesToBeInFolderKey)) if filesToBeInFolderValue[i] not in filesInFolder]
        
 
    def deletingOldFiles(self):

        """it requires fechas() and allFilesToDownload() to run before it"""
 

        filesInFolder = os.listdir(self.downloadPATH)
        for i in range(0,len(filesInFolder)):
            if  filesInFolder[i] not in self.filesNames:
                os.remove(self.downloadPATH + "/" + filesInFolder[i])

    def mergingCsv(self):

        """it requires fechas() and allFilesToDownload() to run before it"""

        
        cvsList = []
        
        for f in sorted(self.filesNames):
            file = self.downloadPATH + "/" + f
            df = pd.read_csv(file, sep=";", encoding='latin-1',low_memory=False)
            #sprint(df.head())
            cvsList.append(df)
        
        csvMerged = pd.concat(cvsList, ignore_index= True)
        csvMerged.to_csv(self.downloadPATH + "/completoReporte.csv",index=False)


    #def secondPlane(self):
    # Finally, to make this in second plane without window
        #https://www.youtube.com/watch?v=a-O2K2VUFQg&list=PLas30d-GGNa2UW9-1H-NCNrUocvWD9cyh&index=24
    
    def run(self):
        
        #para verificar que se elimine los archivos que no se descargaron completamente o no se nombraron 
        self.removingFiles()

        # initialize the webdriver
        self.driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()), options=self.driverOptions)

        # setting the dates
        self.fechas()
        # making the list of the names of files to download
        self.allFilesToDownload()
        
        #revisar si hay descargas del mismo dia, de tal manera que:
        # si este codigo se corre varias veces el mismo día no se descarguen 
        # de nuevo las que ya se han logrado descargar
        self.filesMissingToDownload()    
        
        #si todos los nombres estan en el folder csv no se decarga nada mas
        if self.missingFiles == []:
            print("parece que ya se descargaron todos los reportes de hoy")
        
        # si hay nombres que faltan se decargan los archivos respectivos
        else:
            
            self.loginPage()
            self.navigatingNextPages()
            
            #for i in range(0,2): 
            for i in self.missingFiles:
                
                self.removingFiles()#remuevo lo que no se decargó completamente o lo que no se renombró

                self.fechaIni = self.listFechasIniPorMes[i]
                self.fechaFin = self.listFechasFinPorMes[i]

                #print(self.fechaIni)
                #print(self.fechaFin)

                self.autidoriasPageDescarga()

                

                self.verifyingDownload() #si se excede el maxTime el sigue con el sgt mes por eso se debe eliminar *.crdownload
                
                #para verificar que se elimine los archivos que no se descargaron completamente o no se nombraron 
                

                self.renamingFiles()
                self.removingFiles()
            

        self.filesMissingToDownload()#revisar que se hayan descargado todos los archivos que se querían
        if self.missingFiles == []:
            print("parece que ya se descargaron todos los reportes de hoy") 
            self.mergingCsv() 
            return 0
        else:
            print("faltan reportes por descargar, vuelve a iniciar el programa")
            return 1
        
        self.deletingOldFiles()
            

    #FINALMENTE PONERLO COMO PRUEBAS UNITARIAS
