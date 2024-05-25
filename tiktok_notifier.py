from TikTokApi import TikTokApi
from discord import Embed, SyncWebhook , File
import time
import asyncio
import os
import pyktok as pyk
from args import parse_arguments


def retry(retries=3, delay=30, backoff=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_delay = delay
            for retry_count in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retry_count == retries:
                        print(f"Exception: {e}, all retries failed.")
                        return None
                    print(
                        f"Exception: {e}, trying again in {current_delay} seconds. ({retry_count+1}/{retries})"
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator


@retry()
def send_webhook(
    webhook: SyncWebhook, embed: dict, username: str = "", avatar_url: str = "", file: File = ""
):
    webhook.send(
        username=username,
        avatar_url=avatar_url,
        embed=Embed.from_dict(embed),
        file=file
    )
    return True

async def latest_video(accountname, ms_token):
    async with TikTokApi() as api:
        print(f"Checking Account: {accountname}")
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        counter = 1
        async for video in api.user(accountname).videos(count=2):
            return video.id

def save_video(accountname, video_id):
        url = f"https://www.tiktok.com/@{accountname}/video/{video_id}"
        print(url)
        videopath = pyk.save_tiktok(url + '?is_copy_url=1&is_from_webapp=v1', True,'','edge')
        return videopath

def main():
    
    args = parse_arguments()
    webhook = SyncWebhook.from_url(args.webhook)
    ms_token = args.token

    while True:
        old_feed = []
        if os.path.exists(args.archive):
            print(args.archive)
            with open(args.archive, "r") as f:
                old_feed = [line.strip() for line in f.readlines()]

        video_id = asyncio.run(latest_video(args.account, ms_token))

        print(f"Latest Video ID: {video_id}")
        if video_id in old_feed:
            print(f"Video already posted, skipping...")
        elif old_feed == [] or args.force_old:
            filepath = save_video(args.account, video_id)
            video = File(filepath)
            webhook.send(file=video)
            print(f"Webhook sent!")
            os.remove(filepath)
                    
            with open(args.archive, "a+") as f:
                f.write(video_id + "\n")
        else:
            filepath = save_video(args.account, video_id)
            video = File(filepath)
            webhook.send(file=video)
            print(f"Webhook sent!")
            os.remove(filepath)
                    
            with open(args.archive, "a+") as f:
                f.write(video_id + "\n")

        if not args.continuous:
            break

        print(f"Sleeping for {args.interval}")
        time.sleep(args.interval.total_seconds())



if __name__ == "__main__":
    main()