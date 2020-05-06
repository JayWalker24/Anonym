import json
import datetime
import boto3
from ANONYMLocation import ReportLocation
import os
import TestDuplicates as TD

class ANONYMReport:
    
    def __init__(self,jsonfile=None):
        self.title = jsonfile
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
        

        self.DateError=""
        self.TimeError=""

        
        if(jsonfile!=None):
            self.readJson(jsonfile)
            self.checkLogic()

            self.json_Assess()
            
    def json_Assess(self):
        if(self.DateError!=""):
            print(self.DataError)
            with open(self.title) as outfile:
                data = json.load(outfile)
                data["date_crime"] +=self.DateError
            with open(self.title, "w") as f:
                json.dump(data,f)

                
        if(self.TimeError!=""):
            print(self.TimeError)
            with open(self.title) as outfile:
                data = json.load(outfile)
                data["time_crime"]+=self.TimeError
            with open(self.title, "w") as f:
                json.dump(data,f)

                
    def setJsonFile(self,jsonfile):
        self.readJson(jsonfile)
        self.checkLogic()
        self.json_Assess()

    
    def CheckDateTime(self):
    
        if(self.dateofIncident>self.dateofReport):
            Message = "  The crime is newer than the report"
            self.DateError+=Message
            self.errorHandler(Message)
        print(self.dateofIncident, self.dateofReport)
        if(self.dateofIncident==self.dateofReport and self.timeofReport<self.timeofIncident):
                Message ="  Time of the crime is newer than the time of the report"
                self.TimeError+=Message
                self.errorHandler(Message)
                
    def checkLogic(self):
            #Checking logicality
            self.CheckDateTime()
            self.CheckLocation()
            #self.isDuplicate()
        
    def CheckLocation(self):
       #Address from API
        
       self.locService.setAddress(self.locationofIncident)
       reportedAddress = self.locService.getAddress()
       if(reportedAddress != self.locationofIncident):
           Message = "Warning is this the address: "+ reportedAddress
           #self.errorHandler(Message)

    def NormalizeLocation(self,DB_location):
        rdistance = TD.Noself.locService.DistanceFrom(DB_location)
        adjustedLoc = float(1 - (rdistance/1000))
        LocationGrade =0
        if(adjustedLoc<0):
            LocationGrade = 0
        else:
            LocationGrade = adjustedLoc
        return LocationGrade/2
         
    def isDuplicate(self):
        jsonlst = []
        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket("anonym-json-bucket")
        for s3obj in my_bucket.objects.all():
            filename = s3obj.key
            my_bucket.download_file(s3obj.key, filename)
            jsonlst.append(filename)

        for i in jsonlst:
            message=""
            DB_location, DB_time, DB_description = TD.readJson(i)
            TextGrade = TD.TextGrader((self.crimeDescription+" "+self.suspectDescription), DB_description)
            LocationGrade = self.NormalizeLocation(DB_location)
            if(TextGrade+LocationGrade>0.80):
                message = "A Likely Duplicate"
                self.errorHandler(message)

            
    def timeHandler(self,time):
     
        colon = time.index(":")
        hr = int(time[:colon])
        minutes =int(time[colon+1:colon+3])
        
        if("PM" in time or "pm" in time):
            hr = (hr+12)%24
        return datetime.time(hr,minutes)

    def dateHandler(self,date):
        date = date.replace("/"," ")
        div = date.index(" ")
        month = int(date[:div])
        day = int(date[div+1:div+3])
        year = int(date[-4:])
      
        return datetime.date(year,month,day)
    
    def readJson(self,jsonfile):
            print("aedsg", jsonfile)

    def readJson(self,jsonfile):
            file= open(jsonfile,)
            data = json.load(file)
            for i in data:
                if(i=="date_crime"):
                    self.dateofIncident=self.dateHandler(data[i])
                elif(i=="time_crime"):
                    self.timeofIncident = self.timeHandler(data[i])
                elif(i=="crime_description"):
                    self.crimeDescription = data[i]
                elif(i=="suspect_description"):
                    self.suspectDescription = data[i]
                elif(i=="date_report"):
                    self.dateofReport=self.dateHandler(data[i])           
                elif(i=="time_report"):
                    self.timeofReport = self.timeHandler(data[i])
                elif(i=="location_crime"):
                    self.locationofIncident = data[i]

            file.close()

            
            
    def errorHandler(self,message):
        print(message)

 
