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
        print("Failed to load environment vars... Does '.env.production' exist?")
        sys.exit(1)

# server configuration
API_HOST: str = "localhost"
API_PORT: int = 3000 if IS_PRODUCTION else 3332
API_CORS_ORIGINS: List[str] = os.environ.get("SERVER_API_CORS_ORIGINS").split(",") if IS_PRODUCTION else ["*"]
API_ROUTES_DIR: str = os.path.join("src", "routes")
