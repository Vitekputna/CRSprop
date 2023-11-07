from CRSprop import CRSprop
spec = "N2O"

prop = CRSprop([spec])

print(prop.density(spec,1,300))

print(prop.saturated_pressure(spec,300))
print(prop.saturated_temperature(spec,5.8878))
print(prop.vapor_enthalpy(spec,prop.saturated_temperature(spec,0.1)))
print(prop.liquid_enthalpy(spec,prop.saturated_temperature(spec,0.1)))
