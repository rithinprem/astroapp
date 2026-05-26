import math
import dashaflow
import json
from app.calculators.constants import NAKSHATRA_NAMES, RASHI_NUMBER, RASHI_NAMES, NAKSHATRA_LORDS


class chart_class:
    def __init__(self, birth_data):
        self.birth_data = birth_data
        self.birth_info = self.birth_info(self.birth_data)
       

    def birth_info(self,birth_data):
      chart = dashaflow.cast_chart(**birth_data)
      return chart
    
    def get_varga_nakshatra(self, varga_key, d1_degree, varga_sign):
        """
        Calculates Nakshatra number, name, lord, and Pada for a planet in a Varga chart.
        Parameters:
        varga_key (str): The Varga key (e.g., 'D2', 'D9').
        d1_degree (float): The degree of the planet in the D1 chart.
        varga_sign (int): The sign of the planet in the Varga chart.
        Returns:
        dict: A dictionary containing the calculated Nakshatra information.
        """
        varga_multipliers = {
            'D2': 2, 'D3': 3, 'D7': 7, 'D9': 9,
            'D10': 10, 'D12': 12, 'D30': 30, 'D60': 60
        }

        key = varga_key.upper()
        if key not in varga_multipliers:
            raise ValueError(
                f"Unsupported Varga '{varga_key}'. "
                f"Choose from {list(varga_multipliers.keys())}"
            )

        multiplier = varga_multipliers[key]
        arc_span = 30.0 / multiplier

        raw_mod = d1_degree % arc_span
        if math.isclose(raw_mod, arc_span, rel_tol=1e-9) or math.isclose(raw_mod, 0.0, abs_tol=1e-9):
            internal_varga_degree = 0.0
        else:
            internal_varga_degree = raw_mod * multiplier

        absolute_varga_longitude = (
            ((varga_sign - 1) * 30.0)
            + internal_varga_degree
        )
        absolute_varga_longitude %= 360.0

        nakshatra_span = 360.0 / 27.0  # 13.33333 degrees per nakshatra
        pada_span = nakshatra_span / 4.0  # 3.33333 degrees per pada

        # 1. Calculate overall Nakshatra Number & Name
        nakshatra_number = math.floor(absolute_varga_longitude / nakshatra_span) + 1
        nakshatra_name = NAKSHATRA_NAMES[nakshatra_number - 1]

        # 2. Calculate Nakshatra Lord
        # We use (number - 1) % 9 to loop through the 9-planet array repeatedly
        lord_index = (nakshatra_number - 1) % 9
        nakshatra_lord = NAKSHATRA_LORDS[lord_index]

        # 3. Calculate Pada (1 to 4)
        degrees_into_nakshatra = absolute_varga_longitude % nakshatra_span
        pada = math.floor(degrees_into_nakshatra / pada_span) + 1

        return {
            "nakshatra_number": nakshatra_number,
            "nakshatra_name": nakshatra_name,
            "nakshatra_lord": nakshatra_lord,
            "pada": pada,
            "degree": round(internal_varga_degree, 3)
        }



    def d1_chart_engine(self):
        """
        Calculate the D1 chart based on the provided D1 chart data.
        
        Parameters:
        birth_data (dict): A dictionary containing the D1 chart data with keys as planet names and values as their positions in degrees.
        
        Returns:
        dict: A dictionary containing the calculated D1 chart with planet names as keys and their corresponding Nakshatra names as values.
        """
        chart = self.birth_info
        d1_chart_dict = dict()

        #View the D1 (Birth Chart) Planetary Positions
        for planet, details in chart["planets"].items():        
            d1_chart_dict[planet] = {"Sign": details['sign'], "Degree": details['degree'],"House":details['house'],"Nakshatra":details['nakshatra'],"Pada":details['pada'],"Nakshatra_lord":details['nakshatra_lord'],"Retrograde":details['is_retrograde'],"Combust":details['is_combust']}


        return d1_chart_dict

    def d9_chart_engine(self):
      
      '''Calculate the D9 chart based on the provided D1 chart data.
      Parameters: birth_data (dict): A dictionary containing the D1 chart data with keys as planet names and values as their positions in degrees.
      Returns: dict: A dictionary containing the calculated D9 chart with planet names as keys and their corresponding Nakshatra names as values.
      '''
      chart = self.birth_info
      lagna = chart['lagna']['d9_sign']
      lagna_rashi_number = RASHI_NUMBER[lagna]
      map = self.rashi_house_mapper(lagna_rashi_number)
      d9_chart_dict = dict()
      for planet, details in chart["planets"].items():
            nakshatra_details = self.get_varga_nakshatra('D9', details['degree'], RASHI_NUMBER[details['d9_sign']])        
            d9_chart_dict[planet] = {"Sign": details['d9_sign'], "Degree": nakshatra_details['degree'],"House":map[RASHI_NUMBER[details['d9_sign']]],"Nakshatra":nakshatra_details['nakshatra_name'],"Pada":nakshatra_details['pada'],"Nakshatra_lord":nakshatra_details['nakshatra_lord'],"Retrograde":details['is_retrograde'],"Combust":''}
      return d9_chart_dict
      



    def rashi_house_mapper(self,lagna):
      '''**Return dictionary format Rashi:House'''
      map = dict()
      i = lagna
      j = 1
      for k in range(12):
        map[i] = j
        j = j+1
        i = (i+1)%12
        if i==0:
          i=12
      return map



