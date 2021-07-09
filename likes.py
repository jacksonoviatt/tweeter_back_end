import mariadb
from flask import Flask, request, Response
from flask_cors.core import get_regexp_pattern
from werkzeug.wrappers import response
import dbhelpers
import json
import traceback
import sys
import secrets

def post_like(request_code, like_table, table_id):
    try:
        token = request.json['loginToken']
        type_id = request.json[request_code]
    except:
        return Response("There was an issue with the data received.", mimetype="text/plain", status=400)
    try:
        user_info = dbhelpers.get_user_info('token', token)
    except:
        return Response("That is not a valid token", mimetype="text/plain", status=400)
    
    try:
        like_id = dbhelpers.run_insert_statement(f"INSERT INTO {like_table}(user_id, {table_id}) VALUES (?, ?)", [user_info[0], type_id])
    except:
        return Response("Unauthorized Like", mimetype="text/plain", status=400)

    if(like_id != None and like_id >= 1):
        return Response("Successfully posted!", mimetype="json/application", status=200)
    else:
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)

def delete_like(request_code, like_table, table_id):
    try:
        token = request.json['loginToken']
        type_id = request.json[request_code]
    except:
        return Response("There was an issue with the data received.", mimetype="text/plain", status=400)
   
    try:
        user_info = dbhelpers.get_user_info('token', token)
    except:
        return Response("That is not a valid token", mimetype="text/plain", status=400)
    
    rows = dbhelpers.run_delete_statement(f'DELETE {like_table} FROM {like_table} WHERE user_id = ? AND {table_id} = ?', [user_info[0], type_id])

    if(rows == 1):
        return Response("Successfully deleted!", mimetype="text/plain", status=200)
    elif(rows == 0):
        return Response("Unauthorized delete", mimetype="text/plain", status=400)
    else:
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)

def get_like(request_code, like_table, table_id):
    
    like_results = []
    likes_list = []

    type_id = request.args.get(request_code)
    

    if(type_id != None and type_id != ""):
        likes_result = dbhelpers.run_select_statement(f"SELECT {like_table}.{table_id}, users.id, users.username, users.email, users.bio, users.birthdate, users.image_url, users.banner_url FROM users INNER JOIN {like_table} ON users.id = {like_table}.user_id WHERE {like_table}.{table_id} = ?", [type_id]) 
    else:
        likes_result = dbhelpers.run_select_statement(f"SELECT {like_table}.{table_id}, users.id, users.username, users.email, users.bio, users.birthdate, users.image_url, users.banner_url FROM users INNER JOIN {like_table} ON users.id = {like_table}.user_id", [])
        

    if(likes_result == None):
        return Response("DB Error, Sorry", mimetype="text/plain", status=500)
    else:
        for likes in likes_result:
            like_results = {request_code: likes[0], 'userId': likes[1], 'username': likes[2]}
            likes_list.append(like_results)
        users_json = json.dumps(likes_list, default=str)
        return Response(users_json, mimetype="application/json", status=201)



# get follows and get followers are the same, aside from two columns
def get_follows(column1, column2):
    follows_list = []
    try:
        # get the user_id of the user we are trying to 
        user_id = request.args["userId"]
    except:
        traceback.print_exc()
        return Response("Invalid Data", mimetype="text/plain", status=400)

    # this is an inner join of the users table and the follows table
    # dependent on the funstion args, it will either get the users who's userId line up with the follows or the followers of the userID provided
    follow_user_info = dbhelpers.run_select_statement(
        f"SELECT users.id, users.email, users.username, users.bio, users.birthdate, users.image_url, users.banner_url FROM users INNER JOIN follows ON follows.{column1} = users.id WHERE follows.{column2} = ?",
        [user_id])

    if(follow_user_info == None):
        return Response("DB Error, Sorry", mimetype="text/plain", status=500)
    else:
        # send back the json follows info
        for follow in follow_user_info:
            follow_results = {'userId': follow[0], 'email': follow[1], 'username': follow[2], 'bio': follow[3], 'birthdate': follow[4], 'imageUrl': follow[5], 'bannerUrl': follow[6]}
            follows_list.append(follow_results)
        users_json = json.dumps(follows_list, default=str)
        return Response(users_json, mimetype="application/json", status=201)

