import json
import anthropic
from ...schemas.pipeline import ExtractionResult

MODEL = "claude-haiku-4-5-20251001"

SYSTEM = (
    "You are an expert ATS resume analyst. "
    "Respond only with valid JSON — no preamble, no explanation."
)

PROMPT = """Analyze this job description and extract structured requirements.

Job Description:
{job_description}

Respond with JSON matching exactly this schema:
{{
  "required_skills": ["list of must-have technical and soft skills"],
  "preferred_skills": ["list of nice-to-have skills"],
  "responsibilities": ["list of 3-6 key responsibilities"],
  "experience_level": "one of: entry | mid | senior | lead"
}}"""


def extract(client: anthropic.Anthropic, job_description: str) -> ExtractionResult:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=[
            {"role": "user", "content": PROMPT.format(job_description=job_description)},
            {"role": "assistant", "content": "{"},
        ],
    )
    raw = "{" + response.content[0].text
    return ExtractionResult(**json.loads(raw))
