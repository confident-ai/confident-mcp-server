import re
from typing import Any, List, Union, Dict
from .types import PromptInterpolationType, PromptMessage, PromptType, PromptData


def interpolate_text(
    interpolation_type: PromptInterpolationType, text: str, **kwargs: Any
) -> str:
    """Apply the appropriate interpolation method based on the type"""

    if (
        interpolation_type == PromptInterpolationType.FSTRING
        or interpolation_type == "FSTRING"
    ):
        return re.sub(
            r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}",
            lambda m: str(kwargs.get(m.group(1), m.group(0))),
            text,
        )

    elif interpolation_type in [PromptInterpolationType.MUSTACHE, "MUSTACHE"]:
        return re.sub(
            r"\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}",
            lambda m: str(kwargs.get(m.group(1), m.group(0))),
            text,
        )

    elif interpolation_type in [
        PromptInterpolationType.MUSTACHE_WITH_SPACE,
        "MUSTACHE_WITH_SPACE",
    ]:
        return re.sub(
            r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}",
            lambda m: str(kwargs.get(m.group(1), m.group(0))),
            text,
        )
    return text


def interpolate_prompt_data(
    prompt_data: PromptData, values: Dict[str, Any]
) -> Union[str, List[PromptMessage]]:
    """Helper to interpolate either TEXT or LIST prompts locally"""
    if prompt_data.type == "TEXT" or prompt_data.type == PromptType.TEXT:
        return interpolate_text(
            prompt_data.interpolation_type, prompt_data.text_template, **values
        )

    elif prompt_data.type == "LIST" or prompt_data.type == PromptType.LIST:
        interpolated_messages = []
        for msg in prompt_data.messages_template:
            interpolated_content = interpolate_text(
                prompt_data.interpolation_type, msg.content, **values
            )
            interpolated_messages.append(
                PromptMessage(role=msg.role, content=interpolated_content)
            )
        return interpolated_messages
