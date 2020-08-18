class CustomError(Exception):
    message: str

    def __str__(self):
        return self.message


class EmptyUsernameError(CustomError):
    def __init__(self):
        self.message = "Username may not be blank! Please enter a username."


class InvalidCharactersInUsernameError(CustomError):
    def __init__(self):
        self.message = "Username may contain only letters (A-Z, a-z), numbers (0-9) and underscore (_)! " \
                       "Please enter a valid username."


class UsernameUsedError(CustomError):
    def __init__(self):
        self.message = "Invalid Username! Username is already in use! Please select a different username."


class EmailUsedError(CustomError):
    def __init__(self):
        self.message = "Invalid Email Address! Email Address is already in use! " \
                       "Please select a different email address."
