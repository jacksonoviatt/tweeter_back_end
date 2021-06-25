import mariadb
from flask import Flask, request, Response
from flask_cors.core import get_regexp_pattern
import dbhelpers
import json
import traceback
import sys
import secrets
from email.utils import parseaddr

def post_user():
    new_user_id = None
    image_url = ""
    banner_url = ""

  
        
    
    try:
        # QUESTION: should this be in a try except??
        # parseaddr gives ("", "email")
        email = parseaddr(request.json['email'])
 
        # check that the email has the proper symbols
        if '@' and '.' not in email[1]:
            return Response("Please enter a valid email", mimetype="text/plain", status=400)
        username = request.json['username']
        password = request.json['password']
        bio = request.json['bio']
        try:
            birthdate = request.json['birthdate']
        except:
            return Response("There was a data error. Please ensure the birthdate is in the 'yyyy-mm-dd format'", mimetype="text/plain", status=400)
        image_url = request.json['imageUrl']
        banner_url = request.json['bannerUrl']
    except:
        # TODO better error catching
        traceback.print_exc()
        
        return Response("Receiving Data Error", mimetype="text/plain", status=400)

    # try:
    # if()
        # if image_url and banner_url are empty strings, run an sql statement that inserts the other fields

    if(image_url == "" and banner_url == ""):
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate) VALUES (?,?,?,?,?)", [email[1], username, password, bio, birthdate])
        # if just image_url is an empty string, run an sql statement that inserts the other fields
    elif(image_url != "" and banner_url == ""):
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, image_url) VALUES (?,?,?,?,?,?)", [email[1], username, password, bio, birthdate, image_url])
        # if just banner_url is an empty string, run an sql statement that inserts the other fields
    elif(image_url == "" and banner_url != ""):
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, banner_url) VALUES (?,?,?,?,?,?)", [email[1], username, password, bio, birthdate, banner_url])
    else:
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, image_url, banner_url) VALUES (?,?,?,?,?,?,?)", [email[1], username, password, bio, birthdate, image_url, banner_url])
    # except mariadb.IntegrityError:
    #     return traceback.print_exc()
    # except mariadb.OperationalError:
    #     result = mariadb.OperationalError
    #     return Response(result, mimetype="text/plain", status=400)
        

    if(new_user_id == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:
        token = secrets.token_urlsafe(20)
        dbhelpers.run_insert_statement("INSERT INTO login(token, user_id) VALUES (?,?)", [token, new_user_id])
        new_user = [{'userId': new_user_id, 'loginToken': token, 'email': email[1], 'username': username, 'bio': bio, 'birtdate': birthdate, 'image_url': image_url, 'bannerUrl': banner_url}]
        new_user_json = json.dumps(new_user, default=str)
        return Response(new_user_json, mimetype="application/json", status=201)


def delete_user():
    try:
        login_token = request.json['loginToken']
        password = request.json['password']
        
    except:
        traceback.print_exc()
        print("Incorrect password or token")
        return Response("Data Error", mimetype="text/plain", status=400)



    rows = dbhelpers.run_delete_statement("DELETE login, users FROM login INNER JOIN users ON login.user_id = users.id WHERE login.token = ? AND users.password = ?", [login_token, password])

    if(rows == 2):
        return Response("Deleted succesfully", mimetype="text/plain", status=200)
    elif(rows == 0):
        return Response("Unauthorized delete", mimetype="text/plain", status=400)
    else:
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)


def get_users():
    user_result = []
    users_list = []

    # if the user_id is not an 

    user_id = request.args.get('userId')

    if(user_id != None and user_id != "" ):
        user_result = dbhelpers.run_select_statement("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM users WHERE id=?", [user_id])
    else:
        user_result = dbhelpers.run_select_statement("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM users", [])
        
    if(user_result == [] or user_result == None):
        return Response("DB Error, Sorry", mimetype="text/plain", status=500)
    else:
        for user in user_result:
        # user_results = [{'userId': user_result[i][0], 'email': user_result[0][1], 'username': user_result[0][2], 'bio': user_result[0][3], 'birtdate': user_result[0][4], 'image_url': user_result[0][5], 'bannerUrl': user_result[0][6]}]
            user_results = [{'userId': user[0], 'email': user[1], 'username': user[2], 'bio': user[3], 'birtdate': user[4], 'image_url': user[5], 'bannerUrl': user[6]}]
            users_json = json.dumps(user_results, default=str)
            users_list.append(users_json)
        return Response(users_list, mimetype="application/json", status=201)
