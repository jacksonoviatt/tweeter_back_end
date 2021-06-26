from os import link
import mariadb
from flask import Flask, request, Response
from flask_cors.core import get_regexp_pattern
import dbhelpers
import json
import traceback
import sys
import secrets
from email.utils import parseaddr
import users
import tweets
import likes
import comments


app = Flask(__name__)


@app.post("/api/users")
def users_post():
    return users.post_user()

@app.delete("/api/users")
def users_delete():
    return users.delete_user()

@app.get("/api/users")
def users_get():
    return users.get_users()

@app.patch("/api/users")
def users_patch():
    return users.patch_users()




@app.post("/api/login")
def login_post():
    return users.post_login()

@app.delete("/api/login")
def login_delete():
    return users.delete_login()

@app.post("/api/tweets")
def tweet_post():
    return tweets.post_tweet()


@app.get("/api/tweets")
def get_tweets():
    return tweets.get_tweet()

@app.delete("/api/tweets")
def delete_tweets():
    return tweets.delete_tweet()

@app.patch("/api/tweets")
def patch_tweets():
    return tweets.patch_tweet()



@app.post("/api/tweet-likes")
def post_likes():
    return likes.post_like('tweetId', 'tweet_likes', 'tweet_id')


@app.delete("/api/tweet-likes")
def delete_likes():
    return likes.delete_like('tweetId', 'tweet_likes', 'tweet_id')


@app.get("/api/tweet-likes")
def get_likes():
    return likes.get_like('tweetId', 'tweet_likes', 'tweet_id', {'tweetId': likes[0], 'userId': likes[1], 'username': likes[2]})




@app.post("/api/comments")
def post_comments():
    return comments.post_comment()

@app.get("/api/comments")
def get_comments():
    return comments.get_comment()

@app.delete("/api/comments")
def delete_comments():
    return comments.delete_comment()
@app.patch("/api/comments")
def patch_comments():
    return comments.patch_comment()


@app.post("/api/comment-likes")
def post_comment_likes():
    return likes.post_like('commentId', 'comment_likes', 'comment_id')


@app.delete("/api/comment-likes")
def delete_comment_likes():
    return likes.delete_like('commentId', 'comment_likes', 'comment_id')


@app.get("/api/comment-likes")
def get_comment_likes():
    return likes.get_like('commentId', 'comment_likes', 'comment_id')

@app.post("/api/follows")
def post_follows():
    return likes.post_like("followId", "follows", "follow_user_id")

@app.delete("/api/follows")
def delete_follows():
    return likes.delete_like("followId", "follows", "follow_user_id")

@app.get("/api/follows")
def get_follows():
     return likes.get_follows('follow_user_id', 'user_id')

@app.get("/api/followers")
def get_followers():
    return likes.get_follows('user_id', 'follow_user_id')

if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

if(mode == "production"):
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5015)
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()





    # Get the user_id request.json to work so that if they input a number it brings back onne user


    # print(user_id)
    # get_id = isinstance(user_id, int)
    
    # if you set a variable like:

# username = request.json.get('username')

# if 'username' doesn't exist, it just returns none. 

# I also asked Alex this at the beginning of class though.... if 'username' is spelled wrong, technically it 'isn't there', so I was confused about what to do. he said that would be on the client with the select when they see their returned results are wrong
   

#    Another thing you can do is have the attitude:

# If I can't understand your userId, I will do the default of sending you back all users So if you hit an exception, continue assuming there was no userId

        # ASK ALEX: WHAT COMES BACK AS USER ID WHEN I SEND NOTHING> WHAT IS BEING SENT WHEN NOTHING IS SENT
