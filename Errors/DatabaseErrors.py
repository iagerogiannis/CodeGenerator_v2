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


class AccountLengthError(CustomError):
    def __init__(self):
        self.message = "Invalid Account! Account is either too long or too short! " \
                       "Password must contain between 6 and 48 characters."


class UsernameLengthError(CustomError):
    def __init__(self):
        self.message = "Invalid Username! Username is either too long or too short! " \
                       "Username must contain between 6 and 48 characters."


class EmailLengthError(CustomError):
    def __init__(self):
        self.message = "Invalid Email Address! Email Address is either too long or too short! " \
                       "Email Address must less than 48 characters."


class PasswordLengthError(CustomError):
    def __init__(self):
        self.message = "Invalid Password! Password is either too long or too short! " \
                       "Password must contain between 6 and 48 characters."


class PassAccountLengthError(CustomError):
    def __init__(self):
        self.message = "Invalid Account! Account is either too long or too short! " \
                       "Account must contain between 2 and 48 characters."


class PassUsernameLengthError(CustomError):
    def __init__(self):
        self.message = "Invalid Username! Username is either too long or too short! " \
                       "Username must contain less than 48 characters."


class PassEmailLengthError(CustomError):
    def __init__(self):
        self.message = "Invalid Email Address! Email Address is too long! " \
                       "Email Address must contain less than 48 characters."

