import praw
import json

reddit = praw.Reddit(client_id='wHPycitJ-iCxlg',
                     client_secret='91-Y0BJ5iWblL40DkMIrJWDhSk0',
                     user_agent='imageSearch')

def getImages(subreddit):

    output = []

    for submission in reddit.subreddit(subreddit).hot(limit=20):
        url = submission.url
        if url.endswith(".jpg") or url.endswith(".png") or url.endswith(".gif"):
            output.append({
                'id': submission.id,
                'url': submission.url
            })
    return json.dumps(output)