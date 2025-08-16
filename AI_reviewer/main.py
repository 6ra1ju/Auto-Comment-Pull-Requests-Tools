from fastapi import FastAPI, Request, Header, HTTPException
from AI_reviewer.github_api import get_pull_request_diff, post_comment_to_pr
from temporalio.client import Client
import os
import asyncio
from AI_reviewer.temporal.temporal_review_workflow import ReviewAndCommentWorkflow

app = FastAPI()

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")
async def start_review_workflow(pr_number, diff):
    client = await Client.connect("localhost:7233")
    handle = await client.start_workflow(
        "ReviewAndCommentWorkflow",
        args=[pr_number, diff],
        id=f"review-pr-{pr_number}",
        task_queue="review-pr-queue",
    )
    return await handle.result()

@app.post("/webhook")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None)
):
    body = await request.body()
    payload = await request.json() 
    if x_github_event == "pull_request":
        action = payload.get("action")
        if action in ["opened", "synchronize", "reopened"]:
            pr = payload["pull_request"]
            pr_number = pr["number"]
            print(f"Received PR webhook: #{pr_number} {action}")
            diff = get_pull_request_diff(pr_number)
            if not diff:
                print("⚠️ Không có diff để review.")
                return {"msg": "No diff to review."}
            asyncio.create_task(start_review_workflow(pr_number, diff))
    return {"msg": "ok"}