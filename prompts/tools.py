from typing import List, Union
from confident_mcp import mcp
from confident.api import Api, HttpMethods, Endpoints
from .types import (
    PromptData, 
    PromptResponse, 
    PullRequest, 
    InterpolateRequest, 
    PushRequest, 
    CreateVersionRequest,
    PromptMessage,
    ListVersionsRequest,
    ListVersionsResponse,
    ListCommitsRequest,
    ListCommitsResponse,
    ListPromptsResponse
)
from .utils import interpolate_prompt_data

api = Api()

@mcp.tool()
async def pull_prompt(request: PullRequest) -> PromptResponse:
    """
    This tool can be used to fetch a prompt's from Confident AI. 
    A prompt can be pulled using it's alias which is it's identifier or name. 
    If no method or value is provided, the tool retrieves the most recent commit of prompt.

    Args:
     - request
       - alias (str): The unique name of the prompt.
       - method (Optional[Literal["hash", "version", "label"]]): The identifier type to use for fetching.
       - value (Optional[str]): The specific hash, version string (e.g., '1.0.1'), or label name.

    Response:
     - PromptResponse: Contains the 'data' (the prompt's data), current 'hash', 'version', and 'label' and either text or messages depending on prompt type.
    """
    path_params = {"alias": request.alias}
    if request.method == "version":
        endpoint = Endpoints.PROMPTS_VERSION_ID_ENDPOINT
        path_params["version"] = request.value
    elif request.method == "label":
        endpoint = Endpoints.PROMPTS_LABEL_ENDPOINT
        path_params["label"] = request.value
    elif request.method == "hash":
        endpoint = Endpoints.PROMPTS_COMMIT_HASH_ENDPOINT
        path_params["hash"] = request.value
    else:
        endpoint = Endpoints.PROMPTS_COMMIT_HASH_ENDPOINT
        path_params["hash"] = "latest"

    # 2. Send the request via our centralized API client
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=endpoint,
        path_params=path_params
    )
    
    # 3. Map the API response to our MCP types
    data = response.data
    config = PromptData(
        alias=request.alias,
        type=data["type"],
        text_template=data.get("text"),
        messages_template=data.get("messages"),
        interpolation_type=data["interpolationType"]
    )
    
    return PromptResponse(
        config=config,
        hash=data["hash"],
        version=data.get("version"),
        label=data.get("label")
    )

@mcp.tool()
def interpolate_prompt(request: InterpolateRequest) -> Union[str, List[PromptMessage]]:
    """
    This tool can be used to locally render a prompt template by replacing placeholders with actual values. 
    It supports various formats like {variable} or {{variable}} depending on the prompt's configuration.
    This is a local operation and does not hit the Confident AI API.

    Args:
    - request
    - config (PromptData): The prompt's data object containing templates and settings (obtained from pull_prompt).
    - values (Dict[str, Any]): A dictionary where keys match the variable names used in the prompt template.

    Response:
    - Union[str, List[PromptMessage]]: The rendered result as a string for TEXT prompts, or a list of messages for LIST prompts.
    """
    # Uses the local logic in utils.py
    return interpolate_prompt_data(request.config, request.values)

@mcp.tool()
async def push_prompt(request: PushRequest) -> PromptResponse:
    """
    This tool can be used to create new or save modifications made to a prompt's template or configuration back to Confident AI. 
    Every push creates a new commit in the prompt's history, allowing you to track changes over time.
    Note that this does not automatically create a new version string unless create_prompt_version is called afterward.
    Simply using this tool with appropriate data will create a prompt on the Confident AI platform

    Args:
    - request
    - config (PromptData): The updated prompt data to be saved to the platform.
    - message (Optional[str]): A commit message to describe the changes being made.

    Response:
    - PromptResponse: Contains the updated 'data' (the prompt's data), the new commit 'hash', and the current 'version'.
    """
    body = {
        "alias": request.config.alias,
        "interpolationType": request.config.interpolation_type,
        "message": request.message
    }

    if request.config.text_template is not None:
        body["text"] = request.config.text_template

    if request.config.messages_template is not None:
        body["messages"] = [
            m.model_dump() for m in request.config.messages_template
        ]
    
    response = await api.send_request(
        method=HttpMethods.POST,
        endpoint=Endpoints.PROMPTS_ENDPOINT,
        body=body
    )
    
    data = response.data
    return PromptResponse(
        config=request.config,
        hash=data.get("hash", "latest"),
        version=data.get("version")
    )

@mcp.tool()
async def create_prompt_version(request: CreateVersionRequest) -> str:
    """
    This tool can be used to assign a formal version string to a specific commit hash of a prompt. 
    Versions are automatically created on Confident AI and returned here.

    Args:
    - request
    - alias (str): The unique name of the prompt.
    - hash (str): The specific commit hash that you want to version.

    Response:
    - str: A confirmation message indicating the version was successfully created for the specified hash.
    """
    body = {"hash": request.hash}
    await api.send_request(
        method=HttpMethods.POST,
        endpoint=Endpoints.PROMPTS_VERSIONS_ENDPOINT,
        path_params={"alias": request.alias},
        body=body
    )
    
    return f"Successfully created version {request.version} for prompt {request.alias}"

@mcp.tool()
async def list_prompt_versions(request: ListVersionsRequest) -> ListVersionsResponse:
    """
    This tool can be used to retrieve a list of all formal versions associated with a given prompt alias.
    Use this to see which versions of a prompt have been released to production or tagged.

    Args:
     - request
       - alias (str): The unique name of the prompt.

    Response:
     - ListVersionsResponse: Contains lists of 'textVersions' and 'messagesVersions' associated with the prompt.
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.PROMPTS_VERSIONS_ENDPOINT,
        path_params={"alias": request.alias}
    )
    
    return ListVersionsResponse.model_validate(response.data)

@mcp.tool()
async def list_prompt_commits(request: ListCommitsRequest) -> ListCommitsResponse:
    """
    This tool can be used to retrieve a chronological list of all the commits associated with a prompt alias.
    Use this to view the history of changes, find specific commit hashes, and read commit messages.

    Args:
     - request
       - alias (str): The unique name of the prompt.

    Response:
     - ListCommitsResponse: Contains a list of 'commits', detailing the 'id', 'hash', and 'message' for each.
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.PROMPTS_COMMITS_ENDPOINT,
        path_params={"alias": request.alias}
    )
    
    return ListCommitsResponse.model_validate(response.data)

@mcp.tool()
async def list_prompts() -> ListPromptsResponse:
    """
    This tool can be used to retrieve a list of all prompts available in Confident AI.

    Response:
     - ListPromptsResponse: Contains a list of 'prompts', each with an 'id', 'alias', and 'type'.
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.PROMPTS_COMMITS_ENDPOINT,
    )
    
    return ListPromptsResponse.model_validate(response.data)