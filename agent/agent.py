import google.generativeai as genai
import os

from config import config


def create_model():
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    except KeyError:
        raise Exception(
            "No API key found. Please set the GEMINI_API_KEY environment variable."
        )

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=config["aiagent"]["config"],
        system_instruction=config["aiagent"]["prompts"]["agent"],
    )
    return model