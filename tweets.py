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

    created_at = dbhelpers.run_select_statement("SELECT created_at FROM tweets", [])
   
    if(new_tweet_id >= 1 and new_tweet_id != None):

        new_tweet = [{'tweetId': new_tweet_id, 'userId': user_info[0], 'username': user_info[2], 'userImageUrl': user_info[6], 'content': content, 'createdAt': created_at[0][0], 'imageUrl': image_url}]
        new_tweet_json = json.dumps(new_tweet, default=str)
        return Response(new_tweet_json, mimetype="json/application", status=200)
    else:
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)



def get_tweet():
    tweet_result = []
    tweet_list = []



    user_id = request.json.get('userId')
    
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
