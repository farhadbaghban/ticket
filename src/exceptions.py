from fastapi import HTTPException, status


class ExpireToken(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Token expired"
        self.headers = {"WWW-Authenticate": "Bearer"}


class HeaderNotFound(HTTPException):
    def __ini__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "auth header not found."


class ValidationToken(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "Could not validate credentials."
        self.headers = {"WWW-Authenticate": "Bearer"}


class UserAlreadyExists(HTTPException):
    def __init__(self) -> None:
        self.status_code = 400
        self.detail = "user alreadt exists!"


class UserNotFound(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "user with this username and password not found!"


class StadiumNotFound(HTTPException):
    def __init__(self)->None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "Stadium with this id not found!"


class StadiumNotCreated(HTTPException):
    def __init__(self)->None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Stadium did not created"



class StadiumAlreadyExists(HTTPException):
    def __init__(self) -> None:
        self.status_code = 400
        self.detail = "stadium alreadt exists!"


class MaxStadiumSeats(HTTPException):
    def __init__(self,stadium_name)->None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"You can add more seats for this stadium {stadium_name}"


class SeatsNotCreated(HTTPException):
    def __init__(self)->None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Seats did not created"

            