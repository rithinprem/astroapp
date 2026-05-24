import math
import dashaflow
import json
from app.calculators.constants import NAKSHATRA_NAMES


class chart_class:
    def __init__(self, birth_data):
        self.birth_data = birth_data
        self.d1 = self.d1_chart_engine(**birth_data)

    def d1_chart_engine(self, **birth_data):
        """
        Calculate the D1 chart based on the provided D1 chart data.
        
        Parameters:
        birth_data (dict): A dictionary containing the D1 chart data with keys as planet names and values as their positions in degrees.
        
        Returns:
        dict: A dictionary containing the calculated D1 chart with planet names as keys and their corresponding Nakshatra names as values.
        """
        chart = dashaflow.cast_chart(**birth_data)
        d1_chart_dict = dict()

        #View the D1 (Birth Chart) Planetary Positions
        for planet, details in chart["planets"].items():        
            d1_chart_dict[planet] = {"Sign": details['sign'], "Degree": details['degree'],"House":details['house'],"Nakshatra":details['nakshatra'],"Pada":details['pada'],"Nakshatra_lord":details['nakshatra_lord'],"Retrograde":details['is_retrograde'],"Combust":details['is_combust']}


        return d1_chart_dict

