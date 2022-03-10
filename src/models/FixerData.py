__author__ = "Lucas A. Patino"
__version__ = "1.0.0"
__mantainer__ = "Lucas A. Patino"

import os
import requests
from typing import Union
from shared.constants import *
from models.Rate import Rate

class FixerData(Rate):
    """Custom Rate child class for representing 'Fixer' source.

    Attributes:
    -----------
        url (str): Target url to request data.
        access_key (Union[str, None], optional): Fixer API Access Key. Defaults to None.
    """
    def __init__(self, access_key: Union[str, None] = None):
        Rate.__init__(self, "Fixer")
        self.access_key = os.environ.get('FIXER_ACCESS_KEY') if access_key is None else access_key
        self.url = f"http://data.fixer.io/api/latest?access_key={self.access_key}&base=MXN"
        
    def set_fixer_data(self) -> None:
        """Requests data from Fixer API. It use the self.access_key received, 
        but if self.access_key is None, then it use the access_key from the ENV vars.
        See more https://fixer.io/documentation.

        Then, it sets the parent attributes from the Fixer API response.
        """
        try:
            service_response = requests.get(self.url)
            json_response: dict = service_response.json()
            
            if "error" in json_response.keys():
                details = dict(
                    msg = json_response["error"]["type"]
                    )
                self.details = details
            else:
                details = dict(
                    msg = REQUEST_3RD_PARTY_SOURCE_SUCCESS
                    )
                self.details = details
                self.date = json_response["date"]
                self.value = float(json_response["rates"]["USD"])
        except KeyError as key:
            print(f"{key} does not exist in the source response. {MAYBE_3RD_PARTY_RESPONSE_HAS_CHANGED_MSG}")
            details = dict(
                msg = MAYBE_3RD_PARTY_RESPONSE_HAS_CHANGED_MSG
                )
            self.details = details
        except Exception as error:
            print(error)
            details = dict(
                msg = f"{DEFAULT_EXCEPTION_MSG}: " + str(error)
                )
            self.details = details
