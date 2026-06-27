import anthropic
from ...schemas.pipeline import PipelineContent
from .extractor import extract
from .matcher import match
from .generator import generate
from .scorer import score


def run_pipeline(api_key: str, job_description: str, profile: dict) -> tuple[float, PipelineContent]:
    client = anthropic.Anthropic(api_key=api_key)

    extraction = extract(client, job_description)
    match_result = match(client, extraction, profile)
    generated = generate(client, extraction, match_result, profile)
    total_score, breakdown = score(client, extraction, match_result, profile)

    content = PipelineContent(
        extraction=extraction,
        match=match_result,
        generated=generated,
        score_breakdown=breakdown,
    )
    return total_score, content
