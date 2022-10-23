import os

URL = os.getenv(key="URL", default="https://petstore.swagger.io/v2")
MAX_ERROR_LENGTH = os.getenv(key="MAX_ERROR_LENGTH", default=250)
RERUN_COUNT = os.getenv(key="RERUN_COUNT", default=3)
