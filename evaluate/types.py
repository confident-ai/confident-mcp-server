from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Dict, List, Optional, Literal


class ToolCallData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    name: str
    description: str
    input_parameters: Optional[Dict[str, Any]] = Field(None, alias="inputParameters")
    output: Optional[str] = None
    reasoning: Optional[str] = None

class Turn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    role: Literal["user", "assistant"]
    content: str
    user_id: Optional[str] = Field(None, alias="userId")
    retrieval_context: Optional[List[str]] = Field(None, alias="retrievalContext")
    tools_called: Optional[List[ToolCallData]] = Field(None, alias="toolsCalled")

class LLMTestCase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    input: str
    actual_output: str = Field(alias="actualOutput")
    name: Optional[str] = None
    expected_output: Optional[str] = Field(None, alias="expectedOutput")
    retrieval_context: Optional[List[str]] = Field(None, alias="retrievalContext")
    context: Optional[List[str]] = None
    tools_called: Optional[List[ToolCallData]] = Field(None, alias="toolsCalled")
    expected_tools: Optional[List[ToolCallData]] = Field(None, alias="expectedTools")

class ConversationalTestCase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    turns: List[Turn]
    scenario: Optional[str] = None
    name: Optional[str] = None
    expected_outcome: Optional[str] = Field(None, alias="expectedOutcome")
    user_description: Optional[str] = Field(None, alias="userDescription")
    chatbot_role: Optional[str] = Field(None, alias="chatbotRole")

class EvaluateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    metric_collection: str = Field(alias="metricCollection")
    llm_test_cases: Optional[List[LLMTestCase]] = Field(None, alias="llmTestCases")
    conversational_test_cases: Optional[List[ConversationalTestCase]] = Field(None, alias="conversationalTestCases")
    hyperparameters: Optional[Dict[str, Any]] = None
    identifier: Optional[str] = None

class EvaluateResponseData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str

class ConversationalGolden(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    scenario: str
    user_description: Optional[str] = Field(None, alias="userDescription")
    expected_outcome: Optional[str] = Field(None, alias="expectedOutcome")
    turns: Optional[List[Turn]] = None
    context: Optional[List[str]] = None
    additional_metadata: Optional[Dict[str, Any]] = Field(None, alias="additionalMetadata")
    comments: Optional[str] = None
    source_file: Optional[str] = Field(None, alias="sourceFile")
    finalized: Optional[bool] = None
    custom_column_key_values: Optional[Dict[str, Any]] = Field(None, alias="customColumnKeyValues")

class SimulateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    conversationalGolden: ConversationalGolden

class SimulateResponseData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    simulation_id: Optional[str] = Field(None, alias="simulationId")
    completed: Optional[bool] = None
    user_response: Optional[str] = Field(None, alias="userResponse")
    turns: Optional[List[Turn]] = None