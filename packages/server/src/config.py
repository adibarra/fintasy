import os
import sys
from typing import List

IS_PRODUCTION: bool = bool(set(["--prod", "--production"]) & set(sys.argv))
API_HOST: str = "localhost"
API_PORT: int = 3000 if IS_PRODUCTION else 3332
API_ROUTES_DIR: str = os.path.join("src", "routes")
API_STATIC_DIRS: List[str] = ["public"]
if IS_PRODUCTION:
    API_STATIC_DIRS.append(os.path.join("..", "client", "dist"))
