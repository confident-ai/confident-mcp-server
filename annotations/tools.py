from confident_mcp import mcp
from confident.api import Api, HttpMethods, Endpoints
from .types import (
    ListAnnotationsRequest,
    ListAnnotationsResponse,
    GetAnnotationRequest,
    Annotation
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