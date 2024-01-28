from config import API_HOST, API_PORT, API_ROUTES_DIR, API_STATIC_DIRS

#
# Main Python Flask (or FastAPI?) code goes here
# Highly recommend using some kind of 'file based routing' like this:
# https://github.com/ebubekir/fastapi-directory-routing
#
# Basically, you just have a routes directory with a bunch of files
# that contain your routes and they are automatically loaded
# into the app
#

print("Server should be running on: http://" + API_HOST + ":" + str(API_PORT))
print("Server should be serving the api from:", API_ROUTES_DIR)
print("Server should also be statically serving from:", API_STATIC_DIRS)
