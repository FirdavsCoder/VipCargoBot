from loader import dp
from .throttling import ThrottlingMiddleware
from .user_check import UserCheckMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(UserCheckMiddleware())
