try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from client import Client

with open("./config.toml", mode="rb") as c:
    config = tomllib.load(c)


token = config["general"]["api"]["token"]

bot = Client()

bot.run(token)
