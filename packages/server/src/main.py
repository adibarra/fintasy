# @author: adibarra (Alec Ibarra)
# @description: The main entry point for the server.

from config import API_CORS_ORIGINS, API_HOST, API_PORT, API_ROUTES_DIR

print("Server starting up...")
print("Server should be listening on: http://" + API_HOST + ":" + str(API_PORT))
print("Server should be serving from:", API_ROUTES_DIR)
print("Server should be allowing CORS from:", API_CORS_ORIGINS)

#
# Main Python Flask (or FastAPI?) code goes here
# Highly recommend using some kind of 'file based routing' like this:
# https://github.com/ebubekir/fastapi-directory-routing
#
# Basically, you just have a routes directory with a bunch of files
# that contain your routes and they are automatically loaded
# into the app
#

print("Server shutting down...\n")
