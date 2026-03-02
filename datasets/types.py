from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Literal, Optional, List, Any

class Golden(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    input: str
    expected_output: Optional[str] = Field(default=None, alias="expectedOutput")
    actual_output: Optional[str] = Field(default=None, alias="actualOutput")
    context: Optional[List[str]] = None
    retrieval_context: Optional[List[str]] = Field(default=None, alias="retrievalContext")
    source_file: Optional[str] = Field(default=None, alias="sourceFile")

class GoldenTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ConversationalGolden(BaseModel):
    model_config = ConfigDict(use_enum_values=True, populate_by_name=True)
    scenario: str
    turns: List[GoldenTurn]
    expected_outcome: Optional[str] = Field(default=None, alias="expectedOutcome")
    context: Optional[List[str]] = None
    additional_metadata: Optional[Dict[str, Any]] = Field(default=None, alias="additionalMetadata")

class DatasetData(BaseModel):
    alias: str
    multi_turn: bool = Field(default=False, alias="multiTurn")
    goldens: Optional[List[Golden]] = None
    conversational_goldens: Optional[List[ConversationalGolden]] = Field(
        default=None, alias="conversationalGoldens"
    )

class PullDatasetRequest(BaseModel):
    alias: str
    finalized: bool = True

class PushDatasetRequest(BaseModel):
    dataset: DatasetData
    finalized: bool = True

class DatasetResponse(BaseModel):
    dataset: DatasetData
    id: str
    link: Optional[str] = None

class Datasets(BaseModel):
    id: str
    alias: str
    multi_turn: bool = Field(default=False, alias="multiTurn")

class ListDatasetsResponse(BaseModel):  
    datasets: List[Datasets]