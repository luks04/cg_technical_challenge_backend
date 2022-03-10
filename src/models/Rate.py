__author__ = "Lucas A. Patino"
__version__ = "1.0.0"
__mantainer__ = "Lucas A. Patino"

class Rate:
    """Custom parent class to abstract Exchanges Rates.
    
    Attributes:
    ----------
        source (str | None): The source name of the data.
        date (str | None): The date retrieved from the source.
        value (float | None): The value retrieved from the source.
        details (dict | None): The source name of the data.
    """
    def __init__(self, source: str):
        self.source = source
        self.date = None
        self.value = None
        self.details = None
    
    def get_service_response(self) -> dict:
        """Function to serialize the final service response.
        If self.date and self.value are not None, the field 'success'
        is going to be True, otherwise it is False.

        Returns:
        --------
            dict: A serialized response with source data.
        """
        success_status = self.date is not None and self.value is not None
        data = dict(
            date = self.date,
            value = self.value
        )
        # It is None if there is an error requesting data to 3rd party sources
        rate_data = None if not success_status else data
        # Build the final response
        self.details["source"] = self.source
        response = dict(
            success = success_status,
            data = rate_data,
            details = self.details
        )
        return response
