from state import State
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import Literal

load_dotenv()  # Load environment variables from .env file
model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)



class TweetGenerator(BaseModel):
    tweet:str

class EvaluatorOutput(BaseModel):
    status: Literal['approved', 'needs_improvement']
    feedback: str

class OptimizerOutput(BaseModel):
    tweet: str



generate_model = model.with_structured_output(TweetGenerator)
evaluate_model = model.with_structured_output(EvaluatorOutput)
optimize_model = model.with_structured_output(OptimizerOutput)


def generate_tweet(state: State):
    user_input = state['user_prompt']
    prompt = f"Generate a concise and engaging tweet based on the following prompt:\n\n{user_input}\n\nTweet, the tweet should be under 280 characters and Funny."
    result = generate_model.invoke(prompt)
    return {'tweet': result.tweet}

def evaluate_tweet(state: State):
    tweet = state['tweet']
    prompt = f"Evaluate the following tweet for its engagement potential and humor. Provide a status ('approved', 'needs_improvement') and constructive feedback for improvement.\n\nTweet: {tweet}\n\nRespond in the format:\nStatus: <status>\nFeedback: <feedback>"
    result = evaluate_model.invoke(prompt)
    return {'status': result.status, 'feedback': result.feedback}

def optimize_tweet(state: State):
    tweet = state['tweet']
    feedback = state['feedback']
    prompt = f"Optimize the following tweet based on the provided feedback to enhance its engagement and humor.\n\nOriginal Tweet: {tweet}\nFeedback: {feedback}\n\nProvide the optimized tweet."
    result = optimize_model.invoke(prompt)
    state['iteration'] += 1
    return {'tweet': result.tweet, 'iteration': state['iteration']}
 