from temporalio import activity
import asyncio

@activity.defn
async def review_diff_with_ai_activity(diff_text: str) -> str:
    from AI_reviewer.ai_reviewer import review_diff_with_ai
    return review_diff_with_ai(diff_text)

@activity.defn
async def post_comment_to_pr_activity(pr_number: int, comment: str) -> int:
    from AI_reviewer.github_api import post_comment_to_pr
    return post_comment_to_pr(pr_number, comment)

@activity.defn
async def review_diff_with_ai_activity_timeout(diff_text: str) -> str:
    await asyncio.sleep(120) 
    return "Simulated LLM response after timeout"

@activity.defn
async def post_comment_to_pr_activity_timeout(pr_number: int, comment: str) -> int:
    import random
    if random.random() < 1: 
        raise ConnectionError("Simulated network error")
    from AI_reviewer.github_api import post_comment_to_pr
    return post_comment_to_pr(pr_number, comment)