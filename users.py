import mariadb
from flask import Flask, request, Response
from flask_cors.core import get_regexp_pattern
import dbhelpers
import json
import traceback
import sys
import secrets
from email.utils import parseaddr
import hashlib

def get_salt_from_db(username):
    user = dbhelpers.run_select_statement("SELECT salt FROM users WHERE username = ?", [username])
    if(len(user) == 1):
        return user[0][0]
    else:
        return "error"

def get_salt_from_db_token(token):
    user = dbhelpers.run_select_statement("SELECT salt FROM users INNER JOIN login ON users.id = login.user_id WHERE login.token = ?", [token])
    if(len(user) == 1):
        return user[0][0]
    else:
        return "error"

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
        salt = dbhelpers.create_salt()
        password = salt + password
        password = hashlib.sha512(password.encode()).hexdigest()
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
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, salt) VALUES (?,?,?,?,?,?)", [email[1], username, password, bio, birthdate, salt])
        # if just image_url is an empty string, run an sql statement that inserts the other fields
    elif(image_url != "" and banner_url == ""):
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, image_url, salt) VALUES (?,?,?,?,?,?,?)", [email[1], username, password, bio, birthdate, image_url, salt])
        # if just banner_url is an empty string, run an sql statement that inserts the other fields
    elif(image_url == "" and banner_url != ""):
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, banner_url, salt) VALUES (?,?,?,?,?,?,?)", [email[1], username, password, bio, birthdate, banner_url, salt])
    else:
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, image_url, banner_url, salt) VALUES (?,?,?,?,?,?,?,?)", [email[1], username, password, bio, birthdate, image_url, banner_url, salt])

    if(new_user_id == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:
        token = secrets.token_urlsafe(20)
        dbhelpers.run_insert_statement("INSERT INTO login(token, user_id) VALUES (?,?)", [token, new_user_id])
        new_user = {'userId': new_user_id, 'loginToken': token, 'email': email[1], 'username': username, 'bio': bio, 'birthdate': birthdate, 'imageUrl': image_url, 'bannerUrl': banner_url}
        new_user_json = json.dumps(new_user, default=str)
        return Response(new_user_json, mimetype="application/json", status=201)


def delete_user():
    try:
        login_token = request.json['loginToken']
        password = request.json['password']
        salt = get_salt_from_db_token(login_token)
        password = salt + password
        password = hashlib.sha512(password.encode()).hexdigest()
        print(password)
    except:
        traceback.print_exc()
        print("Incorrect password or token")
        return Response("Data Error", mimetype="text/plain", status=400)



    rows = dbhelpers.run_delete_statement("DELETE users FROM login INNER JOIN users ON login.user_id = users.id WHERE login.token = ? AND users.password = ?", [login_token, password])

    if(rows >= 1):
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
        
    if(user_result == None):
        return Response("DB Error, Sorry", mimetype="text/plain", status=500)
    else:
        for user in user_result:
        # user_results = [{'userId': user_result[i][0], 'email': user_result[0][1], 'username': user_result[0][2], 'bio': user_result[0][3], 'birtdate': user_result[0][4], 'image_url': user_result[0][5], 'bannerUrl': user_result[0][6]}]
            user_results = {'userId': user[0], 'email': user[1], 'username': user[2], 'bio': user[3], 'birthdate': user[4], 'imageUrl': user[5], 'bannerUrl': user[6]}
            users_list.append(user_results)
        users_json = json.dumps(users_list, default=str)
            
        return Response(users_json, mimetype="application/json", status=201)


# My patch users is slightly different than the original tweeter docs. 
# I included the login token in the json response so that the front-end 
# can easily replace the entire user_info cookie 


def patch_users():
    user_id = [()]
    token = ""
    
# The user will provide me with the data they want to update
    try:
        # the login token is not optional
        token = request.json['loginToken']
        # These are all optional
        new_email = request.json.get('email')
        new_username = request.json.get('username')
        new_password = request.json.get('password')
        new_bio = request.json.get('bio')
        new_birthdate = request.json.get('birthdate')
        new_image = request.json.get('imageUrl')
        new_banner = request.json.get('bannerUrl')
    except:
        return Response("That is not a valid request, or something else is wrong", mimetype="text/plain", status=400)
    
    # Get the users information using my helper function

    # def get_user_info(column, token):
    # user_info = run_select_statement(f"SELECT u.id, u.email, u.username, u.password, u.bio, u.birthdate, u.image_url, u.banner_url FROM users AS u INNER JOIN login AS l ON l.user_id = u.id WHERE l.{column} = ?", [token, ])
    # return user_info[0]

    try:   
        user_info = dbhelpers.get_user_info('token', token)
        user_id = user_info[0]
    except:
        return Response("That is not a valid token", mimetype="text/plain", status=400)

    # if the user_id is valid, move on to the next condtional statements
    if(user_id != 0 and user_id != None):
        
        # If the user sends back an empty string or something goes wrong we don't want to update the database
        
        if(new_email != "" and new_email != None):
            
            #  def update_specific_column(table, column, new_data, user_id, key):
                # this is specific to the users table,
                # sql = run_update_statement(f"UPDATE {table} SET {column}=? WHERE {key}=?", [new_data, user_id])
                # return sql  
            sql = dbhelpers.update_specific_column("users", "email", new_email, user_id, "id")
        
        elif(new_username != "" and new_username != None):
            sql = dbhelpers.update_specific_column("users", "username", new_username, user_id, "id")

    # This one is a bit different because you have to add salt to the password
    # and store it securely
        elif(new_password != "" and new_password != None):
            salt = dbhelpers.create_salt()
            sql = dbhelpers.update_specific_column("users", "salt", salt, user_id, "id")
            new_password = salt + new_password
            new_password = hashlib.sha512(new_password.encode()).hexdigest()
            sql = dbhelpers.update_specific_column("users", "password", new_password, user_id, "id")
       
        elif(new_bio != "" and new_bio != None):
            sql = dbhelpers.update_specific_column("users", "bio", new_bio, user_id, "id")
            
        elif(new_birthdate != "" and new_birthdate != None):
            sql = dbhelpers.update_specific_column("users", "birthdate", new_birthdate, user_id, "id")
         
        elif(new_image != "" and new_image != None):
            sql = dbhelpers.update_specific_column("users", "image_url", new_image, user_id, "id")
            
        elif(new_banner != "" and new_banner != None):
            sql = dbhelpers.update_specific_column("users", "banner_url", new_banner, user_id, "id")
        
        # If the user sends back all empty strings the endpoint will respond with the original information
        elif(new_email == "" and new_username == "" and new_bio == "" and new_birthdate == "" and new_image == "" and new_banner == ""):
            new_user = {'userId': user_id, 'loginToken': token, 'email': user_info[1], 'username': user_info[2], 'bio': user_info[4], 'birthdate': user_info[5], 'imageUrl': user_info[6], 'bannerUrl': user_info[7]}
            user_json = json.dumps(new_user, default=str)
            return Response(user_json, mimetype="application/json", status=201)

# If sql == None then the it failed
    if(sql == None):
        return Response("Database error, no updates were made", mimetype="text/plain", status=500)
    else:
        # get the users update information from the database and send this back to the user
        user_info = dbhelpers.get_user_info('token', token)
        new_user = {'userId': user_id, 'loginToken': token, 'email': user_info[1], 'username': user_info[2], 'bio': user_info[4], 'birthdate': user_info[5], 'imageUrl': user_info[6], 'bannerUrl': user_info[7]}
        new_user_json = json.dumps(new_user, default=str)
        return Response(new_user_json, mimetype="application/json", status=201)
    


def post_login():
    try:
        username = request.json["username"]
        password = request.json["password"]
        salt = get_salt_from_db(username)
        password = salt + password
        password = hashlib.sha512(password.encode()).hexdigest()
    except:
        traceback.print_exc()
        return Response("Incorrect username or password", mimetype="text/plain", status=400)
    
    if(username == "" or password == ""):
        return Response("Enter your username and password", mimetype="text/plain", status=400)
    
    user_results = dbhelpers.run_select_statement("SELECT id, email, username, bio, birthdate, image_url, banner_url FROM users WHERE username = ? AND password = ?", [username, password])
    
    token = secrets.token_urlsafe(20)
    login_id = dbhelpers.run_insert_statement("INSERT INTO login(user_id, token) VALUES (?, ?)", [user_results[0][0], token])
    
    user_results = {'userId': user_results[0][0], 'email': user_results[0][1], 'loginToken': token, 'username': user_results[0][2],'bio': user_results[0][3], 'birthdate': user_results[0][4], 'imageUrl': user_results[0][5], 'bannerUrl': user_results[0][6]}
    user_json = json.dumps(user_results, default=str)

    if (login_id != 0 and login_id != None):
        return Response(user_json, mimetype="json/application", status=200)
    else:
        return Response("failure", mimetype="text/plain", status=500)


def delete_login():
    # request the login token
    try:
        login_token = request.json['loginToken']
        
    except:
        traceback.print_exc()
        print("Unauthorized data")
        return Response("Data Error", mimetype="text/plain", status=400)


    # Delete the login row that corresponds with the provided token, this verifys the log out
    rows = dbhelpers.run_delete_statement("DELETE login FROM login WHERE token = ?", [login_token])

# if successful, tell the user it was succesful
    if(rows == 1):
        return Response("Logout succesful", mimetype="text/plain", status=200)
    elif(rows == 0):
        return Response("Unauthorized logout", mimetype="text/plain", status=400)
    else:
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)

