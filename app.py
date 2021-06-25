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
