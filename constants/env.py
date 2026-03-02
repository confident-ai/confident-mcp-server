import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()



class Environments(Enum):
    LOCAL = "LOCAL"
    PROD = "PROD"
    ON_PREM = "ON_PREM"


class Regions(Enum):
    US = "US"
    EU = "EU"
    AU = "AU"


_confident_region_raw = os.getenv("CONFIDENT_REGION")
CONFIDENT_REGION = (
    Regions(_confident_region_raw.upper()) if _confident_region_raw else Regions.US
)

_confident_env_raw = os.getenv("CONFIDENT_ENVIRONMENT")
CONFIDENT_ENVIRONMENT = (
    Environments(_confident_env_raw.upper())
    if _confident_env_raw
    else Environments.LOCAL
)

CONFIDENT_BACKEND_LOCAL_URL = os.getenv("CONFIDENT_BACKEND_LOCAL_URL")
CONFIDENT_BACKEND_US_PROD_URL = os.getenv("CONFIDENT_BACKEND_US_PROD_URL")
CONFIDENT_BACKEND_EU_PROD_URL = os.getenv("CONFIDENT_BACKEND_EU_PROD_URL")
CONFIDENT_BACKEND_AU_PROD_URL = os.getenv("CONFIDENT_BACKEND_AU_PROD_URL")
CONFIDENT_BACKEND_ON_PREM_URL = os.getenv("CONFIDENT_BACKEND_ON_PREM_URL")

_evals_warm_pool_size_raw = os.getenv("EVALS_WARM_POOL_SIZE")
EVALS_WARM_POOL_SIZE = (
    int(_evals_warm_pool_size_raw) if _evals_warm_pool_size_raw else 2
)
