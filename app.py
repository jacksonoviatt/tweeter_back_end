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

app = Flask(__name__)


@app.post("/api/users")
def users_post():
    return users.post_user()




@app.delete("/api/users")
def users_delete():
    return users.delete_user()

@app.get("/api/users")
def get_users():
    user_result = []
    get_all = True
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

@app.patch("/api/users")
def patch_users():
    sql = 0
    user_id = [()]
    token = ""

    try:
        token = request.json['loginToken']
        new_email = request.json.get('email')
        new_username = request.json.get('username')
        new_bio = request.json.get('bio')
        new_birthdate = request.json.get('birthdate')
        new_image = request.json.get('imageUrl')
        new_banner = request.json.get('bannerUrl')
    except:
        return Response("That is not a valid request, or something else is wrong", mimetype="text/plain", status=400)
    try:   
        user_id = dbhelpers.run_select_statement('SELECT users.id FROM users INNER JOIN login ON login.user_id = users.id WHERE login.token = ?', [token])
    except:
        return Response("That is not a valid token", mimetype="text/plain", status=400)

    print(user_id)
    if(user_id == [()]):    
        return Response("That is not a valid token", mimetype="text/plain", status=400)
    elif(user_id[0][0] != 0):
        if(new_email != "" and new_email != None):
            sql = dbhelpers.update_specific_column("users", "email", new_email, user_id[0][0], "id")
        elif(new_username != "" and new_username != None):
            sql = dbhelpers.update_specific_column("users", "username", new_username, user_id[0][0], "id")
        elif(new_bio != "" and new_bio != None):
            sql = dbhelpers.update_specific_column("users", "bio", new_bio, user_id[0][0], "id")
        elif(new_birthdate != "" and new_birthdate != None):
            sql = dbhelpers.update_specific_column("users", "birthdate", new_birthdate, user_id[0][0], "id")
        elif(new_image != "" and new_image != None):
            sql = dbhelpers.update_specific_column("users", "image_url", new_image, user_id[0][0], "id")
        elif(new_banner != "" and new_banner != None):
            sql = dbhelpers.update_specific_column("users", "banner_url", new_banner, user_id[0][0], "id")

    
    if(sql == 1):
        return Response("The patch was succesful", mimetype="text/plain", status=201)
    elif(sql == 0):
         return Response("Unauthorized update", mimetype="text/plain", status=400)
    else:
        return Response("Database error, no updates were made", mimetype="text/plain", status=500)


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
