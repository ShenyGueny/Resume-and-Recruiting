import json
import anthropic
from ...schemas.pipeline import ExtractionResult, MatchResult

MODEL = "claude-haiku-4-5-20251001"

SYSTEM = (
    "You are an expert ATS resume analyst. "
    "Respond only with valid JSON — no preamble, no explanation."
)

PROMPT = """Compare these job requirements against the candidate's profile.

Required Skills: {required_skills}
Preferred Skills: {preferred_skills}

Candidate Skills: {candidate_skills}
Candidate Experience Titles: {experience_titles}

Respond with JSON matching exactly this schema:
{{
  "matched_skills": ["skills the candidate has that match the requirements"],
  "missing_skills": ["required skills the candidate lacks"],
  "match_percentage": <number 0-100 representing overall fit>
}}"""


def match(
    client: anthropic.Anthropic,
    extraction: ExtractionResult,
    profile: dict,
) -> MatchResult:
    experience_titles = [
        f"{e.get('title', '')} at {e.get('company', '')}"
        for e in profile.get("experience", [])
    ]
    candidate_skills = profile.get("skills", [])

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=[
            {
                "role": "user",
                "content": PROMPT.format(
                    required_skills=extraction.required_skills,
                    preferred_skills=extraction.preferred_skills,
                    candidate_skills=candidate_skills,
                    experience_titles=experience_titles,
                ),
            },
            {"role": "assistant", "content": "{"},
        ],
    )
    raw = "{" + response.content[0].text
    return MatchResult(**json.loads(raw))
