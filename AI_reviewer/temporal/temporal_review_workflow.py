# AI_reviewer/temporal/temporal_review_workflow.py
from datetime import timedelta
from temporalio import workflow
from AI_reviewer.temporal.activities import review_diff_with_ai_activity, post_comment_to_pr_activity
from AI_reviewer.temporal.activities import review_diff_with_ai_activity_timeout, post_comment_to_pr_activity_timeout
from temporalio.common import RetryPolicy

@workflow.defn
class ReviewAndCommentWorkflow:
    @workflow.run
    async def run(self, pr_number: int, diff_text: str) -> str:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=5),
            maximum_interval=timedelta(seconds=60),
            maximum_attempts=3,
            backoff_coefficient=2,
        )
        review = await workflow.execute_activity(
            review_diff_with_ai_activity,
            diff_text,
            schedule_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )
        github_retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=3),
            maximum_interval=timedelta(seconds=30),
            maximum_attempts=3,
            backoff_coefficient=2,
        )
        # Gửi comment với retry
        status = await workflow.execute_activity(
            #post_comment_to_pr_activity,
            post_comment_to_pr_activity_timeout,
            args=[pr_number, review],
            schedule_to_close_timeout=timedelta(seconds=30),
            retry_policy=github_retry_policy,
        )
        return f"Comment status: {status}"