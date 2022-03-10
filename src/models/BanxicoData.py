__author__ = "Lucas A. Patino"
__version__ = "1.0.0"
__mantainer__ = "Lucas A. Patino"

import os
import requests
from typing import Union
from shared.constants import *
from models.Rate import Rate

class BanxicoData(Rate):
    """Custom Rate child class for representing 'Banxico' source.

    Attributes:
    -----------
        url (str): Target url to request data.
        bmx_token (Union[str, None], optional): Bmx API token. Defaults to None.
    """
    def __init__(self, bmx_token: Union[str, None] = None):
        Rate.__init__(self, "Banxico")
        self.bmx_token = os.environ.get('BMX_TOKEN') if bmx_token is None else bmx_token
        self.url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
    
    def set_banxico_data(self) -> None:
        """Requests data from Banxico API. It use the self.bmx_token received, 
        but if self.bmx_token is None, then it use the bmx_token from the ENV vars. 
        See more https://www.banxico.org.mx/SieAPIRest/service/v1/doc/consultaDatosSerieOp.
        
        Then, it sets the parent attributes from the Banxico API response.
        """
        api_headers = {
            "Accept": "application/json",
            "Bmx-Token": self.bmx_token
        }
        try:
            service_response = requests.get(self.url, headers = api_headers)
            json_response: dict = service_response.json()
            
            if "error" in json_response.keys():
                details = dict(
                    msg = json_response["error"]["mensaje"]
                    )
                self.details = details
            else:
                details = dict(
                    msg = REQUEST_3RD_PARTY_SOURCE_SUCCESS
                    )
                self.details = details
                self.date = json_response["bmx"]["series"][0]["datos"][0]["fecha"]
                self.value = float(json_response["bmx"]["series"][0]["datos"][0]["dato"])
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
