from confident_mcp import mcp
from confident.api import Api, HttpMethods, Endpoints
from .types import (
    ListAnnotationsRequest,
    ListAnnotationsResponse,
    GetAnnotationRequest,
    Annotation,
    CreateAnnotationRequest,
    UpdateAnnotationRequest,
    AnnotationMutationResponseData
)

api = Api()

@mcp.tool()
async def list_annotations(request: ListAnnotationsRequest) -> ListAnnotationsResponse:
    """
    This tool retrieves a paginated list of annotations (human feedback) from Confident AI.
    Use this to find user feedback, ratings, and corrections applied to specific traces, spans, or threads.

    Args:
     - request
       - traceUuid (Optional[str]): Filter annotations for a specific trace.
       - spanUuid (Optional[str]): Filter annotations for a specific span.
       - threadId (Optional[str]): Filter annotations for a specific thread.
       - type (Optional[str]): Filter by 'THUMBS_RATING' or 'FIVE_STAR_RATING'.
       - minRating / maxRating (Optional[str]): Filter by rating range.
       - page / pageSize (Optional[int]): Pagination controls.

    Response:
     - ListAnnotationsResponse: Contains the list of annotations and pagination metadata (total, limit, offset).
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.ANNOTATIONS_ENDPOINT,
        params=request.model_dump(by_alias=True, exclude_none=True)
    )
    
    return ListAnnotationsResponse.model_validate(response.data)

@mcp.tool()
async def get_annotation(request: GetAnnotationRequest) -> Annotation:
    """
    This tool retrieves the complete details of a specific annotation using its unique ID.
    Use this when you need the full context, explanation, and expected outcome of a single piece of feedback.

    Args:
     - request
       - annotationId (str): The unique ID of the annotation to retrieve.

    Response:
     - Annotation: The complete annotation details, including expected outputs and explanations.
    """
    response = await api.send_request(
        method=HttpMethods.GET,
        endpoint=Endpoints.ANNOTATION_ID_ENDPOINT,
        path_params={"annotationId": request.annotation_id}
    )

    
    data_payload = response.data or {}
    annotation_data = data_payload.get("annotation", {})
    
    return Annotation.model_validate(annotation_data)

@mcp.tool()
async def create_annotation(request: CreateAnnotationRequest) -> AnnotationMutationResponseData:
    """
    This tool creates a new annotation (human feedback) for a specific trace, span, or thread.
    
    CRITICAL VALIDATION RULES:
     1. You MUST provide exactly ONE of the following identifiers: traceUuid, spanUuid, or threadId.
     2. If annotating a trace or span: You MUST use 'expectedOutput'. You CANNOT use 'expectedOutcome'.
     3. If annotating a thread: You MUST use 'expectedOutcome'. You CANNOT use 'expectedOutput'.
     4. 'rating' must be 0 or 1 for THUMBS_RATING, or an integer from 1 to 5 for FIVE_STAR_RATING.

    Args:
     - request: The CreateAnnotationRequest payload.
       - traceUuid / spanUuid / threadId (str): The target identifier.
       - rating (float): The score given by the reviewer.
       - type (str): 'THUMBS_RATING' or 'FIVE_STAR_RATING'.
       - expectedOutput / expectedOutcome (str): The ideal output or outcome.
       - explanation (str): Reason for the rating.
       - userId (str): ID of the user submitting the feedback.

    Response:
     - AnnotationMutationResponseData: Contains the 'id' of the newly created annotation.
    """
    response = await api.send_request(
        method=HttpMethods.POST,
        endpoint=Endpoints.ANNOTATIONS_ENDPOINT,
        body=request.model_dump(by_alias=True, exclude_none=True)
    )
    
    return AnnotationMutationResponseData.model_validate(response.data)

@mcp.tool()
async def update_annotation(request: UpdateAnnotationRequest) -> AnnotationMutationResponseData:
    """
    This tool updates an existing annotation's properties (such as its rating, explanation, or expected output).

    CRITICAL VALIDATION RULES:
     1. If the annotation belongs to a thread: Use 'expectedOutcome'. Do NOT use 'expectedOutput'.
     2. If the annotation belongs to a trace/span: Use 'expectedOutput'. Do NOT use 'expectedOutcome'.

    Args:
     - request: The UpdateAnnotationRequest payload.
       - annotationId (str): The ID of the annotation to update.
       - rating (Optional[float]): The new rating score.
       - type (Optional[str]): 'THUMBS_RATING' or 'FIVE_STAR_RATING'.
       - expectedOutput / expectedOutcome (Optional[str]): The new ideal output/outcome.
       - explanation (Optional[str]): The new explanation.

    Response:
     - AnnotationMutationResponseData: Contains the 'id' of the successfully updated annotation.
    """
    response = await api.send_request(
        method=HttpMethods.PUT,
        endpoint=Endpoints.ANNOTATION_ID_ENDPOINT,
        path_params={"annotationId": request.annotation_id},
        body=request.model_dump(by_alias=True, exclude_none=True)
    )
    
    return AnnotationMutationResponseData.model_validate(response.data)