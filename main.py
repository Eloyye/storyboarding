from enum import Enum, auto

from chat_client import ChatClient
from config import init_runtime_config

"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

My next feature would have been to create a speech interface with the program rather than a CLI program so that
children would have better time interacting with the software. Further, I would like to somehow automate creating
a pdf storybook as a potential option for users. 
"""

class Story:

    def __init__(self, llm_client=None):
        if not llm_client:
            raise ValueError("No llm client provided")
        self.llm_client: ChatClient = llm_client

    def call_model(self, prompt: str, is_done=False) -> str:
        if is_done:
            response = self.llm_client.client_prompt(prompt, "Conclude the story. Ignore creating the title. Make sure it is a happy ending and perhaps include a moral.")
            self.llm_client.clear_history()
            return response
        return self.llm_client.client_prompt(prompt)


    def generate_story(self, user_input: str) -> str:
        self.llm_client.clear_history()
        prompt = f"""
        You are a storytelling assistant. Create a bedtime story for children ages 5–10. 
        Make sure the story is fun, engaging, and age-appropriate. Emphasize interactiveness by asking
        leading questions that will pique the children's interest like "What do you think happens next?" or 
        questions that invoke sensory like "What do you suppose caused that noise?". 
        Use simple language. Title the story, introduce characters, and should lead up to a moral but do not
        mention a moral.
        
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
    END = auto()

def get_string_command(command_str):
    processed_str = command_str.strip().lower()
    match processed_str:
        case "f" | "feedback":
            return StoryCommand.FEEDBACK
        case "c" | "continue":
            return StoryCommand.CONTINUE
        case "e" | "end":
            return StoryCommand.END
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
    client = ChatClient()
    story = Story(llm_client=client)

    story_output = story.generate_story(user_input)
    print("\nHere is your story:\n")
    print(story_output)

    # main loop to continue the interaction
    while True:
        command_message = "\nWhat would you like to do? Type a single character\n\nc. continue the story\ne. end the story\nf. feedback\nn. new story\nq. quit\n"
        command_str = input(command_message).strip()
        com = get_string_command(command_str) # accept multiple commands
        match com:
            case StoryCommand.FEEDBACK:
                feedback = input("\nWould you like it to be funnier, shorter, or include a lesson?\n").strip()
                print("\nGenerating an updated story...\n")
                updated_prompt = f"""
                        Based on the previous story, make it {feedback}. Keep it suitable for children ages 5–10.
                        """
                updated_story = story.call_model(updated_prompt)
                print(updated_story)
            case StoryCommand.CONTINUE:
                prompt = input("What would you like to happen next?\n").strip()
                print("\nContinuing the story...\n")
                updated_prompt = f"""
                                        Continuing from the previous story: {prompt}. Remember, Keep it suitable for children ages 5–10.
                                        """
                updated_story = story.call_model(updated_prompt)
                print(updated_story)
            case StoryCommand.NEW:
                new_story_input = input("\n").strip()
                print("\nCreating a new story\n")
                updated_story = story.generate_story(new_story_input)
                print(updated_story)
            case StoryCommand.END:
                prompt = input("What would you like to happen next for finale?\n").strip()
                print("\nConcluding the story...\n")
                updated_prompt = f"""
                                Continuing from the previous story: {prompt}. Remember, Keep it suitable for children ages 5–10.
                                """
                updated_story = story.call_model(updated_prompt, True)
                print(updated_story)
            case StoryCommand.QUIT:
                print("\nGlad you liked it! Sweet dreams!")
                return

if __name__ == "__main__":
    main()