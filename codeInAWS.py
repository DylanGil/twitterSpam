import json
import tweepy
import keys_test as keys

msgToSend = "#FixTheFriendSystem https://twitter.com/_Kowai_/status/1574837310356688927/video/1"


def api():
    auth = tweepy.OAuth1UserHandler(keys.api_key, keys.api_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)
    return tweepy.API(auth)


def send_reply(api: tweepy.API, fileName: str, userName="Xeralya"):
    filepath = './tmp/' + fileName
    fileTweet = open(filepath, 'r')
    tweetsIds = fileTweet.readlines()
    fileTweet.close()
    file1 = open(filepath, 'w')
    file1.writelines("")
    file1.close()
    gotProblem = False
    valueToReturn = ""
    for tweet in api.user_timeline(screen_name=userName, count=5):
        tweetAlreadyAnswered = False
        for tweetId in tweetsIds:
            if tweetId.rstrip() == tweet.id_str:
                tweetAlreadyAnswered = True

        if not tweetAlreadyAnswered:
            try:
                api.update_status(status=msgToSend, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                if gotProblem == False:
                    valueToReturn = "Tweeted !"
            except tweepy.errors.TweepyException as e:
                valueToReturn = e
                gotProblem = True
            except StopIteration:
                valueToReturn = "Error Xeralya"
                gotProblem = True
                break
        file1 = open(filepath, 'a')  # 'w' pour ecraser le contenu, 'a' pour ecrire en plus
        file1.writelines(str(tweet.id) + "\n")
        file1.close()
    return valueToReturn


def lambda_handler(event, context):
    send_reply(api, "japTweetsIds.txt", "dokkan_official")
    result = send_reply(api, "tweetsIds.txt", "dokkan_global")

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
