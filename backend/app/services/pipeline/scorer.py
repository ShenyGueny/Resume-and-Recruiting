import json
import anthropic
from ...schemas.pipeline import ExtractionResult, MatchResult, GeneratedContent, ScoreBreakdown

MODEL = "claude-haiku-4-5-20251001"

SYSTEM = (
    "You are an expert ATS scoring engine. "
    "Respond only with valid JSON — no preamble, no explanation."
)

PROMPT = """Score this candidate's fit for the target role on a 0-100 ATS scale.

Required Skills: {required_skills}
Matched Skills: {matched_skills}
Missing Skills: {missing_skills}
Skill Match Percentage: {match_percentage}%
Experience Level Required: {experience_level}
Candidate Experience: {experience}
Candidate Education: {education}

Score each dimension independently, then provide a total.
Respond with JSON matching exactly this schema:
{{
  "skills": <0-100 score based on skills match>,
  "experience": <0-100 score based on experience relevance and level>,
  "education": <0-100 score based on education fit>
}}"""


def score(
    client: anthropic.Anthropic,
    extraction: ExtractionResult,
    match_result: MatchResult,
    profile: dict,
) -> tuple[float, ScoreBreakdown]:
    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=SYSTEM,
        messages=[
            {
                "role": "user",
                "content": PROMPT.format(
                    required_skills=extraction.required_skills,
                    matched_skills=match_result.matched_skills,
                    missing_skills=match_result.missing_skills,
                    match_percentage=match_result.match_percentage,
                    experience_level=extraction.experience_level,
                    experience=json.dumps(profile.get("experience", []), indent=2),
                    education=json.dumps(profile.get("education", []), indent=2),
                ),
            },
            {"role": "assistant", "content": "{"},
        ],
    )
    raw = "{" + response.content[0].text
    data = json.loads(raw)
    breakdown = ScoreBreakdown(**data)
    total = round(
        breakdown.skills * 0.5 + breakdown.experience * 0.35 + breakdown.education * 0.15,
        1,
    )
    return total, breakdown
