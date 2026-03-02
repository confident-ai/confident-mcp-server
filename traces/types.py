from typing import Literal, Optional, Any, List, Dict
from pydantic import BaseModel, Field, ConfigDict


class EvaluateThreadRequestBody(BaseModel):
    metric_collection: str = Field(alias="metricCollection")
    overwrite_metrics: bool = Field(alias="overwriteMetrics")
    chatbot_role: Optional[str] = Field(default=None, alias="chatbotRole")


class EvaluateTraceRequestBody(BaseModel):
    metric_collection: str = Field(alias="metricCollection")
    overwrite_metrics: bool = Field(alias="overwriteMetrics")


class EvaluateSpanRequestBody(BaseModel):
    metric_collection: str = Field(alias="metricCollection")
    overwrite_metrics: bool = Field(alias="overwriteMetrics")

class MetricsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    score: Optional[float] = None
    reason: Optional[str] = None
    success: Optional[bool] = None
    threshold: float
    evaluation_model: Optional[str] = Field(None, alias="evaluationModel")
    strict_mode: Optional[bool] = Field(None, alias="strictMode")
    error: Optional[str] = None
    evaluation_cost: Optional[float] = Field(None, alias="evaluationCost")
    name: str
    verbose_logs: Optional[str] = Field(None, alias="verboseLogs")

class Annotation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    rating: int
    type: Literal["THUMBS_RATING", "FIVE_STAR_RATING"]
    name: Optional[str] = None
    expected_outcome: Optional[str] = Field(None, alias="expectedOutcome")
    expected_output: Optional[str] = Field(None, alias="expectedOutput")
    explanation: Optional[str] = None
    created_at: Optional[str] = Field(None, alias="createdAt")
    trace_uuid: Optional[str] = Field(None, alias="traceUuid")
    span_uuid: Optional[str] = Field(None, alias="spanUuid")
    thread_id: Optional[str] = Field(None, alias="threadId")
    test_case_id: Optional[str] = Field(None, alias="testCaseId")
    user_email: Optional[str] = Field(None, alias="userEmail")

class ToolCallData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    name: str
    description: str
    input_parameters: Optional[Dict[str, Any]] = Field(None, alias="inputParameters")
    output: Optional[str] = None
    reasoning: Optional[str] = None


class SpanData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: str
    parent_uuid: Optional[str] = Field(None, alias="parentUuid")
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    start_time: str = Field(alias="startTime")
    end_time: Optional[str] = Field(None, alias="endTime")
    error: Optional[str] = None
    input: Optional[Any] = None
    output: Optional[Any] = None
    expected_output: Optional[str] = Field(None, alias="expectedOutput")
    retrieval_context: Optional[List[str]] = Field(None, alias="retrievalContext")
    context: Optional[List[str]] = None
    tools_called: Optional[List[ToolCallData]] = Field(None, alias="toolsCalled")
    expected_tools: Optional[List[ToolCallData]] = Field(None, alias="expectedTools")
    model: Optional[str] = None
    cost: Optional[float] = None
    input_token_cost: Optional[float] = Field(None, alias="inputTokenCost")
    output_token_cost: Optional[float] = Field(None, alias="outputTokenCost")
    cost_per_input_token: Optional[float] = Field(None, alias="costPerInputToken")
    cost_per_output_token: Optional[float] = Field(None, alias="costPerOutputToken")
    input_token_count: Optional[int] = Field(None, alias="inputTokenCount")
    output_token_count: Optional[int] = Field(None, alias="outputTokenCount")
    prompt_alias: Optional[str] = Field(None, alias="promptAlias")
    prompt_version: Optional[str] = Field(None, alias="promptVersion")
    prompt_label: Optional[str] = Field(None, alias="promptLabel")
    prompt_commit_hash: Optional[str] = Field(None, alias="promptCommitHash")
    embedder: Optional[str] = None
    top_k: Optional[int] = Field(None, alias="topK")
    chunk_size: Optional[int] = Field(None, alias="chunkSize")
    description: Optional[str] = None
    agent_handoffs: Optional[List[Any]] = Field(None, alias="agentHandoffs")
    available_tools: Optional[List[Any]] = Field(None, alias="availableTools")
    metadata: Optional[Dict[str, Any]] = None
    metric_collection_name: Optional[str] = Field(None, alias="metricCollectionName")
    metrics_data: Optional[List[MetricsData]] = Field(None, alias="metricsData")
    annotations: Optional[List[Annotation]] = None


class TraceData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: str
    thread_id: Optional[str] = Field(None, alias="threadId")
    user_id: Optional[str] = Field(None, alias="userId")
    test_case_id: Optional[str] = Field(None, alias="testCaseId")
    name: Optional[str] = None
    status: Optional[str] = None
    start_time: str = Field(alias="startTime")
    end_time: Optional[str] = Field(None, alias="endTime")
    input: Optional[Any] = None
    output: Optional[Any] = None
    tags: Optional[List[str]] = None
    spans: List[SpanData] = Field(default_factory=list)
    cost: Optional[float] = None
    latency: Optional[float] = None
    environment: Optional[str] = None
    metrics_data: Optional[List[MetricsData]] = Field(None, alias="metricsData")

class GetTraceRequest(BaseModel):
    trace_uuid: str = Field(alias="traceUuid")

class TraceSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: str
    name: Optional[str] = None
    input: Optional[str] = None
    output: Optional[str] = None
    start_time: str = Field(alias="startTime")
    end_time: str = Field(alias="endTime")
    environment: Optional[str] = None
    tags: Optional[List[str]] = None
    thread_id: Optional[str] = Field(None, alias="threadId")
    user_id: Optional[str] = Field(None, alias="userId")

class ListTracesRequest(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = Field(25, alias="pageSize")
    environment: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    sort_by: Optional[Literal["createdAt", "endedAt"]] = Field("createdAt", alias="sortBy")
    ascending: Optional[Literal["asc", "desc"]] = None

class ListTracesResponse(BaseModel):
    traces: List[TraceSummary]
    total_traces: int = Field(alias="totalTraces")


class ThreadSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    thread_id: str = Field(alias="threadId")
    created_at: str = Field(alias="createdAt")
    last_activity: str = Field(alias="lastActivity")
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    metric_collection_name: Optional[str] = Field(None, alias="metricCollectionName")
    total_traces: int = Field(alias="totalTraces")

class ListThreadsRequest(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = Field(25, alias="pageSize")
    environment: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    sort_by: Optional[Literal["createdAt", "lastActivity"]] = Field("lastActivity", alias="sortBy")
    ascending: Optional[Literal["asc", "desc"]] = None

class ListThreadsResponse(BaseModel):
    threads: List[ThreadSummary]
    total_threads: int = Field(alias="totalThreads")

class GetThreadRequest(BaseModel):
    thread_id: str = Field(alias="threadId")

class ThreadDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    thread_id: str = Field(alias="threadId")
    created_at: str = Field(alias="createdAt")
    last_activity: str = Field(alias="lastActivity")
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    metric_collection_name: Optional[str] = Field(None, alias="metricCollectionName")
    total_traces: int = Field(alias="totalTraces")
    metrics_data: Optional[List[MetricsData]] = Field(None, alias="metricsData")
    annotations: Optional[List[Annotation]] = None
    traces: Optional[List[TraceData]] = None

class ListSpansRequest(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = Field(25, alias="pageSize")
    start: Optional[str] = None
    end: Optional[str] = None
    sort_by: Optional[Literal["createdAt", "endedAt", "cost", "duration", "name"]] = Field("createdAt", alias="sortBy")
    ascending: Optional[bool] = None
    environment: Optional[Literal["production", "testing", "development", "staging"]] = None
    type: Optional[str] = None  # e.g., 'agent', 'llm', 'retriever', 'tool'
    trace_uuid: Optional[str] = Field(None, alias="traceUuid")
    name: Optional[str] = None
    has_error: Optional[bool] = Field(None, alias="hasError")
    model: Optional[str] = None
    prompt_alias: Optional[str] = Field(None, alias="promptAlias")
    prompt_version: Optional[str] = Field(None, alias="promptVersion")
    prompt_label: Optional[str] = Field(None, alias="promptLabel")
    prompt_commit_hash: Optional[str] = Field(None, alias="promptCommitHash")
    embedder: Optional[str] = None
    top_k: Optional[int] = Field(None, alias="topK")
    chunk_size: Optional[int] = Field(None, alias="chunkSize")

class GetSpanRequest(BaseModel):
    span_uuid: str = Field(alias="spanUuid")

class ListSpansResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    spans: List[SpanData]
    total_spans: int = Field(alias="totalSpans")