from CRSprop import CRSprop
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

spec = "N2O"

def mass_flow(P0,P2,T0,d,print_table=False):

    def func2(X,*args):
        Y = X[0]
        P1 = X[1]

        Yl = Y
        Yg = 1-Y

        h0,T0,P2,T2 = args
        T1 = T0

        # rho1 = prop.density(spec,P1/1e6,T1)
        # h1 = prop.enthalpy(spec,P1/1e6,T1)*1e3

        T1 = prop.saturated_temperature(spec,P1/1e6)
        rho1 = prop.liquid_density(spec,T1)
        h1 = prop.liquid_enthalpy(spec,T1)*1e3
        
        rho2_l = prop.liquid_density(spec,T2)
        rho2_g = prop.vapor_density(spec,T2)
        h2_l = prop.liquid_enthalpy(spec,T2)*1e3
        h2_g = prop.vapor_enthalpy(spec,T2)*1e3

        rho2 = Yl*rho2_l+Yg*rho2_g
        h2 = Yl*h2_l+Yg*h2_g

        c2_2 = (P2-P1)/(rho2*(rho2/rho1-1))
        c1_2 = ((rho2/rho1)**2)*c2_2

        return [h0-h1-0.5*c1_2,h1+0.5*c1_2-h2-0.5*c2_2]

    prop = CRSprop([spec])

    # P0 = 8e6
    # T0 = 300
    # T1 = T0
    # P2 = 2.5e6

    # d = 1e-3
    A = np.pi*(d/2)**2

    T2 = prop.saturated_temperature(spec,P2/1e6)

    h0 = prop.enthalpy(spec,P0/1e6,T0)*1e3

    args = (h0,T0,P2,T2)
    root = fsolve(func2,[0.3,5e6],args)
    # print(root)
    Y_l = min(1,root[0])
    P1 = root[1]
    Y_g = 1-Y_l

    # rho1 = prop.density(spec,P1/1e6,T1)
    # h1 = prop.enthalpy(spec,P1/1e6,T1)*1e3
    T1 = prop.saturated_temperature(spec,P1/1e6)

    rho1 = prop.liquid_density(spec,T1)
    h1 = prop.liquid_enthalpy(spec,T1)*1e3

    rho2_l = prop.liquid_density(spec,T2)
    rho2_g = prop.vapor_density(spec,T2)
    h2_l = prop.liquid_enthalpy(spec,T2)*1e3
    h2_g = prop.vapor_enthalpy(spec,T2)*1e3

    rho2 = Y_l*rho2_l+Y_g*rho2_g
    h2 = Y_l*h2_l+Y_g*h2_g
   
    c2_2 = (P2-P1)/(rho2*(rho2/rho1-1))
    c1_2 = ((rho2/rho1)**2)*c2_2
   
    h2 = Y_l*h2_l + Y_g*h2_g
    rho2 = Y_l*rho2_l + Y_g*rho2_g

    res_e0 = h0-(h1+0.5*c1_2)
    res_e = h1+0.5*c1_2 - h2 - 0.5*c2_2
    res_h = rho1*c1_2 + P1 - (rho2*c2_2+P2)
    res_m = rho1*np.sqrt(c1_2)-rho2*np.sqrt(c2_2)
   
    md_HEM = A*rho2*np.sqrt(2*(h0-h2))
    md_ICO = A*np.sqrt(2*rho1*(P0-P2))
    Pv = prop.saturated_pressure(spec,T0)
    kappa = np.sqrt((P0-P2)/(Pv*1e6-P2))
    a = 1-1/(1+kappa)
    b = 1/(1+kappa)

    mass_flux = a*md_ICO+b*md_HEM

    if print_table:
        print("Outlet vapor fraction:\t",Y_g)
        print("Outlet liquid fraction:\t",Y_l)
        print()

        print("Outlet temperature [K]:\t",T2)
        print("Orifice inlet temp [K]:\t",T1)
        print()

        print("Total pressure [Pa]:\t",P0)
        print("Inlet pressure [Pa]:\t",P1)
        print("Outlet pressure [Pa]:\t",P2)
        print()

        print("Outlet density [kg/m3]:\t", rho2)
        print("Inlet density [kg/m3]:\t", rho1)
        print()

        print("Outlet velocity [m/s]:\t",np.sqrt(c2_2))
        print("Inlet velocity [m/s]:\t",np.sqrt(c1_2))
        print()

        print("Energy eq. 0=>1 res:\t",res_e0)
        print("Energy eq. 1=>2 res:\t",res_e)
        print("Momentum eq. res:\t",res_h)
        print("Mass consrv. eq. res:\t",res_m)
        print()

        print("Incompressible model:\t",md_ICO)
        print("HEM model:\t\t", md_HEM)
        print("NHNE model:\t\t",mass_flux)

    return mass_flux

mass_flow(8e6,2.5e6,300,1e-3,print_table=True)

# p2 = np.linspace(0.1e6,4e6,12)

# md = []
# for p in p2:
#     md.append(mass_flow(8e6,p,300,1e-3))

# plt.plot(p2,md)
# plt.show()

