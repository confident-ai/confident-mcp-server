from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Literal, Union, Any
from enum import Enum


class PromptType(Enum):
    TEXT = "TEXT"
    LIST = "LIST"


class PromptInterpolationType(Enum):
    MUSTACHE = "MUSTACHE"
    MUSTACHE_WITH_SPACE = "MUSTACHE_WITH_SPACE"
    FSTRING = "FSTRING"
    DOLLAR_BRACKETS = "DOLLAR_BRACKETS"
    JINJA = "JINJA"


class PromptMessage(BaseModel):
    role: str
    content: str


class PromptData(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    alias: str
    type: PromptType
    text_template: Optional[str] = None
    messages_template: Optional[List[PromptMessage]] = None
    interpolation_type: PromptInterpolationType = PromptInterpolationType.FSTRING


class PromptResponse(BaseModel):
    prompt_data: PromptData
    hash: str
    version: Optional[str] = None
    label: Optional[str] = None


class PullRequest(BaseModel):
    alias: str
    method: Optional[Literal["version", "label", "hash"]] = None
    value: Optional[str] = None


class InterpolateRequest(BaseModel):
    prompt_data: PromptData
    values: Dict[str, Any]


class PushRequest(BaseModel):
    prompt_data: PromptData
    message: Optional[str] = "Updated via MCP Server"

class CreateVersionRequest(BaseModel):
    alias: str
    hash: str

class CreateVersionResponse(BaseModel):
    version: str
    hash: str

class PromptVersionItem(BaseModel):
    id: str
    version: str

class ListVersionsResponse(BaseModel):
    text_versions: Optional[List[PromptVersionItem]] = Field(default=None, alias="textVersions")
    messages_versions: Optional[List[PromptVersionItem]] = Field(default=None, alias="messagesVersions")

class ListVersionsRequest(BaseModel):
    alias: str

class PromptCommitItem(BaseModel):
    id: str
    hash: str
    message: str

class Prompts(BaseModel):
    id: str
    alias: str
    type: Literal["TEXT", "LIST"]

class ListCommitsResponse(BaseModel):
    commits: List[PromptCommitItem]

class ListCommitsRequest(BaseModel):
    alias: str

class ListPromptsResponse(BaseModel):
    prompts: List[Prompts]