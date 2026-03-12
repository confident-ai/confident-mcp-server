
import aiohttp
import os
from enum import Enum
from contextvars import ContextVar
from typing import Optional, Any, Dict
from .types import ApiResponse, ConfidentApiError
from mcp_logger import logger

confident_api_key: ContextVar[Optional[str]] = ContextVar("confident_api_key", default=None)

from constants.env import (
    CONFIDENT_REGION,
    CONFIDENT_ENVIRONMENT,
    CONFIDENT_BACKEND_LOCAL_URL,
    CONFIDENT_BACKEND_US_PROD_URL,
    CONFIDENT_BACKEND_EU_PROD_URL,
    CONFIDENT_BACKEND_AU_PROD_URL,
    CONFIDENT_BACKEND_ON_PREM_URL,
    Environments,
    Regions,
)

if CONFIDENT_ENVIRONMENT == Environments.ON_PREM:
    if not CONFIDENT_BACKEND_ON_PREM_URL:
        raise ValueError(
            "CONFIDENT_BACKEND_ON_PREM_URL must be set when CONFIDENT_ENVIRONMENT=ON_PREM"
        )
    CONFIDENT_BASE_URL = CONFIDENT_BACKEND_ON_PREM_URL
elif CONFIDENT_ENVIRONMENT == Environments.PROD:
    if CONFIDENT_REGION == Regions.EU:
        if not CONFIDENT_BACKEND_EU_PROD_URL:
            raise ValueError(
                "CONFIDENT_BACKEND_EU_PROD_URL must be set when CONFIDENT_ENVIRONMENT=PROD and CONFIDENT_REGION=EU"
            )
        CONFIDENT_BASE_URL = CONFIDENT_BACKEND_EU_PROD_URL
    elif CONFIDENT_REGION == Regions.AU:
        if not CONFIDENT_BACKEND_AU_PROD_URL:
            raise ValueError(
                "CONFIDENT_BACKEND_AU_PROD_URL must be set when CONFIDENT_ENVIRONMENT=PROD and CONFIDENT_REGION=AU"
            )
        CONFIDENT_BASE_URL = CONFIDENT_BACKEND_AU_PROD_URL
    else:
        if not CONFIDENT_BACKEND_US_PROD_URL:
            raise ValueError(
                "CONFIDENT_BACKEND_US_PROD_URL must be set when CONFIDENT_ENVIRONMENT=PROD and CONFIDENT_REGION=US"
            )
        CONFIDENT_BASE_URL = CONFIDENT_BACKEND_US_PROD_URL
elif CONFIDENT_ENVIRONMENT == Environments.LOCAL:
    if not CONFIDENT_BACKEND_LOCAL_URL:
        raise ValueError("CONFIDENT_BACKEND_LOCAL_URL is not configured")
    CONFIDENT_BASE_URL = CONFIDENT_BACKEND_LOCAL_URL
else:
    raise ValueError(
        f"Unknown CONFIDENT_ENVIRONMENT: {CONFIDENT_ENVIRONMENT}. Must be set to 'LOCAL' or 'PROD' or 'ON_PREM'"
    )


class HttpMethods(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"


class Endpoints(Enum):
    PROMPTS_VERSION_ID_ENDPOINT = "/v1/prompts/:alias/versions/:version"
    PROMPTS_LABEL_ENDPOINT = "/v1/prompts/:alias/labels/:label"
    PROMPTS_ENDPOINT = "/v1/prompts"
    PROMPTS_VERSIONS_ENDPOINT = "/v1/prompts/:alias/versions"
    PROMPTS_COMMITS_ENDPOINT = "/v1/prompts/:alias/commits"
    PROMPTS_COMMIT_HASH_ENDPOINT = "/v1/prompts/:alias/commits/:hash"

    DATASET_ALIAS_ENDPOINT = "/v1/datasets/:alias"
    DATASETS_ENDPOINT = "/v1/datasets"
    
    EVALUATE_THREAD_ENDPOINT = "/v1/evaluate/threads/:threadId"
    EVALUATE_TRACE_ENDPOINT = "/v1/evaluate/traces/:traceUuid"
    EVALUATE_SPAN_ENDPOINT = "/v1/evaluate/spans/:spanUuid"
    EVALUATE_ENDPOINT = "/v1/evaluate"
    SIMULATE_ENDPOINT = "/v1/simulate"

    TRACES_ENDPOINT = "/v1/traces"
    TRACE_ID_ENDPOINT =  "/v1/traces/:traceUuid"
    THREADS_ENDPOINT = "/v1/threads"
    THREAD_ID_ENDPOINT = "/v1/threads/:threadId"
    SPANS_ENDPOINT = "/v1/spans"
    SPAN_ID_ENDPOINT = "/v1/spans/:spanUuid"
    
    ANNOTATIONS_ENDPOINT = "/v1/annotations"
    ANNOTATION_ID_ENDPOINT = "/v1/annotations/:annotationId"

    TEST_RUNS_ENDPOINT = "/v1/test-runs"
    TEST_RUN_ID_ENDPOINT = "/v1/test-runs/:testRunId"

    METRIC_COLLECTIONS_ENDPOINT = "/v1/metric-collections"

class Api:
    def __init__(self, base_url: Optional[str] = None):
        self.base_headers = {"Content-Type": "application/json"}
        self.base_api_url = base_url or CONFIDENT_BASE_URL

    async def send_request(
        self,
        method: HttpMethods,
        endpoint: Endpoints,
        path_params: Optional[Dict[str, str]] = None,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> ApiResponse:
        endpoint_path = endpoint.value
        if path_params:
            for key, value in path_params.items():
                endpoint_path = endpoint_path.replace(f":{key}", str(value))

        url = f"{self.base_api_url}{endpoint_path}"

        resolved_key = confident_api_key.get() or os.getenv("CONFIDENT_API_KEY") # Fallback to environment variable for people running the server locally

        logger.info(f"Request: {method.value} - {url} - CONFIDENT_KEY - {resolved_key}")

        request_headers = self.base_headers.copy()
        if resolved_key:
            request_headers["confident-api-key"] = resolved_key

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=method.value,
                    url=url,
                    headers=request_headers,
                    json=body,
                    params=params,
                ) as response:
                    data = await response.json()

                    if not response.ok:
                        raise ConfidentApiError(
                            message=data.get("error", "Unknown API Error"),
                            status_code=response.status,
                            link=data.get("link"),
                        )

                    return ApiResponse.model_validate(data)
            except aiohttp.ClientError as e:
                raise ConfidentApiError(
                    message=f"Network error: {str(e)}", status_code=500
                )
