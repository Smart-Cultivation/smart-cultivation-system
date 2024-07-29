import os
# from dotenv import dotenv_values

# config = dotenv_values(".env")

# CONFIG = {
#     "SECRET_KEY": config["SECRET_KEY"],
#     "CACHE_TYPE": "SimpleCache",
#     "CACHE_DEFAULT_TIMEOUT": 300,
#     "SESSION_TYPE": "filesystem",
#     "SQLALCHEMY_DATABASE_URI": config["POSTGRES_URL_NON_POOLING"],
#     "SQLALCHEMY_TRACK_MODIFICATIONS": False,
# }

CONFIG = {
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "SESSION_TYPE": "filesystem",
    "SQLALCHEMY_DATABASE_URI": (
        "mysql+pymysql://"
        + os.getenv("MYSQL_USERNAME")
        + ":"
        + os.getenv("MYSQL_PASSWORD")
        + "@"
        + os.getenv("MYSQL_HOST")
        + "/"
        + os.getenv("MYSQL_DATABASE")
    ),
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
}