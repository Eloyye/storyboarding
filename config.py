from environs import env
import openai


def init_api():
    env.read_env()
    openai.api_key = env("OPENAI_API_KEY")
    