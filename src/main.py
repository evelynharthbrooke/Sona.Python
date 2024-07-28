try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from client import Client

with open("./config.toml", mode="rb") as c:
    config = tomllib.load(c)

bot = Client()
token = config["general"]["token"]

bot.run(token)
