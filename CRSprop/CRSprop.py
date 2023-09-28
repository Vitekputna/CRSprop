import os
import math
import yaml

import pkg_resources
from importlib  import resources
import io


def binary_search(value : float, array : list):

    right = len(array)
    left = 0
    width = right-left
    midpoint = math.ceil(width/2 + left)

    counter = 0
    
    while width > 1 and counter < 10:
        if value > array[midpoint]:
            left = midpoint
            width = right-left
            midpoint = math.ceil(width/2 + left)

        else:
            right = midpoint
            width = right-left
            midpoint = math.ceil(width/2 + left)

        counter += 1

    #interpolate
    return (value-array[left])/(array[right]-array[left]),left,right

def polynomial5(value : float, parameters : list):
    return parameters[0]/value + parameters[1] + parameters[2]*value + parameters[3]*value**2+ parameters[4]*value**3 + parameters[5]*value**4 + parameters[6]*value**5

class specie:

    name = ""
    data = {}

    def __init__(self) -> None:
        pass

    def __init__(self,specie : str) -> None:
        self.load(specie)

    def load(self,specie : str) -> None:

        path = os.path.join("data", specie, specie + ".yaml")
        stream = pkg_resources.resource_stream(__name__,path)
        # path = specie + ".yaml"

        # with resources.open_binary('CRSprop',path) as fp:
        #     data = fp.read()

        # data = yaml.safe_load(io.BytesIO(data))

        data = yaml.safe_load(stream)

        # with open(path,'r') as file:
        #     data = yaml.safe_load(file)

        self.data = data["data"]
        self.name = data["name"]

        #check for external data
        for property in self.data:    
            if self.data[property]["type"] == "external":

                filename = self.data[property]["data"]["path"]
                # path = os.path.join(os.path.curdir, "data", specie, filename)
                path = os.path.join("data", specie, filename)

                # with resources.open_text('CRSprop',path) as fp:
                #     data = fp.read()

                stream = pkg_resources.resource_stream(__name__,path)

                data = yaml.safe_load(stream)

                # with open(path,'r') as file:
                #     data = yaml.safe_load(file)

                self.data[property]["data"] = data

class CRSprop:

    species = {}

    def __init__(self,names : list):

        for name in names:
            spec = specie(name)
            self.species[name] = spec

    def list_species(self):
        for specie in self.species:
            print(specie)

    def density(self, specie : str, pressure : float, temperature : float) -> float:
        return self.value(specie,"density",pressure, temperature)
    
    def thermal_conductivity(self, specie : str, pressure : float, temperature : float) -> float:
        return self.value(specie,"thermalconductivity",pressure, temperature)
    
    def dynamic_viscosity(self, specie : str, pressure : float, temperature : float) -> float:
        return self.value(specie,"viscosity",pressure, temperature)
    
    def kinematic_viscosity(self, specie : str, pressure : float, temperature : float) -> float:
        return self.value(specie,"viscosity",pressure, temperature)

    def value(self, specie : str, property : str, pressure : float, temperature : float) -> float:

        data = self.species[specie].data[property]

        if data["type"] == "data" or data["type"] == "external":
            return self.read_data(data["data"],pressure,temperature)

        elif data["type"] == "polynomial5":
            return self.read_fit(data["data"],pressure,temperature)

    def read_data(self,data : dict, pressure : float, temperature : float) -> float:
        #check range
        if pressure >= data["pressure"][0] and pressure <= data["pressure"][-1]:
            pass
        else: 
            print("pressure out of range")
            exit()

        #interpolate pressure
        interp_p,low_p,high_p = binary_search(pressure,data["pressure"])

        #interpolate temperature
        #multiple temp data
        if len(data["pressure"]) == len(data["temperature"]):
            interp_T,low_T,high_T = binary_search(temperature,data["temperature"][low_p])

            low_value = (1-interp_T)*data["value"][low_p][low_T] + interp_T*data["value"][low_p][high_T]

            interp_T,low_T,high_T = binary_search(temperature,data["temperature"][high_p])

            high_value = (1-interp_T)*data["value"][high_p][low_T] + interp_T*data["value"][high_p][high_T]

        #single temp data
        else:
            interp_T,low_T,high_T = binary_search(temperature,data["temperature"])

            low_value = (1-interp_T)*data["value"][low_p][low_T] + interp_T*data["value"][low_p][high_T]

            interp_T,low_T,high_T = binary_search(temperature,data["temperature"])

            high_value = (1-interp_T)*data["value"][high_p][low_T] + interp_T*data["value"][high_p][high_T]

        #interpolate values
        return (1-interp_p)*low_value + interp_p*high_value

    def read_fit(self,data : dict, pressure : float, temperature : float) -> float:

        interp,low_p,high_p = binary_search(pressure,data["pressure"])

        low_value = polynomial5(temperature,data["value"][low_p])
        high_value = polynomial5(temperature,data["value"][high_p])

        return (1-interp)*low_value + interp*high_value

    

