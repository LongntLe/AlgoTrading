import configparser

config = configparser.ConfigParser()
config.read("pyalgo.cfg")

ENVIRONMENTS = {
        "streaming": {
            "real": "stream-fxtrade.oanda.com",
            "practice": "stream-fxpractice.oanda.com"
            },
        "api": {
            "real": "api-fxtrade.oanda.com",
            "practice": "api-fxpractice.oanda.com"
            }
        }

DOMAIN = "practice"
STREAM_DOMAIN = ENVIRONMENTS["streaming"][DOMAIN]
API_DOMAIN = ENVIRONMENTS["api"][DOMAIN]
ACCESS_TOKEN = config["oanda_v20"]["access_token"]
ACCOUNT_ID = config["oanda_v20"]["account_id"]
