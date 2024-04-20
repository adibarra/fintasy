# @author: adibarra (Alec Ibarra)
# @description: Configuration file for the server.

import os
import sys
from typing import List

from dotenv import load_dotenv

# check if running in production mode
IS_PRODUCTION: bool = bool(set(["--prod", "--production"]) & set(sys.argv))

# load environment variables
if IS_PRODUCTION:
    if not load_dotenv(dotenv_path=os.path.join("..", "..", ".env.production")):
        print(
            "Failed to load environment vars... Does '.env.production' exist?",
            flush=True,
        )
        sys.exit(1)
else:
    if not load_dotenv(dotenv_path=os.path.join("..", "..", ".env.development")):
        print(
            "Failed to load environment vars... Does '.env.development' exist?",
            flush=True,
        )
        sys.exit(1)


# server configuration
API_HOST: str = os.environ.get("SERVER_API_HOST")
API_PORT: int = int(os.environ.get("SERVER_API_PORT"))
API_CORS_ORIGINS: List[str] = os.environ.get("SERVER_API_CORS_ORIGINS").split(",")
POSTGRESQL_URI: str = os.environ.get("SERVER_POSTGRESQL_URI")
