import sys
import yaml

path = sys.argv[1]

print(path)

with open(path) as file:
    lines = file.readlines()

parsed_lines = []

for line in lines:
    parsed_line = [float(x) for x in line.split()[:-1]]
    parsed_lines.append([parsed_line[1],parsed_line[0],parsed_line[-1]])

sorted_parsed_lines = sorted(parsed_lines,key=lambda x: x[0])

unique_pres = set([sorted_parsed_lines[i][0] for i in range(len(sorted_parsed_lines))])

unique_pres = sorted(unique_pres)

pres_dict = {}

for item in sorted_parsed_lines:

    if item[0] not in pres_dict.keys():
        pres_dict[item[0]]  =  [[item[1],item[2]]]
    else:
        pres_dict[item[0]].append([item[1],item[2]])

for key in pres_dict:
    pres_dict[key] = sorted(pres_dict[key],key=lambda x: x[0])
    
# print(pres_dict)

count = 0
last_count = 0

multiple_temp = False

for key in pres_dict:
    count = 0

    for item in pres_dict[key]:
        count += 1

    if count != last_count and last_count != 0:
        multiple_temp = True
        print("diferent temp value counts")

    last_count = count

names = ["pressure","temperature","value"]

export_data = {}

export_data["pressure"] = unique_pres
export_data["temperature"] = []
export_data["value"] = []

if multiple_temp == True:

    for key in pres_dict:

        temp_list = []

        for item in pres_dict[key]:
            temp_list.append(item[0])

        # print(temp_list)
        export_data["temperature"].append(temp_list)

else: 
    temp_list = []

    for item in pres_dict[key]:
        temp_list.append(item[0])

    # print(temp_list)
    export_data["temperature"] = temp_list

for key in pres_dict:

    val_list = []

    for item in pres_dict[key]:
        val_list.append(item[1])

    # print(val_list)
    export_data["value"].append(val_list)

export_path = path.replace(".txt",".yaml")

# print(export_data)

with open(export_path,'w') as file:
    yaml.dump(export_data,file,default_flow_style=False, line_break= True, width = 5)
