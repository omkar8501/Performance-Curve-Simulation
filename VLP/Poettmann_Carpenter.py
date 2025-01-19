import numpy as np
import pandas as pd
from Misc_Correlations import Constants
from typing import Optional, List


def poettmann_carpenter(oil_rate: float, gor_st: float, water_cut: float, pvt_table: pd.DataFrame, thp: float,
                        tht: float, tbg_id: float, tbg_shoe: float, num_iter: int,
                        sg_water: Optional[float] = 1.0) -> pd.DataFrame:
    """
        Calculates the flowing bottomhole pressure in a string at a given set of conditions.

        Poettmann and Carpenter Correlation is a simplified three-phase flow model to compute pressure losses in
        wellbores by estimating mixture density and friciton factor

        Parameters:
        ----------
        oil_rate : float
            Rate of produced oil at surface in standard conditions (stb/day)
        gor_st : float
            Ratio of produced gas to oil at standard conditions (scf/stb)
        water_cut : float
            Fraction of produced water in the total liquid at standard conditions
        pvt_table : pd.DataFrame
            PVT Table consisting of fluid properties like FVF, Viscosity, Density, etc at reservoir temperature
        thp : float
            Wellhead pressure in psia
        tht : float
            Wellhead temperature of the fluid in degC
        tbg_id : float
            Inside diameter of the tubing string in inches (in)
        tbg_shoe : float
            Length of the tubing string in meters (m)
        num_iter : int
            Number of iterations to be done
        sg_water : optional, float
            Specific gravity of the produced water, default value is 1

        Returns:
        -------
        pd.DataFrame
            Returns the pressure traverse for the given set of conditions

        Notes:
        ------
        - No Slip condition of liquid phase is assumed
        - Valid only for vertical strings of sizes between 2" and 3"
        - Valid for artes greater than 400 bopd, GLR under 1500 scf/stb and viscosity under 5 cp
        - Effect of acceleration is neglected

        Example:
        --------
        >>>

    """

    # Discretize the tubing into small elements and create an empty dataframe to store the pressure traverse
    depth_arr: np.ndarray = np.linspace(0, tbg_shoe, num_iter + 1)
    pressure_trav: pd.DataFrame = pd.DataFrame(depth_arr, columns=['Depth'])
    pressure_arr: List[float] = [thp]  # Empty list to store all the pressures with THP as the first element

    # Convert the tubing length from meter to feet and  id from inches to feet
    tbg_shoe *= Constants.m_to_ft
    tbg_id *= Constants.in_to_ft

    # Convert the wellhead temperature from degC to degR
    tht = Constants.convert_temp(tht, 'C', 'R')

    # Calculate the WOR and store it in a new variable
    wor: float = water_cut / (1 - water_cut)
    gor: float = gor_st

    # Height of the discrete tubing element in meters
    del_h: float = tbg_shoe / num_iter

    pressure: float = thp  # Initial pressure

    # Iterate over each element and compute the pressure gradient
    for i in range(num_iter):
        # PVT properties at the current pressure
        pressure_round: float = float(round(pressure))
        print(pressure_round)
        oil_den: float = pvt_table.loc[pvt_table['Pressure'] == pressure_round, 'Oil Density'].iloc[0]  # lbm/ft3
        water_den: float = Constants.water_den * sg_water  # lbm/ft3
        gas_den: float = pvt_table.loc[pvt_table['Pressure'] == pressure_round, 'Gas Density'].iloc[0]  # lbm/ft3
        gas_sol: float = pvt_table.loc[pvt_table['Pressure'] == pressure_round, 'Gas Solubility'].iloc[0]  # scf/stb
        gas_comp_factor: float = \
            pvt_table.loc[pvt_table['Pressure'] == pressure_round, 'Gas Compressibility Factor'].iloc[0]
        oil_fvf: float = pvt_table.loc[pvt_table['Pressure'] == pressure_round, 'Oil FVF'].iloc[0]  # rb/stb

        # Mass and Volume associated with one barrel oil for ith element
        mass_i: float = Constants.bbl_to_ft3 * (oil_den + wor * water_den) + gor * gas_den
        volume_i: float = Constants.bbl_to_ft3 * (oil_fvf + wor) + (gor - gas_sol) * (14.7 / pressure) * (
                tht / 520) * gas_comp_factor
        # Average density of ith element
        density_i: float = mass_i / volume_i

        # Calculate friction factor
        d_rho_v: float = 1.4737 * np.power(10.0, -5.0) * mass_i * oil_rate / tbg_id
        friction_fact: float = np.power(10.0, 1.444 - 2.5 * np.log10(d_rho_v))

        # Average K-factor
        k_fact: float = friction_fact * np.square(oil_rate) * np.square(mass_i) / (
                7.7137 * np.power(10.0, 10.0) * np.power(tbg_id, 5))

        # Pressure gradient in psia/ft
        pressure_grad: float = (density_i + k_fact / density_i) / 144

        # Drop in pressure over delta h
        del_p: float = pressure_grad * del_h

        # Increase the pressure for the next iteration and add it to the traverse array
        pressure += del_p
        pressure_arr.append(pressure)

    pressure_trav['Pressure'] = pressure_arr

    return pressure_trav
