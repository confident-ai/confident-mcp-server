from confident_mcp import mcp
from confident.api import Api, HttpMethods, Endpoints
from .types import (
    ConversationalGolden,
    DatasetData,
    Golden,
    GoldenTurn,
    Optional,
    PullDatasetRequest,
    PushDatasetRequest,
    DatasetResponse,
    ListDatasetsResponse,
)
from mcp_logger import logger

api = Api()

@mcp.tool()
async def pull_dataset(request: PullDatasetRequest) -> DatasetResponse:
    """
    This tool can be used to fetch an entire evaluation dataset from Confident AI. 
    It retrieves all 'goldens' associated with a specific alias.

    Args:
     - request
       - alias (str): The unique name of the dataset to pull.

    Response:
     - DatasetResponse: Contains the 'dataset' state (alias and list of goldens) and the dataset ID.
    """
    logger.info(f"Called tool 'pull_dataset' with params: {request.model_dump(exclude_none=True)}")
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.DATASET_ALIAS_ENDPOINT,
        path_params={"alias": request.alias},
        params={"finalized": str(request.finalized).lower()}
    )
    
    data = response.data
    # Robust multi-turn detection
    raw_conv = data.get("conversationalGoldens")
    is_multi = raw_conv is not None

    if is_multi:
        conv_goldens = []
        for g in (raw_conv or []):
            turns = [
                GoldenTurn(
                    role=t.get("role"), 
                    content=t.get("content")
                ) for t in (g.get("turns") or [])
            ]
            conv_goldens.append(
                ConversationalGolden(
                    scenario=g.get("scenario"),
                    turns=turns,
                    expected_outcome=g.get("expectedOutcome"),
                    context=g.get("context"),
                    additional_metadata=g.get("additionalMetadata")
                )
            )
        dataset_state = DatasetData(
            alias=request.alias, 
            multiTurn=True, 
            conversationalGoldens=conv_goldens
        )
    else:
        raw_goldens = data.get("goldens") or []
        goldens = [Golden(**g) for g in raw_goldens]
        dataset_state = DatasetData(
            alias=request.alias, 
            multiTurn=False, 
            goldens=goldens
        )
    
    return DatasetResponse(
        dataset=dataset_state,
        id=data["id"]
    )


@mcp.tool()
async def list_datasets() -> ListDatasetsResponse:
    """
    This tool can be used to retrieve a list of all datasets available in Confident AI.

    Response:
     - ListDatasetsResponse: Contains a list of 'datasets', each with an 'id', 'alias', and 'multiTurn' boolean.
    """
    logger.info(f"Called tool 'list_datasets'.")
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.DATASETS_ENDPOINT,
    )
    
    return ListDatasetsResponse.model_validate(response.data)