from confident_mcp import mcp
from confident.api import Api, HttpMethods, Endpoints
from .types import ListMetricCollectionsResponse
from mcp_logger import logger

api = Api()

@mcp.tool()
async def list_metric_collections() -> ListMetricCollectionsResponse:
    """
    This tool retrieves a list of all available metric collections in your Confident AI project.
    Use this to discover what metric collections exist before triggering a cloud evaluation 
    (e.g., using evaluate_trace, evaluate_span, or evaluate_thread). It tells you the exact 
    'metric_collection' names you can use.

    Response:
     - ListMetricCollectionsResponse: Contains a list of metric collections, including their names, 
       whether they are for multi-turn conversations, and the specific metrics/thresholds inside them.
    """
    logger.info(f"Called tool 'list_metric_collections'.")
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.METRIC_COLLECTIONS_ENDPOINT
    )
    
    return ListMetricCollectionsResponse.model_validate(response.data)