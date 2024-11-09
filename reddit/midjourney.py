import asyncpraw
import asyncio
import csv
from datetime import datetime, timezone

async def main():
    reddit = asyncpraw.Reddit(
        client_id='QnDDSCK_6ypYdQN5Yc6LUA',
        client_secret='OgS6eiDmqJGlDsNpd_-aqsQKhqKX4A',
        user_agent='reddit_data_mining',
    )

    subreddit_name = 'midjourney'
    subreddit = await reddit.subreddit(subreddit_name)

    start_time = datetime(2019, 1, 1, tzinfo=timezone.utc).timestamp()
    end_time = datetime(2021, 1, 1, tzinfo=timezone.utc).timestamp()

    with open('midjourney_async_posts_details.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['post_title', 'upvotes', 'num_comments', 'date_created'])
        async for submission in subreddit.new(limit=70):
            if start_time <= submission.created_utc <= end_time:
                created_date = datetime.fromtimestamp(submission.created_utc, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([submission.title, submission.score, submission.num_comments, created_date])

    await reddit.close()

if __name__ == '__main__':
    asyncio.run(main())
