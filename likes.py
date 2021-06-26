import mariadb
from flask import Flask, request, Response
from flask_cors.core import get_regexp_pattern
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
        return Response("liked successfully", mimetype="json/application", status=200)
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
        return Response("Deleted succesfully", mimetype="text/plain", status=200)
    elif(rows == 0):
        return Response("Unauthorized delete", mimetype="text/plain", status=400)
    else:
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)

def get_like(request_code, like_table, table_id):
    
    likes_list = []

    type_id = request.args.get(request_code)
    
    print(type_id)
    if(type_id != None and type_id != ""):
        likes_result = dbhelpers.run_select_statement(f"SELECT {like_table}.{table_id}, users.id, users.username FROM users INNER JOIN {like_table} ON users.id = {like_table}.user_id WHERE {like_table}.{table_id} = ?", [type_id]) 
    else:
        likes_result = dbhelpers.run_select_statement(f"SELECT {like_table}.{table_id}, users.id, users.username FROM users INNER JOIN {like_table} ON users.id = {like_table}.user_id", [])
        

    if(likes_result == [] or likes_result == None):
        return Response("DB Error, Sorry", mimetype="text/plain", status=500)
    else:
        for likes in likes_result:
        # user_results = [{'userId': user_result[i][0], 'email': user_result[0][1], 'username': user_result[0][2], 'bio': user_result[0][3], 'birtdate': user_result[0][4], 'image_url': user_result[0][5], 'bannerUrl': user_result[0][6]}]
            like_results = [{request_code: likes[0], 'userId': likes[1], 'username': likes[2]}]
            users_json = json.dumps(like_results, default=str)
            likes_list.append(users_json)
        return Response(likes_list, mimetype="application/json", status=201)