from typing import Tuple, TypeAlias

ErrorResponse: TypeAlias = Tuple[dict, int]

INTERNAL_ERROR: ErrorResponse = ({
        "errors": [
            {
                "title": "Something bad happened",
                "status" : "500",
                "meta": "Contact Dima and tell him to fix it"
            }
        ]
    }, 405)

INVALID_METHOD: ErrorResponse = ({
        "errors": [
            {
                "title": "Invalid request method",
                "status" : "405",
                "meta": "Only POST requests are allowed."
            }
        ]
    }, 405)

BAD_REQUEST: ErrorResponse = ({
    "errors": [
            {
                "code": "400",
                "title": "Bad Request",
                "meta": "Data is incorrectly structured"
            }
        ]
    }, 400)

WRONG_SALT: ErrorResponse = ({
    "errors": [
        {
            "code": "400",
            "title": "Bad Request",
            "meta": "Wrong salt"
        }
    ]
}, 403)

ACCOUNT_ALREADY_EXISTS: ErrorResponse = ({
    "errors": [
        {
            "code": "400",
            "title": "Bad Request",
            "meta": "Account already exists"
        }
    ]
}, 400)

NO_FACE_FOUND: ErrorResponse = ({
    "errors": [
            {
                "code": "400",
                "title": "No face found",
                "meta": "No face found in the image"
            }
        ]
    }, 400)

TOO_MANY_PEOPLE: ErrorResponse = ({
        "errors": [
            {
                "code": "400",
                "title": "Too many people",
                "meta": "Too many people found in the image"
            }
        ]
    }, 400)

