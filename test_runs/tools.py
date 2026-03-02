from confident_mcp import mcp
from confident.api import Api, HttpMethods, Endpoints
from .types import (
    ListTestRunsRequest,
    ListTestRunsResponse,
    GetTestRunRequest,
    GetTestRunResponseData
)

api = Api()

@mcp.tool()
async def list_test_runs(request: ListTestRunsRequest) -> ListTestRunsResponse:
    """
    This tool retrieves a paginated list of test runs (evaluations) from Confident AI.
    Use this to see recent experiments, check if a test run passed/failed, or filter 
    for specific environments or multi-turn conversational tests.

    Args:
     - request
       - status (Optional[str]): Filter by 'COMPLETED', 'ERRORED', 'IN_PROGRESS', or 'CANCELLED'.
       - multiTurn (Optional[str]): Filter for multi-turn tests ("true" or "false").
       - sortBy (Optional[str]): Sort by 'createdAt' or 'runDuration'.
       - ascending (Optional[str]): Sort ascending ("true" or "false").
       - start / end (Optional[str]): ISO datetime filters.
       - page / pageSize (Optional[int]): Pagination controls.

    Response:
     - ListTestRunsResponse: A list of test runs containing pass/fail metrics, duration, and AI-generated summaries.
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.TEST_RUNS_ENDPOINT,
        params=request.model_dump(by_alias=True, exclude_none=True)
    )
    
    return ListTestRunsResponse.model_validate(response.data)

@mcp.tool()
async def get_test_run(request: GetTestRunRequest) -> GetTestRunResponseData:
    """
    This tool retrieves the complete details of a specific test run using its unique ID.
    Use this to deeply inspect exactly which test cases failed, view the specific metric 
    scores (and reasoning) for each test case, and examine the tools called during the execution.

    Args:
     - request
       - testRunId (str): The unique ID of the test run to retrieve.

    Response:
     - GetTestRunResponseData: Detailed results containing aggregated metric scores and a 
       full list of evaluated test cases (including multi-turn conversations).
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.TEST_RUN_ID_ENDPOINT,
        path_params={"testRunId": request.test_run_id}
    )
    
    return GetTestRunResponseData.model_validate(response.data)