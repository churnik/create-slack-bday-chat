from dotenv import load_dotenv, find_dotenv
from environs import Env

load_dotenv(find_dotenv())

env = Env()
env.read_env()

YOUR_ENV_VARIABLE = env("YOUR_ENV_VARIABLE", "DEFAULT_VALUE")
FLASK_ENV = env("FLASK_ENV", "production")
SLACK_BOT_TOKEN = env("SLACK_BOT_API")
SLACK_SIGNING_SECRET = env("SLACK_SIGNING_SECRET")
SLACK_VERIFICATION_TOKEN = env("SLACK_VERIFICATION_TOKEN")
