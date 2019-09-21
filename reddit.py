import praw

reddit = praw.Reddit(client_id='wHPycitJ-iCxlg',
                     client_secret='91-Y0BJ5iWblL40DkMIrJWDhSk0',
                     user_agent='imageSearch')

def getImages(subreddit):

    output = {}

    for submission in reddit.subreddit(subreddit).hot(limit=10):
        url = submission.url
        if url.endswith(".jpg"):
            output['image'] = submission.url
    return output