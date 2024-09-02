from __future__ import annotations

FILENAME = "model-settings.json"
TEMPLATE = """
{{
    "name": "model",
    "implementation": "{}",
    "parameters": {{
        "uri": "{}"
    }}
}}
""".lstrip(
    "\n"
)
