from confident_mcp import mcp
from confident.api import Api, HttpMethods, Endpoints
from .types import (
    EvaluateSpanRequestBody,
    EvaluateThreadRequestBody,
    EvaluateTraceRequestBody,
    GetTraceRequest,
    ListTracesResponse,
    TraceData,
    ListTracesRequest,
    ListThreadsRequest,
    ListThreadsResponse,
    GetThreadRequest,
    ThreadDetail,
    ListSpansRequest,
    ListSpansResponse,
    GetSpanRequest,
    SpanData
)

api = Api()

@mcp.tool()
async def evaluate_span(evaluate_span_request_body: EvaluateSpanRequestBody, span_uuid: str):
    """
    This tool can be used to trigger a remote evaluation for a specific span within a trace on Confident AI. 
    Use this when you want to evaluate a granular step of your LLM application (like a retrieval step or a specific tool call) against a predefined metric collection.

    Args:
    - evaluate_span_request_body
    - metric_collection (str): The name of the metric collection to use for evaluation.
    - overwrite_metrics (bool): Whether to overwrite existing evaluation results for this span.
    - span_uuid (str): The unique identifier (UUID) of the span to be evaluated.

    Response:
    - str: A success message with the evaluation ID or a detailed failure message.
    """
    response = await api.send_request(
        method=HttpMethods.POST,
        endpoint=Endpoints.EVALUATE_SPAN_ENDPOINT,
        body=evaluate_span_request_body.model_dump(by_alias=True, exclude_none=True),
        path_params={"spanUuid": span_uuid},
    )

    success = response.success == True
    if success:
        return f"Successfully triggered span evaluation for span {response.data.get('id')}"
    else:
        return f"Failed to trigger span evaluation for span {span_uuid}. Response: {response}"
    

@mcp.tool()
async def evaluate_thread(evaluate_thread_request_body: EvaluateThreadRequestBody, thread_id: str):
    """
    This tool can be used to trigger a remote evaluation for an entire conversation thread on Confident AI. 
    Use this to evaluate multi-turn interactions and ensure consistency and quality across a full session.

    Args:
    - evaluate_thread_request_body
    - metric_collection (str): The name of the metric collection to use for evaluation. Must be a multi-turn metric collection
    - overwrite_metrics (bool): Whether to overwrite existing evaluation results for this thread.
    - chatbot_role (Optional[str]): The role name assigned to the chatbot in this thread for evaluation context.
    - thread_id (str): The identifier of the thread to be evaluated.

    Response:
    - str: A success message with the evaluation ID or a detailed failure message.
    """
    response = await api.send_request(
        method=HttpMethods.POST,
        endpoint=Endpoints.EVALUATE_THREAD_ENDPOINT,
        body=evaluate_thread_request_body.model_dump(by_alias=True, exclude_none=True),
        path_params={"threadId": thread_id},
    )

    success = response.success == True
    if success:
        return f"Successfully triggered thread evaluation for thread {response.data.get('id')}"
    else:
        return f"Failed to trigger thread evaluation for thread {thread_id}. Response: {response}"

@mcp.tool()
async def evaluate_trace(evaluate_trace_request_body: EvaluateTraceRequestBody, trace_uuid: str):
    """
    This tool can be used to trigger a remote evaluation for an entire trace on Confident AI. 
    A trace represents a single end-to-end request in your LLM application. Use this to evaluate the overall performance of a specific execution.

    Args:
    - evaluate_trace_request_body
    - metric_collection (str): The name of the metric collection to use for evaluation.
    - overwrite_metrics (bool): Whether to overwrite existing evaluation results for this trace.
    - trace_uuid (str): The unique identifier (UUID) of the trace to be evaluated.

    Response:
    - str: A success message with the evaluation ID or a detailed failure message.
    """
    response = await api.send_request(
        method=HttpMethods.POST,
        endpoint=Endpoints.EVALUATE_TRACE_ENDPOINT,
        body=evaluate_trace_request_body.model_dump(by_alias=True, exclude_none=True),
        path_params={"traceUuid": trace_uuid},
    )

    success = response.success == True
    if success:
        return f"Successfully triggered trace evaluation for trace {response.data.get('id')}"
    else:
        return f"Failed to trigger trace evaluation for trace {trace_uuid}. Response: {response}"
    

@mcp.tool()
async def get_trace(request: GetTraceRequest) -> TraceData:
    """
    This tool can be used to retrieve the full details of a specific execution trace. 
    A trace includes the overall input/output and a list of all internal spans (steps).

    Args:
     - request
       - trace_uuid (str): The unique identifier (UUID) of the trace to retrieve.

    Response:
     - TraceData: The complete trace details, including metadata, tags, and all associated spans.
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.TRACE_ID_ENDPOINT,
        path_params={"traceUuid": request.trace_uuid}
    )
    
    return TraceData.model_validate(response.data)

@mcp.tool()
async def list_traces(request: ListTracesRequest) -> ListTracesResponse:
    """
    This tool can be used to retrieve a paginated list of traces from Confident AI. 
    Use this to discover recent executions, filter by environment, or find specific 
    trace UUIDs for further inspection with get_trace.

    Args:
     - request
       - page (Optional[int]): The page number to return (default: 1).
       - page_size (Optional[int]): Max traces per page (default: 25).
       - environment (Optional[str]): Filter by environment (e.g., 'production').
       - start (Optional[str]): Filter for traces after this ISO datetime.
       - end (Optional[str]): Filter for traces before this ISO datetime.
       - sort_by (Optional[str]): Field to sort by ('createdAt' or 'endedAt').
       - ascending (Optional[Literal["true", "false"]]): Sort ascending as string ("true" or "false")

    Response:
     - ListTracesResponse: A list of trace summaries and the total count available.
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.TRACES_ENDPOINT,
        params=request.model_dump(by_alias=True, exclude_none=True)
    )
    
    return ListTracesResponse.model_validate(response.data)

@mcp.tool()
async def list_threads(request: ListThreadsRequest) -> ListThreadsResponse:
    """
    This tool can be used to retrieve a paginated list of conversation threads from Confident AI. 
    Use this to discover recent multi-turn conversations, filter by environment, or find specific 
    thread IDs for further inspection with get_thread.

    Args:
     - request
       - page (Optional[int]): The page number to return (default: 1).
       - page_size (Optional[int]): Max threads per page (default: 25).
       - environment (Optional[str]): Filter by environment (e.g., 'production').
       - start (Optional[str]): Filter for threads created after this ISO datetime.
       - end (Optional[str]): Filter for threads created before this ISO datetime.
       - sort_by (Optional[str]): Field to sort by ('createdAt' or 'lastActivity').
       - ascending (Optional[Literal["true", "false"]]): Sort ascending as string ("true" or "false")

    Response:
     - ListThreadsResponse: A list of thread summaries and the total count available.
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.THREADS_ENDPOINT,
        params=request.model_dump(by_alias=True, exclude_none=True)
    )
    
    return ListThreadsResponse.model_validate(response.data)

@mcp.tool()
async def get_thread(request: GetThreadRequest) -> ThreadDetail:
    """
    This tool can be used to retrieve the full details of a specific conversational thread. 
    A thread groups multiple traces together into a single conversation and includes 
    thread-level metrics and annotations.

    Args:
     - request
       - thread_id (str): The unique identifier of the thread to retrieve.

    Response:
     - ThreadDetail: The complete thread details, including metadata, tags, annotations, 
       metrics data, and all associated traces within the thread.
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.THREAD_ID_ENDPOINT,
        path_params={"threadId": request.thread_id}
    )
    
    return ThreadDetail.model_validate(response.data)

@mcp.tool()
async def list_spans(request: ListSpansRequest) -> ListSpansResponse:
    """
    This tool retrieves a paginated list of spans from Confident AI. 
    Spans represent individual steps (e.g., an LLM call, a tool execution, or a retriever step) 
    within a larger trace. Use this to filter specific span types, environments, or prompt versions.

    Args:
     - request
       - page / pageSize (Optional[int]): Pagination controls.
       - start / end (Optional[str]): ISO datetime filters.
       - sort_by / ascending: Sorting configurations.
       - environment (Optional[str]): Filter by 'production', 'staging', etc.
       - type (Optional[str]): Filter by 'llm', 'retriever', 'agent', or 'tool'.
       - traceUuid (Optional[str]): Find all spans belonging to a specific trace.
       - hasError (Optional[bool]): Filter for spans that encountered an error.
       - promptAlias / promptVersion (Optional[str]): Filter by specific prompt tracking.

    Response:
     - ListSpansResponse: A paginated list of spans (excludes deep details like metrics/annotations).
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.SPANS_ENDPOINT,
        params=request.model_dump(by_alias=True, exclude_none=True)
    )
    
    return ListSpansResponse.model_validate(response.data)

@mcp.tool()
async def get_span(request: GetSpanRequest) -> SpanData:
    """
    This tool retrieves the complete details of a specific execution span using its UUID.
    Unlike the list_spans tool, this includes deep details such as the full input/output payload, 
    evaluation metrics data, and human annotations.

    Args:
     - request
       - spanUuid (str): The unique identifier of the span to retrieve.

    Response:
     - SpanData: The complete span details, including I/O, prompt tracking, cost, metrics, and annotations.
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.SPAN_ID_ENDPOINT,
        path_params={"spanUuid": request.span_uuid}
    )
    
    return SpanData.model_validate(response.data)