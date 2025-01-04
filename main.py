import asyncio
from agent import *
from character import *
from t2v import *
from twitter_agent import *
from db import *

async def main(prompt):
    agent = AgentModule("ollama:llama3.2")
    classification_result = await agent.classification_agent.run(prompt)
    result = await agent.character_agent.run(prompt, deps=mc_lore)
    print("Prompt Classification:", classification_result.data.classification )
    print("$NTX",result.data)
    if classification_result.data.classification != "Chat":
        t2v_result = await agent.t2v_agent.run(f"Generate prompt for text-to-video generator model using this AI Agent response: {result.data}", deps=planet)
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
                mentions = automation.scrape_mentions(username, tweet_limit=1, start_time="2025-01-01 00:00:00", end_time="2025-01-01 23:59:59")
                print(mentions)
                for mention in mentions:
                    if mention == "No Data":
                        print("No Data")
                        break
                    # Save to DB
                    db = TweetDatabase()
                    exist = db.check_if_exist(mention["tweet_id"])
                    # if exist:
                    #     print("Data already exist!")
                    #     continue
                    db.save_tweet(
                        mention["tweet_id"],
                        mention["username"],
                        mention["content"],
                        mention["created_at"],
                        mention["href"]
                    )
                    message = mention['content'].replace(f"@{username}\n ", "")
                    print("="*5,"Get AI Agent Response","="*5)
                    response, video_path = asyncio.run(main(message))
                    # response, video_path = """Arco Magna, my Martian origin planet, is a hub for interstellar research and trade. It's a sprawling colony with terraforming domes that simulate a comfortable environment. The sky is a deep crimson, and the landscape is dotted with futuristic architecture and research facilities. A city of interconnected domes, each containing a different ecosystem, stretches out towards the horizon.""", "C:\\Users\\Alfian\\AppData\\Local\\Temp\\gradio\\50342854308bff8236e9b0818c277ebdae79eb52f1af1e9ddf5b8517670b8507\\20250104_183203.mp4"
                    if len(response) > 230:
                        cut = response.split(".")[0:2]
                        response = ".".join(cut) + "."
                        print(response)
                    if video_path == "Chat":
                        print("="*5,"Post tweet","="*5)
                        tweet = response + f"\n{mention['href']}"
                        db.save_response(
                            mention["tweet_id"],
                            tweet,
                            None,
                            datetime.now()
                        )
                        db.close()
                        automation.login()
                        automation.send_tweet(
                            tweet
                        )
                    else:
                        print("="*5,"Post tweet","="*5)
                        tweet = response + f"\n{mention['href']}"
                        db.save_response(
                            mention["tweet_id"],
                            tweet,
                            video_path,
                            datetime.now()
                        )
                        db.close()
                        automation.login()
                        automation.upload_file(video_path)
                        automation.send_tweet(
                            tweet
                        )
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                automation.close()
        elif prompt == "x schedule":
            min = int(input("Input time (in minutes): "))
            while True:
                print(f"System sleep for {min} minutes")
                time.sleep(min * 60)
                print("System on")
                try:
                    print("="*5,"Get mentioned tweet","="*5)
                    # Scrape mentions
                    username = "MadivalVoyage"
                    automation = XBot(driver_path=DRIVER_PATH, base_url=BASE_URL, cookie=TWITTER_COOKIES)
                    automation.login()
                    start = datetime.now() - timedelta(minutes=min)
                    start = start.strftime("%Y-%m-%d %H:%M:%S")
                    end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    mentions = automation.scrape_mentions(username, tweet_limit=1, start_time=start, end_time=end)
                    print(mentions)
                    for mention in mentions:
                        if mention == "No Data":
                            print("No Data")
                            break
                        # Save to DB
                        db = TweetDatabase()
                        exist = db.check_if_exist(mention["tweet_id"])
                        if exist:
                            print("Data already exist!")
                            continue
                        db.save_tweet(
                            mention["tweet_id"],
                            mention["username"],
                            mention["content"],
                            mention["created_at"],
                            mention["href"]
                        )
                        message = mention['content'].replace(f"@{username}\n ", "")
                        print("="*5,"Get AI Agent Response","="*5)
                        # response, video_path = asyncio.run(main(message))
                        response, video_path = """Arco Magna, my Martian origin planet, is a hub for interstellar research and trade. It's a sprawling colony with terraforming domes that simulate a comfortable environment. The sky is a deep crimson, and the landscape is dotted with futuristic architecture and research facilities. A city of interconnected domes, each containing a different ecosystem, stretches out towards the horizon.""", "C:\\Users\\Alfian\\AppData\\Local\\Temp\\gradio\\50342854308bff8236e9b0818c277ebdae79eb52f1af1e9ddf5b8517670b8507\\20250104_183203.mp4"
                        if len(response) > 230:
                            cut = response.split(".")[0:2]
                            response = ".".join(cut) + "."
                            print(response)
                        if video_path == "Chat":
                            print("="*5,"Post tweet","="*5)
                            tweet = response + f"\n{mention['href']}"
                            db.save_response(
                                mention["tweet_id"],
                                tweet,
                                None,
                                datetime.now()
                            )
                            db.close()
                            automation.login()
                            automation.send_tweet(
                                tweet
                            )
                        else:
                            print("="*5,"Post tweet","="*5)
                            tweet = response + f"\n{mention['href']}"
                            db.save_response(
                                mention["tweet_id"],
                                tweet,
                                video_path,
                                datetime.now()
                            )
                            db.close()
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