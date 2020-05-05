"""
To use class add:

    from anonymLocation import ReportLocation
    
Validates Reads and  Stores Location data

Able to read the information a user entered and passed to GMapsAPI to be deconstructed 
"""
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key = "#######")


class ReportLocation:
    def __init__(self,reported_address=None):
        #misc handles additional information that was provided like parks, points of location, names of places
        self.misc=''
        self.streetnumber=''
        self.street=""
        self.neighborhood=""
        self.city=""
        self.state=""
        self.postalCode=""
        self.country=""

        self.compilation=[self.misc,self.streetnumber,self.street,self.neighborhood,
                         self.city,self.state,self.postalCode,self.country]
        #The full address as should be entered on to form
        self.fullAddress=""

        self.undefined=""
        if(reported_address!=None):
            self.undefined=reported_address
            self.gMapsreader(reported_address)

    def setAddress(self,reported_address):
        self.gMapsreader(reported_address)
        
    def gMapsreader(self,reported_address):
        encodedAddress = gmaps.geocode(reported_address)[0]["address_components"]

        if(len(set(encodedAddress[0]['types']).intersection({"colloquial_area","","establishment","point_of_interest"}))!=0):
                self.setMisc(encodedAddress[0]["long_name"])

        correctSt=True
        for i in range(len(encodedAddress)):
          #  print(encodedAddress[i])
           # print(encodedAddress[i]['types'])
            if(encodedAddress[i]['types'][0]=="street_number"):
                self.setStreetNumber(encodedAddress[i]["long_name"])

            if(encodedAddress[i]['types'][0]=="route"):
                self.setStreetAddress(encodedAddress[i]["long_name"])
                
            if(encodedAddress[i]['types'][0]=="neighborhood"):
                self.setNeighborhood(encodedAddress[i]['long_name'])
                
            if(encodedAddress[i]['types'][0]=="locality" or encodedAddress[i]['types'][0]=="political"):
                self.setCity(encodedAddress[i]["long_name"])
                
            if(encodedAddress[i]['types'][0]=="administrative_area_level_1"):
                self.setState(encodedAddress[i]["long_name"])
                
            if(encodedAddress[i]['types'][0]=="postal_code"):
                self.setPostalCode(encodedAddress[i]["long_name"])
        self.setFullAddress()
 
    def DistanceFrom(self, otherAddress):
        fullDistance = gmaps.distance_matrix(self.fullAddress,otherAddress)['rows'][0]['elements'][0]['distance']['text'].replace(",","")
        Distance = 0
        if("km" in fullDistance):
            Distance = float(fullDistance[:-2])*1000
        else:
            Distance = float(fullDistance[:-2])
        return Distance
        
    def setMisc(self, reportedMisc):
        self.misc = reportedMisc+ " "
    def setStreetNumber(self,reportedStrNum):
        self.streetnumber = reportedStrNum+ " "
        
    def setStreetAddress(self,reportedStr): 
        self.street=reportedStr + " "

    def setNeighborhood(self,reportedNeigh):
        self.neighborhood = reportedNeigh+ " "
       
    def setCity(self,reportedCity):
        self.city=reportedCity+ " "
        
    def setState(self,reportedState):
        self.state=reportedState+ " "

    def setPostalCode(self,reportedPS):
        self.postalCode= reportedPS+ " "
        
    def setFullAddress(self):
        if(self.street=="" and self.neighborhood==""):
            self.street=self.undefined+" "
        if(self.misc==self.street):
            self.street=""
        if(self.street!=""):
            self.neighborhood=""
        self.fullAddress = str(self.misc+ self.streetnumber+ self.street+self.neighborhood
                               +", "+self.city+","+ self.state+
                                ", "+ self.postalCode + self.country)
        
    #Returns the full address
    def getAddress(self):
        return self.fullAddress
 
