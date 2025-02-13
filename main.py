import os
from enum import Enum, auto

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
class StoryCommand(Enum):
    FEEDBACK = auto()
    CONTINUE = auto()
    QUIT = auto()
    NEW = auto()

def get_string_command(command_str):
    processed_str = command_str.strip().lower()
    match processed_str:
        case "f" | "feedback":
            return StoryCommand.FEEDBACK
        case "c" | "continue":
            return StoryCommand.CONTINUE
        case "q" | "quit":
            return StoryCommand.QUIT
        case "n" | "new":
            return StoryCommand.NEW
        case _:
            raise ValueError("invalid command")

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

    # main loop to continue the interaction
    while True:
        command_message = "\nWhat would you like to do? Type a single character\n\nc. continue the story\nf. feedback\nn. new story\nq. quit\n"
        command_str = input(command_message).strip()
        com = get_string_command(command_str) # accept multiple commands
        match com:
            case StoryCommand.FEEDBACK:
                feedback = input("\nWould you like it to be funnier, shorter, or include a lesson?").strip()
                print("\nGenerating an updated story...\n")
                updated_prompt = f"""
                        Based on the previous story, make it {feedback}. Keep it suitable for children ages 5–10.
                        """
                updated_story = story.call_model(updated_prompt)
                print(updated_story)
            case StoryCommand.CONTINUE:
                feedback = input("What would you like to happen next?\n").strip()
                print("\nContinuing the story...\n")
                updated_prompt = f"""
                                        Continuing from the previous story: {feedback}. Remember, Keep it suitable for children ages 5–10.
                                        """
                updated_story = story.call_model(updated_prompt)
                print(updated_story)
            case StoryCommand.NEW:
                new_story_input = input("\n").strip()
                print("\nCreating a new story\n")
                updated_story = story.generate_story(new_story_input)
                print(updated_story)
            case StoryCommand.QUIT:
                print("\nGlad you liked it! Sweet dreams!")
                return

if __name__ == "__main__":
    main()