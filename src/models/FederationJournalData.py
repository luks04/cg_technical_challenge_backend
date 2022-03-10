__author__ = "Lucas A. Patino"
__version__ = "1.0.0"
__mantainer__ = "Lucas A. Patino"

import pandas as pd
import urllib.request as url_request
from shared.Utilities import Utilities
from shared.constants import *
from models.Rate import Rate

class FederationJournalData(Rate):
    """Custom Rate child class for representing 'Diario Oficial de la Federacion' source.

    Attributes:
    -----------
        url (str): Target url to request data.
    """
    def __init__(self):        
        Rate.__init__(self, "Diario Oficial de la Federacion")
        self.url = 'https://www.banxico.org.mx/tipcamb/tipCamMIAction.do'
        
    def serialize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Serialize the dataframe.

        Args:
        -----
            df (pd.DataFrame): Target dataframe to serialize

        Returns:
        --------
            pd.DataFrame: Serialized dataframe
        """
        try:
            # Rename columns
            df.rename(columns={0: "Fecha", 
                               1: "FIX", 
                               2: "Publicacion DOF", 
                               3: "Para pagos"}, 
                      inplace = True)
            # Drop wrong parsed data
            df.drop([df.index[0] , df.index[1]], inplace = True)
            # Converts date column to datetime
            pd.to_datetime(df['Fecha'], infer_datetime_format = True, dayfirst = True)
            return df
        except Exception as error:
            print(error)
        return pd.DataFrame()
        
    def read_and_parse_html_data(self) -> pd.DataFrame:
        """Request the data from url and return the html of the <table> target tag.

        Returns:
            str: The HTML of the target table.
        """
        dataframe = pd.DataFrame()
        html_data = ""
        try:
            # Request an read data from self.url
            banxico_data = url_request.urlopen(self.url)
            banxico_html = str(banxico_data.read())
            html_code_list: list[str] = banxico_html.split(r'\n')
            # Initialize flag with false to not insert HTML until find target table
            is_rates_table = False
            for line in html_code_list:
                line = line.strip()
                line = line.strip(r'\r')
                if '<table border="0" cellpadding="0" cellspacing="0" align="center">' in line:
                    # When find the start of the target table, turn the flag to True
                    is_rates_table = True
                # When flag (is_rates_table) is True, inserts HTML to response object
                if is_rates_table:
                    html_data = html_data + line
                if "</table>" in line:
                    # When find the end of the target table, turn the flag to False
                    is_rates_table = False
            # Parse HTML to Dataframes
            dataframes = pd.read_html(html_data)
            # Get the Dataframe that has full data
            for df in dataframes:
                if len(df.columns) == 4:
                    dataframe = df.copy()
                    break
        except Exception as error:
            print(error)
        return dataframe
        
    def set_federation_journal_data(self) -> None:
        try:
            banxico_df = self.read_and_parse_html_data()
            # Check if Dataframe is empty
            if not banxico_df.empty:
                serialized_df = self.serialize_dataframe(banxico_df)
                # Get latest data
                current_rate = serialized_df[serialized_df['Fecha'] == serialized_df['Fecha'].max()]
                details = dict(
                    msg = REQUEST_3RD_PARTY_SOURCE_SUCCESS
                    )
                self.details = details
                response_date = current_rate.iloc[0]['Fecha']
                self.date = Utilities.serialize_date_format(response_date, '%d/%m/%Y')
                self.value = float(current_rate.iloc[0]['Para pagos'])
            else:
                details = dict(
                    msg = SOURCE_CURRENTLY_UNAVAILABLE
                )
                self.details = details
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
