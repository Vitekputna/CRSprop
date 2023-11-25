import os
import math
import yaml
import pkg_resources


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

    def __init__(self,specie : str) -> None:
        self.load(specie)

    def load(self,specie : str) -> None:

        path = os.path.join("data", specie, specie + ".yaml")
        stream = pkg_resources.resource_stream(__name__,path)
        data = yaml.safe_load(stream)

        self.data = data["data"]
        self.name = data["name"]

        #check for external data
        for property in self.data:    
            if self.data[property]["type"] == "external":

                filename = self.data[property]["data"]["path"]
                path = os.path.join("data", specie, filename)

                stream = pkg_resources.resource_stream(__name__,path)

                data = yaml.safe_load(stream)

                self.data[property]["data"] = data

class CRSprop:

    species = {}

    def __init__(self,names : list = []):

        for name in names:
            spec = specie(name)
            self.species[name] = spec
            
    def add_specie(self,name : str) -> None:
        spec = specie(name)
        self.species[name] = spec

    def list_species(self) -> None:
        for specie in self.species:
            print(specie)

    def density(self, specie : str, pressure : float, temperature : float) -> float:
        return self.value(specie,"density","value","pressure","temperature",pressure, temperature)
    
    def thermal_conductivity(self, specie : str, pressure : float, temperature : float) -> float:
        return self.value(specie,"thermalconductivity","value","pressure","temperature",pressure, temperature)
    
    def dynamic_viscosity(self, specie : str, pressure : float, temperature : float) -> float:
        return self.value(specie,"viscosity","value","pressure","temperature",pressure, temperature)
    
    def kinematic_viscosity(self, specie : str, pressure : float, temperature : float) -> float:
        return self.value(specie,"viscosity","value","pressure","temperature",pressure, temperature)
    
    def enthalpy(self, specie : str, pressure : float, temperature : float) -> float:
        return self.value(specie, "enthalpy","value","pressure","temperature",pressure, temperature)
    
    def saturated_pressure(self, specie : str, temperature : float) -> float:
        return self.interpolator_1D(specie,"saturated","pressure","temperature",temperature)
    
    def saturated_temperature(self, specie : str, pressure : float) -> float:
        return self.interpolator_1D(specie,"saturated","temperature","pressure",pressure)

    def vapor_enthalpy(self, specie : str, temperature : float) -> float:
        return self.interpolator_1D(specie,"saturated","vapor_enthalpy","temperature",temperature)
    
    def vapor_density(self, specie : str, temperature : float) -> float:
        return self.interpolator_1D(specie,"saturated","vapor_density","temperature",temperature)

    def liquid_enthalpy(self, specie : str, temperature : float) -> float:
        return self.interpolator_1D(specie,"saturated","liquid_enthalpy","temperature",temperature)
    
    def liquid_density(self, specie : str, temperature : float) -> float:
        return self.interpolator_1D(specie,"saturated","liquid_density","temperature",temperature)

    def value(self, specie : str, property : str, data_label : str, interp_array1 : str, interp_array2 : str,  value_1 : float, value_2 : float) -> float:

        data = self.species[specie].data[property]

        if data["type"] == "data" or data["type"] == "external":

            if data["dimension"] == 2:
                return self.interpolator_2D(specie,property,data_label,value_1,value_2)
            
            elif data["dimension"] == 1:
                return self.interpolator_1D(specie, property,data_label,interp_array1,value_1)
            
            else:
                print("Wrong data dimension")

        elif data["type"] == "polynomial5":
            return self.read_fit(data["data"],value_1,value_2)
        
        elif data["type"] == "constant":
            return data["data"]["value"]
        
        elif data["type"] == "antoine_equation":
            return self.read_antoine_equation(data["data"],value_1)
        
        else:
            print("Property type: " + data["type"] + " not recognized")

    def interpolator_1D(self, specie : str, property : str, data_label : str, interpolated_array : str, value : float) -> float:

        data = self.species[specie].data[property]["data"]

        interp_T,low_T,high_T = binary_search(value,data[interpolated_array])

        return (1-interp_T)*data[data_label][low_T] + interp_T*data[data_label][high_T]

    def read_phase(self,data : dict, pressure : float, temperature : float) -> str:
       
        interp,low_p,high_p = binary_search(pressure,data["pressure"])

        if interp > 0.5:
           P = high_p
        else:
           P = low_p

        interp,low_T,high_T = binary_search(temperature,data["temperature"][P])

        if interp > 0.5:
            T = high_T
        else:
            T = low_T

        return data["value"][P][T]

    def interpolator_2D(self,specie : str, property : str, data_label : str, pressure : float, temperature : float) -> float:

        data = self.species[specie].data[property]["data"]

        #check range
        if (pressure >= data["pressure"][0] and pressure <= data["pressure"][-1]) or pressure is None:
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

            low_value = (1-interp_T)*data[data_label][low_p][low_T] + interp_T*data[data_label][low_p][high_T]

            interp_T,low_T,high_T = binary_search(temperature,data["temperature"][high_p])

            high_value = (1-interp_T)*data[data_label][high_p][low_T] + interp_T*data[data_label][high_p][high_T]

        #single temp data
        else:
            interp_T,low_T,high_T = binary_search(temperature,data["temperature"])

            low_value = (1-interp_T)*data[data_label][low_p][low_T] + interp_T*data[data_label][low_p][high_T]

            interp_T,low_T,high_T = binary_search(temperature,data["temperature"])

            high_value = (1-interp_T)*data[data_label][high_p][low_T] + interp_T*data[data_label][high_p][high_T]

        #interpolate values
        return (1-interp_p)*low_value + interp_p*high_value

    def read_fit(self,data : dict, pressure : float, temperature : float) -> float:

        interp,low_p,high_p = binary_search(pressure,data["pressure"])

        low_value = polynomial5(temperature,data["value"][low_p])
        high_value = polynomial5(temperature,data["value"][high_p])

        return (1-interp)*low_value + interp*high_value

    def read_antoine_equation(self, data : dict, temperature: float) -> float:
        A = data["A"]
        B = data["B"]
        C = data["C"]

        return 10**(A-B/(temperature+C))

