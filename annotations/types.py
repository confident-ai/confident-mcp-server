from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Literal

class Annotation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    rating: int
    type: Literal["THUMBS_RATING", "FIVE_STAR_RATING"]
    name: Optional[str] = None
    expectedOutcome: Optional[str] = None
    expectedOutput: Optional[str] = None
    explanation: Optional[str] = None
    createdAt: Optional[str] = None
    traceUuid: Optional[str] = None
    spanUuid: Optional[str] = None
    threadId: Optional[str] = None
    testCaseId: Optional[str] = None
    userEmail: Optional[str] = None

class ListAnnotationsRequest(BaseModel):
    trace_uuid: Optional[str] = Field(None, alias="traceUuid")
    span_uuid: Optional[str] = Field(None, alias="spanUuid")
    thread_id: Optional[str] = Field(None, alias="threadId")
    type: Optional[Literal["THUMBS_RATING", "FIVE_STAR_RATING"]] = None
    min_rating: Optional[str] = Field(None, alias="minRating") 
    max_rating: Optional[str] = Field(None, alias="maxRating")
    page: Optional[int] = 1
    page_size: Optional[int] = Field(25, alias="pageSize")
    start: Optional[str] = None
    end: Optional[str] = None
    sort_by: Optional[Literal["createdAt"]] = Field("createdAt", alias="sortBy")
    ascending: Optional[Literal["asc", "desc"]] = None

class ListAnnotationsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    annotations: List[Annotation]
    total: int
    page: Optional[int] = None
    pagesize: Optional[int] = None

class GetAnnotationRequest(BaseModel):
    annotation_id: str = Field(alias="annotationId")

class CreateAnnotationRequest(BaseModel):
    trace_uuid: Optional[str] = Field(None, alias="traceUuid")
    span_uuid: Optional[str] = Field(None, alias="spanUuid")
    thread_id: Optional[str] = Field(None, alias="threadId")
    
    rating: float
    type: Optional[Literal["THUMBS_RATING", "FIVE_STAR_RATING"]] = Field("THUMBS_RATING")
    
    expected_output: Optional[str] = Field(None, alias="expectedOutput")
    expected_outcome: Optional[str] = Field(None, alias="expectedOutcome")
    explanation: Optional[str] = None
    user_id: Optional[str] = Field(None, alias="userId")

class UpdateAnnotationRequest(BaseModel):
    annotation_id: str = Field(alias="annotationId", exclude=True)
    
    rating: Optional[float] = None
    type: Optional[Literal["THUMBS_RATING", "FIVE_STAR_RATING"]] = None
    expected_output: Optional[str] = Field(None, alias="expectedOutput")
    expected_outcome: Optional[str] = Field(None, alias="expectedOutcome")
    explanation: Optional[str] = None

class AnnotationMutationResponseData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str