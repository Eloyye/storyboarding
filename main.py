import os

from openai import OpenAI

from config import init_runtime_config

"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:
"""

class Story:

    def __init__(self, llm_client=None):
        if not llm_client:
            raise ValueError("No llm client provided")
        self.llm_client: OpenAI = llm_client

    def call_model(self, prompt: str, max_tokens=3000, temperature=0.1) -> str:
        resp = self.llm_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=False,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        if not resp.choices:
            raise ValueError("No response from llm")
        return resp.choices[0].message.content


    def generate_story(self, user_input: str) -> str:
        prompt = f"""
        You are a storytelling assistant. Create a bedtime story for children ages 5–10. 
        Make sure the story is fun, engaging, and age-appropriate. Include a clear beginning, middle, and happy ending. 
        Use simple language. Title the story, introduce characters, and include a moral if relevant.
        
        User request: {user_input}
        
        Start the story now:
        """
        story = self.call_model(prompt)
        return story

example_requests = "A story about a girl named Alice and her best friend Bob, who happens to be a cat."
def main():
    init_runtime_config()
    print("Welcome to the Bedtime Story Generator!")
    user_input = input("What kind of story do you want to hear? (e.g., 'A story about a brave rabbit who saves the day'): ")

    # openai client llm
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    story = Story(llm_client=client)

    story_output = story.generate_story(user_input)
    print("\nHere is your story:\n")
    print(story_output)

    feedback = input("\nDid you like the story? Would you like it to be funnier, shorter, or include a lesson? (Leave blank if you're happy): ").strip()
    if feedback:
        print("\nGenerating an updated story...\n")
        updated_prompt = f"""
        Based on the previous story, make it {feedback}. Keep it suitable for children ages 5–10.
        """
        updated_story = story.call_model(updated_prompt)
        print(updated_story)
    else:
        print("\nGlad you liked it! Sweet dreams!")


if __name__ == "__main__":
    main()