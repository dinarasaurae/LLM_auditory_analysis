import praw
from collections import defaultdict
import csv

reddit = praw.Reddit(
    client_id='QnDDSCK_6ypYdQN5Yc6LUA',
    client_secret='OgS6eiDmqJGlDsNpd_-aqsQKhqKX4A',
    user_agent='reddit_data_mining',
    username = 'data_mining by NaughtyChinchilla'
)
subreddit_name = 'LLM'
subreddit = reddit.subreddit(subreddit_name)
subreddits_commented = defaultdict(int)

for submission in subreddit.new(limit=8): 
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        user = comment.author
        if user: 
            for user_comment in reddit.redditor(str(user.name)).comments.new(limit=50):
                subreddits_commented[user_comment.subreddit.display_name] += 1
                
with open('subreddits_commented.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['subreddit_name', 'comment_amount'])  
    for subreddit, count in subreddits_commented.items():
        writer.writerow([subreddit, count])