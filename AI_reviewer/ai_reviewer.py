import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from openai import OpenAI
from AI_reviewer.config import GROQ_API_KEY, GROQ_MODEL

# Initialize the client with the correct base URL and API key
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

def review_diff_with_ai(diff_text):
    # Prepare the prompt with the given diff text
    prompt = f"""
    Bạn là một kỹ sư phần mềm chuyên review pull request. Dưới đây là đoạn diff code:

    ```diff
    {diff_text}
    ```
    """

    try:
        # Call the chat completions endpoint with the prepared prompt
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia review code thông minh và sắc sảo."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=512,
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        # Handle errors and print the error message
        print(f"[ERROR] {str(e)}", file=sys.stderr)
        return "Đã xảy ra lỗi khi review bằng Groq."
