# @author: Alec Ibarra (adibarra)
# @description: User routes for the API

# placeholder pseudocode until the route loading is actually setup


from src.helpers.user import User
from src.services.database import Database

db = Database()


# POST /users
def create_user(ctx):
    body = ctx.request.body

    # verify all required fields are present
    if any(field not in body for field in ["username", "password", "email"]):
        return ctx.code(400).send(
            {
                "code": 400,
                "message": "Bad Request",
            }
        )

    # verify all fields are valid
    try:
        User.validate_username(body["username"])
        User.validate_password(body["password"])
        User.validate_email(body["email"])
    except ValueError:
        return ctx.code(400).send(
            {
                "code": 400,
                "message": "Bad Request",
            }
        )

    # attempt creating user
    try:
        if not db.create_user(
            body["username"], body["email"], User.hash_password(body["password"])
        ):
            return ctx.code(409).send(
                {
                    "code": 409,
                    "message": "Conflict",
                }
            )
    except Exception:
        return ctx.code(500).send(
            {
                "code": 500,
                "message": "Internal Server Error",
            }
        )

    # retrieve new user
    try:
        user = db.get_user_by_email(body["email"])
        if user is None:
            return ctx.code(500).send(
                {
                    "code": 500,
                    "message": "Internal Server Error",
                }
            )
        else:
            return ctx.code(200).send(
                {
                    "code": 200,
                    "message": "OK",
                    "data": {
                        "uuid": user.uuid,
                        "username": user.username,
                        "email": user.email,
                        "coins": user.coins,
                        "created_at": user.created_at,
                        "updated_at": user.updated_at,
                    },
                }
            )
    except Exception:
        return ctx.code(500).send(
            {
                "code": 500,
                "message": "Internal Server Error",
            }
        )


# GET /users/{uuid}
def get_user(ctx):
    params = ctx.params

    # verify all required fields are present
    if "uuid" not in params:
        return ctx.code(400).send(
            {
                "code": 400,
                "message": "Bad Request",
            }
        )

    # attempt fetching user
    try:
        user = db.get_user(params["uuid"])
        if user is None:
            return ctx.code(404).send(
                {
                    "code": 404,
                    "message": "Not Found",
                }
            )
        else:
            return ctx.code(200).send(
                {
                    "code": 200,
                    "message": "OK",
                    "data": {
                        "uuid": user.uuid,
                        "username": user.username,
                        "email": user.email,
                        "coins": user.coins,
                        "created_at": user.created_at,
                        "updated_at": user.updated_at,
                    },
                }
            )
    except Exception:
        return ctx.code(500).send(
            {
                "code": 500,
                "message": "Internal Server Error",
            }
        )


# PATCH /users/{uuid}
def patch_user(ctx):
    params = ctx.params
    body = ctx.request.body

    # verify all required fields are present
    if "uuid" not in params:
        return ctx.code(400).send(
            {
                "code": 400,
                "message": "Bad Request",
            }
        )

    # attempt fetching user
    try:
        user = db.get_user(params["uuid"])
        if user is None:
            return ctx.code(404).send(
                {
                    "code": 404,
                    "message": "Not Found",
                }
            )
    except Exception:
        return ctx.code(500).send(
            {
                "code": 500,
                "message": "Internal Server Error",
            }
        )

    # attempt updating user
    try:
        if "username" in body:
            try:
                User.validate_username(body["username"])
                user.username = body["username"]
            except ValueError:
                return ctx.code(400).send(
                    {
                        "code": 400,
                        "message": "Bad Request",
                    }
                )

        if "password" in body:
            try:
                User.validate_password(body["password"])
                user.password_hash = User.hash_password(body["password"])
            except ValueError:
                return ctx.code(400).send(
                    {
                        "code": 400,
                        "message": "Bad Request",
                    }
                )

        if "email" in body:
            try:
                User.validate_email(body["email"])
                user.email = body["email"]
            except ValueError:
                return ctx.code(400).send(
                    {
                        "code": 400,
                        "message": "Bad Request",
                    }
                )

        if not db.update_user(user):
            return ctx.code(409).send(
                {
                    "code": 409,
                    "message": "Conflict",
                }
            )
    except Exception:
        return ctx.code(500).send(
            {
                "code": 500,
                "message": "Internal Server Error",
            }
        )

    # retrieve updated user
    try:
        user = db.get_user(user.uuid)
        if user is None:
            return ctx.code(500).send(
                {
                    "code": 500,
                    "message": "Internal Server Error",
                }
            )
        else:
            return ctx.code(200).send

    finally:
        print("hello world")
