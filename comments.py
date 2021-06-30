from re import DEBUG
import mariadb
from flask import Flask, request, Response
from flask_cors.core import get_regexp_pattern
import dbhelpers
import json
import traceback
import sys
import secrets





def post_comment():
    try:
        content = request.json['content']
        tweet_id = request.json['tweetId']
        token = request.json['loginToken']
    except:
        return Response("There was an issue with the data received.", mimetype="text/plain", status=400)
     
    try:   
        user_info = dbhelpers.get_user_info('token', token)
    except:
        return Response("That is not a valid token", mimetype="text/plain", status=400)
    new_comment_id = dbhelpers.run_insert_statement("INSERT INTO comments(user_id, tweet_id, content) VALUES (?,?,?)", [user_info[0], tweet_id, content])
    
    created_at = dbhelpers.run_select_statement("SELECT created_at FROM comments WHERE id = ?", [new_comment_id])
    if(new_comment_id != None and new_comment_id >= 1):

        new_comment = {'commentId': new_comment_id, 'tweetId': tweet_id, 'userId': user_info[0], 'username': user_info[2], 'content': content, 'createdAt': created_at[0][0]}
        new_comment_json = json.dumps(new_comment, default=str)
        return Response(new_comment_json, mimetype="json/application", status=200)
    else:
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)





def get_comment():
    comment_result = []
    comment_list = []

    tweet_id = request.args.get('tweetId')
    
    print(tweet_id)
    if(tweet_id != None and tweet_id != ""):
        comment_result = dbhelpers.run_select_statement("SELECT c.id, c.tweet_id, u.id, u.username, c.content, c.created_at FROM users AS u INNER JOIN comments AS c ON u.id = c.user_id WHERE c.tweet_id = ?", [tweet_id]) 
    else:
        comment_result = dbhelpers.run_select_statement("SELECT c.id, c.tweet_id, u.id, u.username, c.content, c.created_at FROM users AS u INNER JOIN comments AS c ON u.id = c.user_id", [])
        
    if(comment_result == None):
        return Response("DB Error, Sorry", mimetype="text/plain", status=500)
    else:
        for comment in comment_result:
        # user_results = [{'userId': user_result[i][0], 'email': user_result[0][1], 'username': user_result[0][2], 'bio': user_result[0][3], 'birtdate': user_result[0][4], 'image_url': user_result[0][5], 'bannerUrl': user_result[0][6]}]
            comment_results = {'commentId': comment[0], 'tweetId': comment[1], 'userId': comment[2], 'username': comment[3], 'content': comment[4], 'createdAt': comment[5]}
           
            
            comment_list.append(comment_results)
        users_json = json.dumps(comment_list, default=str)

        return Response(users_json, mimetype="application/json", status=201)


def delete_comment():
    try:
        login_token = request.json['loginToken']
        comment_id = request.json['commentId']
    except:
        return Response("Unauthorized data", mimetype="text/plain", status=400)

    rows = dbhelpers.run_delete_statement("DELETE comments FROM comments INNER JOIN login ON login.user_id = comments.user_id WHERE login.token = ? AND comments.id = ?", [login_token, comment_id])

    if(rows == 1):
        return Response("Deleted succesfully", mimetype="text/plain", status=200)
    elif(rows == 0):
        return Response("Unauthorized delete", mimetype="text/plain", status=400)
    else:
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)






def patch_comment():
    sql = 0
    token = ""
    

    try:
        token = request.json['loginToken']
        comment_id = request.json['commentId']
        new_content = request.json['content']
    except:
        return Response("That is not a valid request, or something else is wrong", mimetype="text/plain", status=400)
    
    try:   
        user_info = dbhelpers.get_user_info('token', token)
    except:
        return Response("That is not a valid token", mimetype="text/plain", status=400)

    try:
        comment_user = dbhelpers.run_select_statement("SELECT user_id FROM comments WHERE id=?", [comment_id])
    except:
        return Response("That is not a valid comment Id", mimetype="text/plain", status=400)    
    
    if(user_info[0] == comment_user[0][0]):
        sql = dbhelpers.update_specific_column("comments", "content", new_content, comment_id, "id")
    else:
         return Response("Unauthourized edit", mimetype="text/plain", status=400)    
    

    if(sql == 1):
        return Response("The patch was succesful", mimetype="text/plain", status=201)
    elif(sql == 0):
        return Response("Unauthorized update", mimetype="text/plain", status=400)
    else:
        return Response("Database error, no updates were made", mimetype="text/plain", status=500)
