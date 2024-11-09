import asyncpraw
import asyncio
import csv
from datetime import datetime, timezone
from config import client_id, client_secret

async def main():
    reddit = asyncpraw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent='reddit_data_mining'
    )

    subreddit_name = 'LLM'
    subreddit = await reddit.subreddit(subreddit_name)

    start_time = datetime(2023, 1, 1, tzinfo=timezone.utc).timestamp()
    end_time = datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp()

    with open('async_posts_details.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['post_title', 'upvotes', 'num_comments', 'date_created'])
        async for submission in subreddit.new(limit=1000):
            if start_time <= submission.created_utc <= end_time:
                created_date = datetime.fromtimestamp(submission.created_utc, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([submission.title, submission.score, submission.num_comments, created_date])

    await reddit.close()

if __name__ == '__main__':
    asyncio.run(main())
