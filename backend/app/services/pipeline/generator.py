import json
import anthropic
from ...schemas.pipeline import ExtractionResult, MatchResult, GeneratedContent

MODEL = "claude-sonnet-4-6"

SYSTEM = (
    "You are an expert resume writer who tailors resumes to specific job descriptions. "
    "You only enhance and reframe real experience — never fabricate or exaggerate. "
    "Respond only with valid JSON — no preamble, no explanation."
)

PROMPT = """Tailor this candidate's resume content for the target role.

Target Role Responsibilities:
{responsibilities}

Skills the Candidate Matches:
{matched_skills}

Candidate's Actual Experience:
{experience}

Rules:
- Only use real experience from the candidate's profile
- Reframe bullet points to emphasize matched skills and relevant impact
- Use strong action verbs and quantify impact where the existing data supports it
- Write a professional summary that bridges the candidate's background to this role

Respond with JSON matching exactly this schema:
{{
  "tailored_bullets": ["3 to 5 rewritten resume bullet points"],
  "summary": "2-3 sentence professional summary tailored to this role"
}}"""


def generate(
    client: anthropic.Anthropic,
    extraction: ExtractionResult,
    match_result: MatchResult,
    profile: dict,
) -> GeneratedContent:
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=SYSTEM,
        messages=[
            {
                "role": "user",
                "content": PROMPT.format(
                    responsibilities=extraction.responsibilities,
                    matched_skills=match_result.matched_skills,
                    experience=json.dumps(profile.get("experience", []), indent=2),
                ),
            },
            {"role": "assistant", "content": "{"},
        ],
    )
    raw = "{" + response.content[0].text
    return GeneratedContent(**json.loads(raw))
