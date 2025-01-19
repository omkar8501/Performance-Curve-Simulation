# Constants
gas_const: float = 10.73159  # psia-ft3/R-lbmol
amw_air: float = 28.9647  # lb/lb-mol
water_den: float = 62.4  # lbm/ft3

# Length Conversion
in_to_ft: float = 1 / 12
ft_to_in: float = 1 / in_to_ft

m_to_ft: float = 3.2808399
ft_to_m: float = 1 / m_to_ft

# Volume Conversion
bbl_to_ft3: float = 5.6145833333333
ft3_to_bbl: float = 1 / bbl_to_ft3


# Temperature Conversion
def convert_temp(temp: float, from_unit: str, to_unit: str) -> float:
    """
        Convert temperature between Celsius, Fahrenheit, Kelvin, and Rankine

        Parameters:
        ----------
        temp : float
            The temperature to convert
        from_unit : str
            The current unit of the temperature ('C', 'F', 'K', 'R')
        to_unit : str
            The unit to convert the temperature to ('C', 'F', 'K', 'R')

        Returns:
        -------
        float
            Temperature in the desired unit

        Example:
        --------
        >>> convert_temp(temp=0, from_unit='C', to_unit='F')
        32.0
    """
    if from_unit == to_unit:
        return temp

    # Convert to Celsius
    to_celsius = {
        'C': lambda t: t,
        'F': lambda t: (t - 32) * 5 / 9,
        'K': lambda t: t - 273.15,
        'R': lambda t: (t - 491.67) * 5 / 9,
    }
    celsius = to_celsius[from_unit](temp)

    # Convert from Celsius to target unit
    from_celsius = {
        'C': lambda t: t,
        'F': lambda t: t * 9 / 5 + 32,
        'K': lambda t: t + 273.15,
        'R': lambda t: (t + 273.15) * 9 / 5,
    }
    return from_celsius[to_unit](celsius)
