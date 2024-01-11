# This code simple get the environment variable for path
# import os

# path = os.getenv("Path")
# print(path)


from config import settings
print('Secret key:', settings.secret_key)