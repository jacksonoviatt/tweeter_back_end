import mariadb
from flask import Flask, request, Response
from flask_cors.core import get_regexp_pattern
import dbhelpers
import json
import traceback
import sys
import secrets





def post_tweet():
    image_url = ""
    # tweet_list = []

  
    try:
        image_url = request.json.get('imageUrl')
        content = request.json['content']
        token = request.json['loginToken']
    except:
        return Response("There was an issue with the data received.", mimetype="text/plain", status=400)
     
    try:   
        user_info = dbhelpers.get_user_info('token', token)
    except:
        return Response("That is not a valid token", mimetype="text/plain", status=400)


    if(image_url != "" and image_url != None):
        new_tweet_id = dbhelpers.run_insert_statement("INSERT INTO tweets(user_id, content, tweet_image) VALUES (?,?,?)", [user_info[0], content, image_url])
        # if just image_url is an empty string, run an sql statement that inserts the other fields
    else:
        new_tweet_id = dbhelpers.run_insert_statement("INSERT INTO tweets(user_id, content) VALUES (?,?)", [user_info[0], content])

    created_at = dbhelpers.run_select_statement("SELECT created_at FROM tweets WHERE id = ?", [new_tweet_id])
   
    if(new_tweet_id >= 1 and new_tweet_id != None):

        new_tweet = [{'tweetId': new_tweet_id, 'userId': user_info[0], 'username': user_info[2], 'userImageUrl': user_info[6], 'content': content, 'createdAt': created_at[0][0], 'imageUrl': image_url}]
        new_tweet_json = json.dumps(new_tweet, default=str)
        return Response(new_tweet_json, mimetype="json/application", status=200)
    else:
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)



def get_tweet():
    tweet_result = []
    tweet_list = []



    user_id = request.args.get('userId')
    
    print(user_id)
    if(user_id != None and user_id != ""):
        tweet_result = dbhelpers.run_select_statement("SELECT t.id, u.id, u.username, t.content, t.created_at, u.image_url, t.tweet_image FROM users AS u INNER JOIN tweets AS t ON u.id = t.user_id WHERE t.user_id = ?", [user_id]) 
    else:
        tweet_result = dbhelpers.run_select_statement("SELECT t.id, u.id, u.username, t.content, t.created_at, u.image_url, t.tweet_image FROM users AS u INNER JOIN tweets AS t ON u.id = t.user_id", [])
        
    if(tweet_result == [] or tweet_result == None):
        return Response("DB Error, Sorry", mimetype="text/plain", status=500)
    else:
        for tweet in tweet_result:
        # user_results = [{'userId': user_result[i][0], 'email': user_result[0][1], 'username': user_result[0][2], 'bio': user_result[0][3], 'birtdate': user_result[0][4], 'image_url': user_result[0][5], 'bannerUrl': user_result[0][6]}]
            tweet_results = [{'tweetId': tweet[0], 'userId': tweet[1], 'username': tweet[2], 'content': tweet[3], 'createdAt': tweet[4], 'userImageUrl': tweet[5], 'tweetImageUrl': tweet[6]}]
            users_json = json.dumps(tweet_results, default=str)
            tweet_list.append(users_json)
        return Response(tweet_list, mimetype="application/json", status=201)

def delete_tweet():
    try:
        login_token = request.json['loginToken']
        tweet_id = request.json['tweetId']
    except:
        return Response("Unauthorized data", mimetype="text/plain", status=400)



    rows = dbhelpers.run_delete_statement("DELETE tweets FROM tweets INNER JOIN login ON login.user_id = tweets.user_id WHERE login.token = ? AND tweets.id = ?", [login_token, tweet_id])

    if(rows == 1):
        return Response("Deleted succesfully", mimetype="text/plain", status=200)
    elif(rows == 0):
        return Response("Unauthorized delete", mimetype="text/plain", status=400)
    else:
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)






def patch_tweet():
    sql = 0
    user_id = [()]
    token = ""
    

    try:
        token = request.json['loginToken']
        tweet_id = request.json['tweetId']
        new_content = request.json['content']
    except:
        return Response("That is not a valid request, or something else is wrong", mimetype="text/plain", status=400)
       
 
    try:   
        user_info = dbhelpers.get_user_info('token', token)
    except:
        return Response("That is not a valid token", mimetype="text/plain", status=400)

    try:
        tweet_user = dbhelpers.run_select_statement("SELECT user_id FROM tweets WHERE id=?", [tweet_id])
    except:
        return Response("That is not a valid comment Id", mimetype="text/plain", status=400)    
    
    if(user_info[0] == tweet_user[0][0]):
           sql = dbhelpers.update_specific_column("tweets", "content", new_content, tweet_id, "id")
    else:
         return Response("Unauthourized edit", mimetype="text/plain", status=400)    
    

    if(sql == 1):
        return Response("The patch was succesful", mimetype="text/plain", status=201)
    elif(sql == 0):
        return Response("Unauthourized update", mimetype="text/plain", status=400)
    else:
        return Response("Database error, no updates were made", mimetype="text/plain", status=500)
