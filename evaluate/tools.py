from confident_mcp import mcp
from confident.api import Api, HttpMethods, Endpoints
from .types import (
    EvaluateRequest, 
    EvaluateResponseData,
    SimulateRequest,
    SimulateResponseData
)
from mcp_logger import logger

api = Api()

@mcp.tool()
async def run_llm_evals(request: EvaluateRequest) -> EvaluateResponseData:
    """
    This tool triggers an online evaluation for a batch of raw, local test cases on Confident AI.

    Args:
     - request
       - metricCollection (str): The name of the metric collection to use for grading.
       - llmTestCases (Optional[List[LLMTestCase]]): A list of single-turn test cases to evaluate.
       - conversationalTestCases (Optional[List[ConversationalTestCase]]): A list of multi-turn test cases.
       - hyperparameters (Optional[Dict]): Track variables like model name, prompt alias, or temperature.
       - identifier (Optional[str]): A custom name/identifier for this specific test run.

    Response:
     - EvaluateResponseData: Contains the unique 'id' of the newly created test run.
    """
    logger.info(f"Called tool 'run_llm_evals' with params: {request.model_dump(exclude_none=True)}")
    response = await api.send_request(
        method=HttpMethods.POST,
        endpoint=Endpoints.EVALUATE_ENDPOINT,
        body=request.model_dump(by_alias=True, exclude_none=True)
    )
    
    return EvaluateResponseData.model_validate(response.data)

@mcp.tool()
async def simulate_conversation(request: SimulateRequest) -> SimulateResponseData:
    """
    This tool simulates the next step of a conversational flow using Confident AI. 
    It takes a 'ConversationalGolden' (which contains a scenario, user description, and turn history) 
    and returns a simulated user response that tries to advance the conversation toward the 'expectedOutcome'.

    Args:
     - request: A SimulateRequest containing the ConversationalGolden.
       - conversationalGolden.scenario (str): The context of the conversation.
       - conversationalGolden.expectedOutcome (str): The goal the simulated user is trying to reach.
       - conversationalGolden.turns (List[Turn]): The current chat history.

    Response:
     - SimulateResponseData: Contains the new simulated 'userResponse', whether the outcome is 'completed', 
       and the updated 'turns' list.
    """
    logger.info(f"Called tool 'simulate_conversation' with params: {request.model_dump(exclude_none=True)}")
    response = await api.send_request(
        method=HttpMethods.POST,
        endpoint=Endpoints.SIMULATE_ENDPOINT,
        body=request.model_dump(by_alias=True, exclude_none=True)
    )
    
    return SimulateResponseData.model_validate(response.data)
