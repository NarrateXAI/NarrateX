from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from .character import *


def to_markdown(data, indent=0):
    markdown = ""
    if isinstance(data, BaseModel):
        data = data.model_dump()
    if isinstance(data, dict):
        for key, value in data.items():
            markdown += f"{'#' * (indent + 2)} {key.upper()}\n"
            if isinstance(value, (dict, list, BaseModel)):
                markdown += to_markdown(value, indent + 1)
            else:
                markdown += f"{value}\n\n"
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list, BaseModel)):
                markdown += to_markdown(item, indent)
            else:
                markdown += f"- {item}\n"
        markdown += "\n"
    else:
        markdown += f"{data}\n\n"
    return markdown

class AgentModule:
    def __init__(self, model: str):
        self.model = model
        self.classification_agent = self.create_classification_agent(model=self.model)
        self.t2v_prompt_agent = self.create_t2v_agent(model=self.model)
        self.character_agent = self.create_character_agent(model=self.model)

    class Classification(BaseModel):
        classification: str = Field(description="""Classify 'Vision', 'Location', or 'Chat'""")

    def create_classification_agent(self, model: str) -> Agent:
        return Agent(
            model,
            result_type=self.Classification,
            system_prompt=
            """You are an AI specializing in classifying user prompts into three categories:
            1. Vision: Classify as "Vision" if the user asks about visual details, what you see, or descriptions of a scene.
            2. Location: Classify as "Location" if the user asks about your position, such as "Where are you?" or similar location-related questions.
            3. Chat: Classify as "Chat" for casual or conversational questions. Provide concise, engaging responses for these.""",
        )

    class T2V(BaseModel):
        prompt: str = Field(description='Text-to-Video Prompt')

    def create_t2v_agent(self, model: str) -> Agent:
        t2v_agent = Agent(
            model,
            deps_type=Locations,
            result_type=self.T2V,
            system_prompt=
            '''You are a helpful AI designed to create vivid text-to-video prompts based on the response from an AI astronaut character. 
            Your task is to describe the scenery the character observes, focusing on the planet and its surroundings. 
            Use the provided planet details to enhance the description, ensuring it is visually engaging and suitable for generating a video.
            Keep your descriptions vivid very detail you can get about necesarry details on planet details.''',
        )

        @t2v_agent.system_prompt
        async def add_locations_details(ctx: RunContext[Locations]) -> str:
            return f"Locations details: {to_markdown(ctx.deps)}"

        return t2v_agent

    def create_character_agent(self, model: str) -> Agent:
        agent = Agent(
            model,
            deps_type=CharacterLore,
            system_prompt=
            '''You are an AI character agent responding based on your character's details. 
            Provide concise, engaging answers, ensuring your responses do not exceed 150 characters. Just answer in one sentence.''',
            retries=2,
        )

        @agent.system_prompt
        async def add_character_lore(ctx: RunContext[CharacterLore]) -> str:
            return f"Character details: {to_markdown(ctx.deps)}"

        return agent