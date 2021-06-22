import re
from flask import Flask, request, Response
from flask_cors.core import get_regexp_pattern
import dbhelpers
import json
import traceback
import sys
import secrets

app = Flask(__name__)


@app.post("/api/users")
def users_post():
    new_user_id = None
    image_url = ""
    banner_url = ""

    try:
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        bio = request.json['bio']
        birthdate = request.json['birthdate']
        image_url = request.json['imageUrl']
        banner_url = request.json['bannerUrl']
    except:
        # TODO better error catching
        traceback.print_exc()
        print("Error with the request")
        return Response("Data Error", mimetype="text/plain", status=400)
        
        # if image_url and banner_url are empty strings, run an sql statement that inserts the other fields

    if(image_url == "" and banner_url == ""):
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate) VALUES (?,?,?,?,?)", [email, username, password, bio, birthdate])
    # if just image_url is an empty string, run an sql statement that inserts the other fields
    elif(image_url != "" and banner_url == ""):
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, image_url) VALUES (?,?,?,?,?,?)", [email, username, password, bio, birthdate, image_url])
    # if just banner_url is an empty string, run an sql statement that inserts the other fields
    elif(image_url == "" and banner_url != ""):
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, banner_url) VALUES (?,?,?,?,?,?)", [email, username, password, bio, birthdate, banner_url])
    else:
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, image_url, banner_url) VALUES (?,?,?,?,?,?,?)", [email, username, password, bio, birthdate, image_url, banner_url])

        
    if(new_user_id == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:
        token = secrets.token_urlsafe(20)
        dbhelpers.run_insert_statement("INSERT INTO login(token, user_id) VALUES (?,?)", [token, new_user_id])
        new_user = [{'userId': new_user_id, 'loginToken': token, 'email': email, 'username': username, 'bio': bio, 'birtdate': birthdate, 'image_url': image_url, 'bannerUrl': banner_url}]
        new_user_json = json.dumps(new_user, default=str)
        return Response(new_user_json, mimetype="application/json", status=201)


@app.delete("/api/users")
def delete_user():
    try:
        login_token = request.json['loginToken']
        password = request.json['password']
        
    except:
        # TODO better error catching
        traceback.print_exc()
        print("Incorrect password or token")
        return Response("Data Error", mimetype="text/plain", status=400)


# TODO ask how to check this function. 
    rows = dbhelpers.run_delete_statement("DELETE login, users FROM login INNER JOIN users ON login.user_id = users.id WHERE login.token = ? AND users.password = ?", [login_token, password])

    # if(rows == 1):
    return Response(rows, mimetype="text/plain", status=200)
    # else:
    #     return Response("DB Error, Sorry!", mimetype="text/plain", status=500)

@app.get("/api/users")
def get_users():
    user_id = None
    user_result = None
    get_all = True
    users_list = []
    try:
        user_id = int(request.json['userId'])
        get_all = False
    except: 
        traceback.print_exc()
        
    if(get_all == True):
        user_result = dbhelpers.run_select_statement("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM users", [])
    elif(get_all == False):
        user_result = dbhelpers.run_select_statement("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM users WHERE id=?", [user_id])
     
    if(user_result == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:
        for user in user_result:
        # user_results = [{'userId': user_result[i][0], 'email': user_result[0][1], 'username': user_result[0][2], 'bio': user_result[0][3], 'birtdate': user_result[0][4], 'image_url': user_result[0][5], 'bannerUrl': user_result[0][6]}]
            user_results = [{'userId': user[0], 'email': user[1], 'username': user[2], 'bio': user[3], 'birtdate': user[4], 'image_url': user[5], 'bannerUrl': user[6]}]
            users_json = json.dumps(user_results, default=str)
            users_list.append(users_json)
        return Response(users_list, mimetype="application/json", status=201)

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