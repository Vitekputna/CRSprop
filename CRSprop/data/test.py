from CRSprop import CRSprop

spec = "N2O"
p = 1
T = 300

props = CRSprop([spec])
print(props.density(spec,1,300))
print(props.enthalpy(spec,1,300))
print(props.dynamic_viscosity(spec,1,300))
print(props.thermal_conductivity(spec,1,300))
print(props.vapor_pressure(spec,300))
print(props.saturated_temperature(spec,5.8878))

# print(props.species[spec].data["density"])
