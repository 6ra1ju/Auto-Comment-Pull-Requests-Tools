from temporalio.client import Client
import asyncio
from temporalio import activity
import uuid

async def review_diff_with_temporal(diff_text: str) -> str:
    client = await Client.connect("localhost:7233")
    handle = await client.start_workflow(
        "ReviewAndCommentWorkflow",
        diff_text,
        id=f"review-pr-test-timeout-{uuid.uuid4()}",
        task_queue="review-pr-queue",
    )
    return await handle.result()