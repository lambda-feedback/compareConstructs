import openai
from dotenv import load_dotenv
import os


def ai_check(response, answer):
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user",
                   "content": f"Given the following response: \n {response} and answer \n{answer}\n"
                              f"Give me feedbacks of the response in the form of 'Bool' (True or False), 'Feedback' (The feedback of the response"}]

    )
    reply_content = completion.choices[0].message.content
    return reply_content



