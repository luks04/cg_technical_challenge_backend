class User:
    """Custom User class
    
    Attributes:
    -----------
        username (str): Username
        password (str): Password
    """
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
    