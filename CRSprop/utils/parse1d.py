import sys
import yaml

path = sys.argv[1]

print(path)

with open(path) as file:
    lines = file.readlines()

parsed_lines = []

for line in lines:
    parsed_line = [float(x) for x in line.split()[:-1]]
    parsed_lines.append(parsed_line)

names = ["temperature","pressure","density","Volume","internal_energy","enthalpy","entropy","Cv","Cp","sound_speed","joule_thompson","viscosity","thermal_conductivity","surface_tension"]

output = {}

for i in range(len(names)):
    vector = []
    for line in parsed_lines:
        vector.append(line[i])

    output[names[i]] = vector

export_path = path.replace(".txt",".yaml")

with open(export_path,'w') as file:
    yaml.dump(output,file,default_flow_style=False, line_break= True, width = 5)