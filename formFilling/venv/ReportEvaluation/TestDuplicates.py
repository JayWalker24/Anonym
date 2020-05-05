# Look at reports that were submitted in the lsat 10 mins
# Look at location and distance from a max of 25 miles
# Look at the words (only input) and how much are more than the average
 
import io
import json
 

 

def readJson(jsonfile):
    file = open(jsonfile,)
    data = json.load(file)
    location = data["location_crime"]
    time = data["time_crime"]
    description = data["crime_description"] +" "+data["suspect_description"]
    return location,time, description
    

def readWords(ReportText):
    Words =[]
    newstr=""
    for i in range(len(ReportText)):
        if(ord(ReportText[i])==32):
            Words.append(newstr.replace("\n",""))
            newstr=""
        if(i==len(ReportText)-1):
            newstr+=ReportText[i]
            Words.append(newstr)
        else:
            newstr+=ReportText[i]
 
    return Words
    
def NormalizeLocation(rdistance):
        adjustedLoc = float(1 - (rdistance/1000))
        LocationGrade =0
        if(adjustedLoc<0):
            LocationGrade = 0
        else:
            LocationGrade = adjustedLoc
        return LocationGrade/2

 
        
def TextGrader(newReportText,oldReportText):

    newReportWords = readWords(newReportText)
    oldReportWords = readWords(oldReportText)
 
    longestReport = max(len(newReportWords),len(oldReportWords))
    wordgrade = (len(set(newReportWords).intersection(oldReportWords))/longestReport/2)
    
    return wordgrade


 
 
