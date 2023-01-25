import tweepy
import keys_test as keys

# msgToSend = "#FixTheFriendSystem https://twitter.com/_Kowai_/status/1574837310356688927/video/1"
msgToSend = "Give us the true DF of this campaign"
imgPath = "gohancell.jpeg"

def api():
    auth = tweepy.OAuth1UserHandler(keys.api_key, keys.api_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)
    return tweepy.API(auth)


def send_reply(api: tweepy.API, fileName: str, userName="Xeralya" ):
    fileTweet = open(fileName, 'r')
    tweetsIds = fileTweet.readlines()
    file1 = open(fileName, 'w')
    file1.writelines("")
    file1.close()
    for tweet in api.user_timeline(screen_name=userName, count=30):
        tweetAlreadyAnswered = False
        for tweetId in tweetsIds:
            if tweetId.rstrip() == tweet.id_str:
                tweetAlreadyAnswered = True

        if not tweetAlreadyAnswered:
            try:
                # api.update_status(status=msgToSend, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                api.update_status_with_media(filename=imgPath, status=msgToSend, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                print("Tweeted !")
            except tweepy.errors.TweepyException as e:
                print(e)
            except StopIteration:
                print("Error Xeralya")
                break
        file1 = open(fileName, 'a')  # 'w' pour ecraser le contenu, 'a' pour ecrire en plus
        file1.writelines(str(tweet.id) + "\n")
        file1.close()
    print("Done !")


if __name__ == '__main__':
    api = api()
    send_reply(api, "tweetsIds.txt", "dokkan_global")
    # send_reply(api, "japTweetsIds.txt", "dokkan_official")
