import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from AI_reviewer.temporal.temporal_review_workflow import ReviewAndCommentWorkflow
from AI_reviewer.temporal.activities import review_diff_with_ai_activity, post_comment_to_pr_activity, review_diff_with_ai_activity_timeout, post_comment_to_pr_activity_timeout
async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="review-pr-queue",
        workflows=[ReviewAndCommentWorkflow],
        activities=[
            review_diff_with_ai_activity,
            review_diff_with_ai_activity_timeout,
            post_comment_to_pr_activity,
            post_comment_to_pr_activity_timeout,
        ],
    )

    
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())