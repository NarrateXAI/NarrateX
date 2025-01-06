from narratexai import *
from .char import *

import os
import asyncio
from datetime import datetime, timedelta
import random
import time

async def main(prompt):
    agent = AgentModule("openai:gpt-4o-mini")
    classification_result = await agent.classification_agent.run(prompt)
    result = await agent.character_agent.run(prompt, deps=character)
    print("Prompt Classification:", classification_result.data.classification )
    print("$Agents",result.data)
    if classification_result.data.classification != "Chat":
        t2v_result = await agent.t2v_agent.run(f"Generate prompt for text-to-video generator model using this AI Agent response: {result.data}", deps=location)
        print("T2V Prompt:",t2v_result.data.prompt)
        t2v_model = T2VModel()
        try_cnt = 0
        while try_cnt!=3:
            try:
                try_cnt+=1
                print("Try:",try_cnt)
                generated_video = t2v_model.generate_video(
                    prompt=t2v_result.data.prompt
                )
                print("Generated Video Result:", generated_video)
                return result.data, generated_video[0]['video']
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
    return result.data, "Chat"
if __name__ == '__main__':
    while True:
        prompt = str(input("> "))
        if prompt == "exit":
            break
        else:
            asyncio.run(main(prompt))