import json
import datetime

from ANONYMLocation import ReportLocation

class ANONYMReport:
    
    def __init__(self,jsonfile=None):
        #Calling ANONYM location class
        self.locService = ReportLocation()
        
        #When and where incident occured
        self.dateofIncident=None
        self.timeofIncident=None
        self.locationofIncident=None

        #Details of crime
        self.suspectDescription=""
        self.crimeDescription=""

        #When the report was filed
        self.dateofReport=None
        self.timeofReport=None

        
        if(jsonfile!=None):
            self.readJson(jsonfile)
            
        
    def setJsonFile(self,jsonfile):
        self.readJson(jsonfile)

    def CheckDateTime(self):
    
        if(self.dateofIncident>self.dateofReport):
            Message = "ERROR!! Impossible the date of the crime is newer than the report"
            self.errorHandler(Message)
            
        if(self.dateofIncident==self.dateofReport and self.timeofReport<self.timeofIncident):
                Message ="ERROR!! Impossible, the time of the crime is newer than the time of the report"
                self.errorHandler(Message)

        
    def CheckLocation(self):
       #Address from API
        
       self.locService.setAddress(self.locationofIncident)
       reportedAddress = self.locService.getAddress()
       if(reportedAddress != self.locationofIncident):
           Message = "Warning is this the address: "+ reportedAddress
           self.errorHandler(Message)

       
    def readJson(self,jsonfile):
            
            file= open(jsonfile,)
            data = json.load(file)
            for i in data:
                if(i=="date_crime"):
                    date = data[i].replace("/"," ")
                    month = int(date[:2])
                    day = int(date[2:4])
                    year = int(date[-4:])
                    self.dateofIncident=datetime.date(year,month,day)
                elif(i=="time_crime"):
                    time= data[i].replace(":"," ")
                    hour=int(time[:2])
                    minute=int(time[3:5])
                    second=int(time[6:])
                    self.timeofIncident = datetime.time(hour,minute,second)
                elif(i=="crime_description"):
                    self.crimeDescription = data[i]
                elif(i=="suspect_desctiption"):
                    self.suspectDescription = data[i]
                elif(i=="date_report"):
                    date = data[i].replace("/"," ")
                    month = int(date[:2])
                    day = int(date[2:4])
                    year = int(date[-4:])
                    self.dateofReport=datetime.date(year,month,day)
                    
                elif(i=="time_report"):
                    time= data[i].replace(":"," ")
                    hour=int(time[:2])
                    minute=int(time[3:5])
                    second=int(time[6:])
                    self.timeofReport = datetime.time(hour,minute,second)
                elif(i=="location_crime"):
                    self.locationofIncident = data[i]
            file.close()

            #Checking logicality
            self.CheckDateTime()
            self.CheckLocation()
            
    def errorHandler(self,message):
        print(message)

def main():
    #Pass a json file ANONYM does time and location checks
    #AND PRints errors and warning
    JsonReport="report.json"

    
    newReport = ANONYMReport(JsonReport)
 
        

main()
