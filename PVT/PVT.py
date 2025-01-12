import Fluid
import Gas_Solubility as gas_sol
import Oil_Formation_Volume_Factor as Oil_FVF

if __name__ == '__main__':
    oil = Fluid.Fluid(0.84, 0.7)

    Rs = gas_sol.standings_gas_solubility(1000, 70, 37, 0.7)
    Bo = Oil_FVF.standings_oil_fvf(Rs, 70, 37, 0.7)
    print(Bo)
