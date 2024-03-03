# package imports
import os
from dotenv import load_dotenv


def getEnvVar():

    load_dotenv(override=True)
    API_KEY = os.environ.get("OPENAI_API_KEY")
    return API_KEY
