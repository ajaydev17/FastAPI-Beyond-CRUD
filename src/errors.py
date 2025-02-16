from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status


class BooklyException(Exception):
    """
    This is the class for all book errors
    """
    pass


class InvalidToken(BooklyException):
    """
    Raised when the provided token is invalid.
    """
    pass


class RevokedToken(BooklyException):
    """
    Raised when the provided token has been revoked.
    """
    pass


class AccessTokenRequired(BooklyException):
    """
    Raised when the user is not authenticated or provided refresh token instead of access token.
    """


class RefreshTokenRequired(BooklyException):
    """
    Raised when the user is not authenticated or provided access token instead of refresh token.
    """
    pass


class UserAlreadyExists(BooklyException):
    """
    Raised when the user already exists.
    """
    pass


class InvalidCredentials(BooklyException):
    """
    Raised when the provided credentials are invalid.
    """
    pass


class InsufficientPermissions(BooklyException):
    """
    Raised when the user does not have sufficient permissions to perform the requested operation.
    """
    pass


class BookNotFound(BooklyException):
    """
    Raised when the book is not found.
    """
    pass


class UserNotFound(BooklyException):
    """
    Raised when the user is not found.
    """
    pass


class ReviewNotFound(BooklyException):
    """
    Raised when the review is not found.
    """
    pass


def create_exception_handler(status_code: int, initial_detail: Any) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BooklyException):
        return JSONResponse(
            content=initial_detail,
            status_code=status_code,
        )

    return exception_handler

def register_all_exceptions(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists"
            }
        )
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found"
            }
        )
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book not found",
                "error_code": "book_not_found"
            }
        )
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid credentials",
                "error_code": "invalid_credentials"
            }
        )
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Invalid token",
                "resolution": "Please get a new token",
                "error_code": "invalid_token"
            }
        )
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token has been revoked",
                "resolution": "Please get a new token",
                "error_code": "revoked_token"
            }
        )
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Access token required",
                "resolution": "Please provide an access token",
                "error_code": "access_token_required"
            }
        )
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Refresh token required",
                "resolution": "Please provide a refresh token",
                "error_code": "refresh_token_required"
            }
        )
    )

    app.add_exception_handler(
        InsufficientPermissions,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Insufficient permissions",
                "error_code": "insufficient_permissions"
            }
        )
    )

    app.add_exception_handler(
        ReviewNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Review not found",
                "error_code": "review_not_found"
            }
        )
    )
