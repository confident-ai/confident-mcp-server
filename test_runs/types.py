from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Dict, List, Optional, Union, Literal

class ListTestRunsRequest(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = Field(25, alias="pageSize")
    status: Optional[Literal["COMPLETED", "ERRORED", "IN_PROGRESS", "CANCELLED"]] = None
    multi_turn: Optional[Literal["true", "false"]] = Field(None, alias="multiTurn")
    sort_by: Optional[Literal["createdAt", "runDuration"]] = Field("createdAt", alias="sortBy")
    ascending: Optional[bool] = False
    start: Optional[str] = None
    end: Optional[str] = None

class GetTestRunRequest(BaseModel):
    test_run_id: str = Field(alias="testRunId")


class MetricScores(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    metric: str
    scores: Optional[List[float]] = None
    passes: Optional[int] = None
    fails: Optional[int] = None
    errors: Optional[int] = None

class TestRunSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    topicSummaries: Optional[List[Dict[str, Any]]] = None
    summaryOverview: Optional[Dict[str, Any]] = None

class TestRunItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    createdAt: str
    identifier: Optional[str] = None
    status: Optional[str] = None
    multiTurn: Optional[bool] = None
    testsPassed: Optional[int] = None
    testsFailed: Optional[int] = None
    totalTests: Optional[int] = None
    metricsScores: Optional[List[MetricScores]] = None
    runDuration: Optional[float] = None
    evaluationCost: Optional[float] = None
    datasetAlias: Optional[str] = None
    testFile: Optional[str] = None
    summary: Optional[TestRunSummary] = None

class ListTestRunsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    testRuns: List[TestRunItem]
    totalTestRuns: int
    page: Optional[int] = None
    pageSize: Optional[int] = None


class ToolCallData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    name: str
    description: str
    inputParameters: Optional[Dict[str, Any]] = None
    output: Optional[str] = None
    reasoning: Optional[str] = None

class MetricsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    score: Optional[float] = None
    reason: Optional[str] = None
    success: Optional[bool] = None
    threshold: float
    evaluationModel: Optional[str] = None
    strictMode: Optional[bool] = None
    error: Optional[str] = None
    evaluationCost: Optional[float] = None
    name: str
    verboseLogs: Optional[str] = None

class TestRunTurn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    role: Literal["user", "assistant"]
    content: str
    toolsCalled: Optional[List[ToolCallData]] = None
    retrievalContext: Optional[List[str]] = None


class TestRunTestCase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    name: str
    input: str
    actualOutput: Optional[str] = None
    context: Optional[List[str]] = None
    retrievalContext: Optional[List[str]] = None
    expectedOutput: Optional[str] = None
    toolsCalled: Optional[List[ToolCallData]] = None
    expectedTools: Optional[List[ToolCallData]] = None
    metricsData: Optional[List[MetricsData]] = None
    comments: Optional[str] = None
    additionalMetadata: Optional[Dict[str, Any]] = None
    success: Optional[bool] = None
    runDuration: Optional[float] = None
    evaluationCost: Optional[float] = None

class TestRunConversationalTestCase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    name: str
    turns: List[TestRunTurn]
    scenario: Optional[str] = None
    expectedOutcome: Optional[str] = None
    userDescription: Optional[str] = None
    context: Optional[List[str]] = None
    comments: Optional[str] = None
    additionalMetadata: Optional[Dict[str, Any]] = None
    metricsData: Optional[List[MetricsData]] = None
    success: Optional[bool] = None
    runDuration: Optional[float] = None
    evaluationCost: Optional[float] = None

class TestRunTraceData(BaseModel):
    """The nested trace object returned inside a trace-based test case."""
    model_config = ConfigDict(populate_by_name=True)
    
    uuid: str
    input: Optional[Any] = None
    output: Optional[Any] = None
    startTime: str
    endTime: Optional[str] = None
    name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    environment: Optional[str] = None
    threadId: Optional[str] = None
    testCaseId: Optional[str] = None
    userId: Optional[str] = None
    metricCollectionName: Optional[str] = None
    retrievalContext: Optional[List[str]] = None
    context: Optional[List[str]] = None
    expectedOutput: Optional[str] = None
    expectedTools: Optional[List[ToolCallData]] = None
    metricsData: Optional[List[MetricsData]] = None
    tags: Optional[List[str]] = None
    spans: Optional[Any] = None

class TestRunTraceTestCase(BaseModel):
    """A test case that wraps a full execution trace rather than just input/output."""
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    name: str
    trace: TestRunTraceData
    metricsData: Optional[List[MetricsData]] = None
    comments: Optional[str] = None
    additionalMetadata: Optional[Dict[str, Any]] = None
    success: Optional[bool] = None
    runDuration: Optional[float] = None
    evaluationCost: Optional[float] = None

class GetTestRunResponseData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    metricsScores: List[MetricScores]
    testCases: List[Union[TestRunTestCase, TestRunConversationalTestCase, TestRunTraceTestCase]]
    multiTurn: Optional[bool] = None
    identifier: Optional[str] = None
    status: Optional[str] = None
    testsPassed: Optional[float] = None
    testsFailed: Optional[float] = None
    totalTests: Optional[float] = None
    runDuration: Optional[float] = None