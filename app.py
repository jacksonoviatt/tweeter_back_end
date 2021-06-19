from flask import Flask, request, Response
import dbhelpers
import json
import traceback
import sys


app = Flask(__name__)


@app.post("/api/users")
def users_post():
    new_user_id = None
    image_url = None
    banner_url = None

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
    if(image_url == None and banner_url == None):
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate) VALUES (?,?,?,?,?)", [email, username, password, bio, birthdate])
     # if just image_url is an empty string, run an sql statement that inserts the other fields
    elif(image_url != None and banner_url == None):
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, image_url) VALUES (?,?,?,?,?,?)", [email, username, password, bio, birthdate, image_url])
    # if just banner_url is an empty string, run an sql statement that inserts the other fields
    elif(image_url == None and banner_url != None):
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, banner_url) VALUES (?,?,?,?,?,?)", [email, username, password, bio, birthdate, banner_url])
    else:
        new_user_id = dbhelpers.run_insert_statement("INSERT INTO users(email, username, password, bio, birthdate, image_url, banner_url) VALUES (?,?,?,?,?,?,?)", [email, username, password, bio, birthdate, image_url, banner_url])
   
   
    if(new_user_id == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:
        new_user = [{'userId': new_user_id, 'email': email, 'username': username, 'bio': bio, 'birtdate': birthdate, 'image_url': image_url, 'bannerUrl': banner_url}]
        new_user_json = json.dumps(new_user, default=str)
        return Response(new_user_json, mimetype="application/json", status=201)


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