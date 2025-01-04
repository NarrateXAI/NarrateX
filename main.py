import asyncio
from agent import *
from character import *
from t2v import *
from twitter_agent import *

async def main(prompt):
    agent = AgentModule("ollama:llama3.2")
    classification_result = await agent.classification_agent.run(prompt)
    result = await agent.character_agent.run(prompt, deps=mc_lore)
    print("Prompt Classification:", classification_result.data.classification )
    print("$MDV",result.data)
    # if classification_result.data.classification != "Chat":
    #     t2v_result = await agent.t2v_agent.run(f"Generate prompt for text-to-video generator model using this AI Agent response: {result.data}", deps=planet)
    #     print("T2V Prompt:",t2v_result.data.prompt)
    #     t2v_model = T2VModel()
    #     generated_video = t2v_model.generate_video(
    #         prompt=t2v_result.data.prompt
    #     )
    #     print("Generated Video Result:", generated_video)
    #     return result.data, generated_video[0]['video']
    return result.data, "Chat"
if __name__ == '__main__':
    TWITTER_COOKIES=os.getenv('TWITTER_COOKIES')
    BASE_URL = os.getenv('BASE_URL')
    DRIVER_PATH = os.getenv('DRIVER_PATH') # Update with your ChromeDriver path
    while True:
        prompt = str(input("> "))
        if prompt == "x":
            try:
                print("="*5,"Get mentioned tweet","="*5)
                # Scrape mentions
                username = "MadivalVoyage"
                automation = XBot(driver_path=DRIVER_PATH, base_url=BASE_URL, cookie=TWITTER_COOKIES)
                automation.login()
                mentions = automation.scrape_mentions(username)
                for mention in mentions:
                    print(mention)
                print("="*5,"Get last tweet","="*5)
                last_tweet = mentions[0]
                message = last_tweet['tweet'].replace("@MadivalVoyage\n ", "")
                print("="*5,"Get AI Agent Response","="*5)
                # response, video_path = asyncio.run(main(message))
                response, video_path = "My origin planet, Arco Magna! Mars' largest hub for interstellar research & trade. Colonized by my parents, renowned explorers who taught me the cosmos. Terraforming domes with artificial gravity support a diverse community.", "C:\\Users\\Alfian\\AppData\\Local\\Temp\\gradio\\e49772d03ef9d76cf1b811361c136d0ef8bb7c8eb066f7ba9299c41e04da89b9\\20250101_185947.mp4"
                if video_path == "Chat":
                    print("="*5,"Post tweet","="*5)
                    tweet = response + f"\n{last_tweet['href']}"
                    automation.login()
                    automation.send_tweet(
                        tweet
                    )
                else:
                    print("="*5,"Post tweet","="*5)
                    tweet = response + f"\n{last_tweet['href']}"
                    automation.login()
                    automation.upload_file(video_path)
                    automation.send_tweet(
                        tweet
                    )
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                automation.close()
        elif prompt == "exit":
            break
        else:
            asyncio.run(main(prompt))