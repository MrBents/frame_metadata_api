import pickle
from geopy.geocoders import GoogleV3
import json
import os
from config import *
import math


class VroomPayloadBuilder():

    def __init__(self):
        self.vehicles = []
        self.jobs = []
        self.with_addr = False
        self.location_manager = LocationManager()
        self.addVehicles("whatever")

    # TODO: Implement this.
    def addVehicles(self, some_config):
        self.vehicles.append(
            {"id": 0, "start": [-80.1602584,25.9699994], "end": [-80.1602582,25.9699994]})
        self.vehicles.append(
            {"id": 1, "start": [-80.1602584,25.9699994], "end": [-80.1602582,25.9699994]})
        self.vehicles.append(
            {"id": 2, "start": [-80.1602584,25.9699994], "end": [-80.1602582,25.9699994]})
    
    def __populateVehicleCapacity(self):
        C = math.ceil(1.2 * len(self.jobs) / len(self.vehicles))
        for i in range(len(self.vehicles)):
            temp = self.vehicles[i]
            temp["capacity"] = [C]
            self.vehicles[i] =  temp

    # TODO: Implement this.
    def toJson(self):
        self.__populateVehicleCapacity()
        tmp = self.__dict__.copy()
        tmp.pop("location_manager", None)
        tmp.pop("with_addr", None)
        return json.dumps(tmp)

    # TODO: Implement this.
    def toDict(self, with_addr=False):
        self.__populateVehicleCapacity()
        tmp = self.__dict__.copy()
        tmp.pop("location_manager", None)
        tmp.pop("with_addr", None)
        return tmp

    # TODO: Implement this.
    def fromJson(self):
        pass

    def fromRowList(self, row_list):
        for row in row_list:
            self.parseJob(row)
        return self

    def persistResult(self):
        with open(os.path.join(base_path, 'output/output.json'), 'w') as f:
            json.dump(self.toDict(), f)
        return self

    def parseJob(self, sql_row):
        location = self.location_manager.getLocation(sql_row)

        if location != None:
            if not self.with_addr:
                self.jobs.append(
                    {"id": len(self.jobs), "location": location.coordinates, "delivery": [1]})
            else:
                self.jobs.append(
                    {"id": len(self.jobs), "location": location.coordinates, "delivery": [1], "description": location.geo_location.address})
        # TODO: Create limitation parser object.
        # TODO: Add limitation to jobs

    def withAddr(self):
        self.with_addr = True
        return self


class LocationManager():

    def __init__(self):
        self.geolocator = GoogleV3(os.environ['API_KEY'])
        try:
            with open(os.path.join(base_path, "cache/cache.pickle"), "rb") as f:
                self.cache = pickle.load(f)
        except:
            self.cache = {}

        try:
            with open(os.path.join(base_path, "cache/coords_to_address_cache.pickle"), "rb") as f:
                self.coords_to_address_cache = pickle.load(f)
        except:
            self.coords_to_address_cache = {}

    def getLocation(self, sql_result):


        k = list(sql_result.keys())

        # KeySpace:
        # ['S_No', 'Sales_Order_No', 'Customer', 'Sales_Order_Date', 
        # 'Billing_Address_Line_1', 'Billing_Address_Line_2', 'Billing_Address_Line_3',
        # 'Billing_Address_City', 'Billing_Address_State', 'Billing_Address_Postal_Code',
        # 'Ship_Date', 'Sales_Rep']
        address_keys = ['Billing_Address_Line_2', 'Billing_Address_Line_3', 'Billing_Address_City', 'Billing_Address_State', 'Billing_Address_Postal_Code']        

        address_fields = [sql_result[k]
                          for k in address_keys if sql_result[k] != None]

        parsed_address = ', '.join(address_fields)

        if parsed_address in self.cache:
            self.coords_to_address_cache[','.join(str(loc) for loc in self.cache[parsed_address].coordinates)] = self.cache[parsed_address].geo_location.address
            self.persist_updated_cache()
            return self.cache[parsed_address]

        if parsed_address == "":
            return None

        geo_location = self.geolocator.geocode(parsed_address)

        if geo_location == None:
            # TODO: throw some exception
            print("Fuck. ")
            return None

        new_location = Location(sql_result, geo_location)
        self.cache[parsed_address] = new_location
        self.coords_to_address_cache[','.join(str(loc) for loc in new_location.coordinates)] = new_location.geo_location.address
        self.persist_updated_cache()
        return self.cache[parsed_address]

    def persist_updated_cache(self):
        with open(os.path.join(base_path, "cache/cache.pickle"), "wb") as f:
            pickle.dump(self.cache, f)
        with open(os.path.join(base_path, "cache/coords_to_address_cache.pickle"), "wb") as f:
            pickle.dump(self.coords_to_address_cache, f)


class Location():
    def __init__(self, row, geo_location):
        self.row = row
        self.latitude = geo_location.latitude
        self.longitude = geo_location.longitude
        self.coordinates = [self.longitude, self.latitude]
        self.geo_location = geo_location
