#! /usr/bin/python3

import os, cgi, sys, json, passwords, MySQLdb

def main():
    # CHECKS IF THEY TRY TO ACCESS SCRIPT DIRECTLY --> SENDS A REDIRECT WITH "/"" PATH
    if "PATH_INFO" not in os.environ:
        redirect_root()

    # IF PATH IS ONLY "/", SENDS A 403 FORBIDDEN WEBPAGE
    elif os.environ["PATH_INFO"] == "/":
        forbidden()

    # CHECKS IF PATH IS TRYING TO ACCESS PETS
    elif os.environ["PATH_INFO"].startswith("/pets"):
        pet_handler()

    # CHECKS IF PATH IS TRYING TO ACCESS PEOPLE
    elif os.environ["PATH_INFO"].startswith("/people"):
        people_handler()

    # ELSE NOT A VALID PATH SUPPORTED --> 404 NOT FOUND
    else:
        http_404()

def pet_handler():
    path = os.environ["PATH_INFO"]
    request_method = os.environ["REQUEST_METHOD"]

    if path == "/pets" or path == "/pets/":
        # RETURNS JSON OBJECT OF ALL PETS IN SQL DATABASE
        if request_method == "GET":
            http_json_ok()
            create_json_pets()

        # HANDLES A POST AND INSERTS NEW PET INTO DATABASE
        elif request_method == "POST":
            handle_pet_post()

        # ALL OTHER COMMANDS ARE NOT SUPPORTED
        else:
            method_not_allowed()

    else:
        # SPLITS OS PATH ALONG /
        split_path = path.split("/")

        # IF PATH IS LONGER THAN 3 TERMS, SEND A 404 NOT FOUND.
        if len(split_path) > 3:
            http_404()

        elif split_path[2].isnumeric():

            if request_method == "GET":
                pets_id(split_path)

            elif request_method == "PUT":
                update_pets(split_path)

            elif request_method == "DELETE":
                delete_pet_id()

            else:
                method_not_allowed()
        else:
            http_404()

# THIS METHOD CHECKS THE DIFFERENT REQUEST TYPES FOR PEOPLE URL BRANCH
# HAS GET, POST. IF SPECIFIC PERSON, IT HAS GET AND DELETE
def people_handler():
    path = os.environ["PATH_INFO"]
    request_method = os.environ["REQUEST_METHOD"]

    # CHECKS IF THE PATH ONLY IS REQUESTING PEOPLE
    if path == "/people" or path == "/people/":
        # RETURNS JSON OBJECT OF ALL PEOPLE IN SQL DATABASE
        if request_method == "GET":
            http_json_ok()
            create_json_people()

        # CALLS A METHOD TO INSERT A PERSON RECORD INTO THE DATABASE
        elif request_method == "POST":
            handle_people_post()

        # ELSE ANY OTHER METHOD IS NOT ALLOWED (LIKE DELETE, PUT, ETC.) 
        else:
            method_not_allowed()

    else:
        # SPLITS OS PATH ALONG /
        split_path = path.split("/")

        # IF PATH IS LONGER THAN 3 TERMS, SEND A 404 NOT FOUND.
        if len(split_path) > 3:
            http_404()

        # IF THE PATH IS AN ID THEN CONTINUE
        elif split_path[2].isnumeric():

            if request_method == "GET":
                people_id(split_path)
            
            elif request_method == "DELETE":
                delete_people_id(split_path)

            else:
                method_not_allowed()
        # ELSE SEND A 404
        else:
            http_404()

def update_pets(path):
    try:
        input_data = sys.stdin.read()
        python_input = json.loads(input_data)

        if type(python_input) is list:
            for dic in python_input:
                update_pet_record(path, dic)

            print("Status: 302 Redirect")
            print()

        elif type(python_input) is dict:
            update_pet_record(path, python_input)

            print("Status: 302 Redirect")
            print()

        else:
            bad_request()

    except:
        bad_request()

def update_pet_record(path, dic):
    pet_id = int(path[2])

    conn = connect_db()
    cursor = conn.cursor()

    keys = dic.keys()

    if "id" in keys:
        dic.pop("id")

    if "breed" in keys:
        dic.pop("breed")

    if "name" in keys:
        sql = "UPDATE pets SET name=%s WHERE id=%s;"
        vals = (dic["name"], pet_id)
        cursor.execute(sql, vals)

    if "weight" in keys:
        sql = "UPDATE pets SET weight=%s WHERE id=%s;"
        vals = (dic["weight"], pet_id)
        cursor.execute(sql, vals)

    if "age" in keys:
        sql = "UPDATE pets SET age=%s WHERE id=%s;"
        vals = (dic["age"], pet_id)
        cursor.execute(sql, vals)

    cursor.close()
    conn.commit()
    conn.close()


def delete_people_id(path):
    people_id = int(path[2])

    conn = connect_db()
    cursor = conn.cursor()

    sql_pet = "DELETE FROM pets WHERE owner_id = %s;"
    sql_person = "DELETE FROM people WHERE id=%s;"

    vals = (people_id,)

    cursor.execute(sql_pet, vals)
    cursor.execute(sql_person, vals)

    if cursor.rowcount == 0:
        http_404()
    else:   
        print("Status: 302 Redirect")
        print("Location: /cgi-bin/petcare/people/")
        print()

    cursor.close()
    conn.commit()
    conn.close()

def pets_id(path):
    pet_id = int(path[2])

    conn = connect_db()
    cursor = conn.cursor()

    sql = "SELECT * FROM pets WHERE id=%s"
    val = (pet_id,)

    cursor.execute(sql, val)
    response = cursor.fetchall()

    json_pet_id = []
    if response:
        http_json_ok()

        for record in response:
            owner_addr = "http://54.80.108.212/cgi-bin/people/" + str(record[0])
            entry = {
                "id": record[0],
                "name": record[1],
                "breed": record[2],
                "age": record[3],
                "weight": record[4],
                "owner_id": owner_addr
            }
            json_pet_id.append(entry)

        print(json.dumps(json_pet_id, indent=2))

    else:
        http_404()

# THIS METHOD DISPLAYS SPECIFIC PERSON ID AND THEIR PETS
def people_id(path):
    people_id = int(path[2])

    conn = connect_db()
    cursor = conn.cursor()

    # GETS THE INFORMATION FOR SPECIFIC PERSON
    sql = "SELECT * FROM people WHERE id=%s"
    val = (people_id,)

    cursor.execute(sql, val)
    response = cursor.fetchall()

    # GETS INFORMATION FOR ALL THE PETS THAT PERSON HAS
    pet_sql = "SELECT name FROM pets WHERE owner_id = %s;"
    cursor.execute(pet_sql, val)
    pet_results = cursor.fetchall()
    pets = []

    # GOES THROUGH AND ADDS EACH PET TO AN ARRAY
    if pet_results:
        for pet in pet_results:
            for name in pet:
                pets.append(name)


    json_people_id = []
    if response:
        # SENDS JSON RESPONSE AS OKAY
        http_json_ok()

        for record in response:
            unique_addr = "http://54.80.108.212/cgi-bin/people/" + str(record[0])
            entry = {
                "id": record[0],
                "first_name": record[1],
                "last_name": record[2],
                "age": record[3],
                "address": record[4],
                "link": unique_addr,
                "pets": pets
            }
            json_people_id.append(entry)

        print(json.dumps(json_people_id, indent=2))

    # IF THE ID DOES NOT EXIST, IT SENDS A 404 NOT FOUND
    else:
        http_404()

    cursor.close()
    conn.close()

def handle_pet_post():
    try:
        input_data = sys.stdin.read()
        python_input = json.loads(input_data)

        if type(python_input) is list:
            for dic in python_input:
                pet_post(dic)

            print("Status: 302 Redirect")
            print("Location: /cgi-bin/petcare/people/")
            print()

        elif type(python_input) is dict:
            pet_post(python_input)

            print("Status: 302 Redirect")
            print("Location: /cgi-bin/petcare/people/")
            print()

        else:
            bad_request()
    except:
        bad_request()

def handle_people_post():
    try:
        input_data = sys.stdin.read()
        python_input = json.loads(input_data)

        # CHECKS IF JSON HAS MULTIPLE RECORDS
        if type(python_input) is list:
            for dic in python_input:
                dict_post(dic)

            print("Status: 302 Redirect")
            print()

        # IF SINGLE RECORD, RUNS ONLY ONCE
        elif type(python_input) is dict:
            dict_post(python_input)

            print("Status: 302 Redirect")
            print()

        # IF ITS NOT A VALID JSON, IT THROWS A BAD REQUEST EERROR
        else:
            bad_request()

    # CATCHES ANY ERRORS OR ASSERTS FALSE. IF IT DOESNT RUN, IT THROWS 400 ERROR
    except:
        bad_request()

def pet_post(json_dict):
    conn = connect_db()
    cursor = conn.cursor()

    keys = json_dict.keys()
    if "id" in keys:
        json_dict.pop("id")

    if len(keys) < 4:
        assert False

    else:
        if "name" in keys and "age" in keys and "weight" in keys and "owner_id" in keys:
            if "breed" in keys:
                brd = json_dict["breed"]
            else: brd = "Unknown"

            sql = "INSERT INTO pets (name, breed, age, weight, owner_id) VALUES (%s, %s, %s, %s, %s);"

            vals = (json_dict["name"], brd, json_dict["age"], json_dict["weight"], json_dict["owner_id"])

            cursor.execute(sql, vals)

        else:
            assert False

    cursor.close()
    conn.commit()
    conn.close()

def dict_post(json_dict):
    conn = connect_db()
    cursor = conn.cursor()

    keys = json_dict.keys()
    if "id" in keys:
        json_dict.pop("id")

    if len(keys) < 3:
        assert False

    else:
        if "first_name" in keys and "last_name" in keys and "age" in keys:
            if "address" in keys:
                addr = json_dict["address"]
            else: addr = "None"

            sql = "INSERT INTO people (first_name, last_name, age, address) VALUES (%s, %s, %s, %s);"

            vals = (json_dict["first_name"], json_dict["last_name"], json_dict["age"], addr)

            cursor.execute(sql, vals)
        else:
            assert False

    cursor.close()
    conn.commit()
    conn.close()

# CREATES & PRINTS JSON OBJECT FOR ALL PEOPLE IN DATABASE 
def create_json_people():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM people")
    response = cursor.fetchall()

    json_people = []
    if response:
        for record in response:
            unique_addr = "http://54.80.108.212/cgi-bin/people/" + str(record[0])
            entry = {
                "id": record[0],
                "first_name": record[1],
                "last_name": record[2],
                "age": record[3],
                "address": record[4],
                "link": unique_addr
            }
            json_people.append(entry)
    else:
        json_people = []

    print(json.dumps(json_people, indent=2))

    cursor.close()
    conn.close()

# CREATES & PRINTS JSON OBJECT FOR ALL PETS IN DATABASE
def create_json_pets():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pets")
    response = cursor.fetchall()

    json_pets = []
    if response:
        for record in response:
            unique_addr = "http://54.80.108.212/cgi-bin/people/" + str(record[5])
            entry = {
                "id": record[0],
                "name": record[1],
                "breed": record[2],
                "age": record[3],
                "weight": record[4],
                "owner_id": unique_addr
            }
            json_pets.append(entry)
    else:
        json_pets = []

    print(json.dumps(json_pets, indent=2))

    cursor.close()
    conn.close()


# METHOD THAT CONNECTS TO THE SQL DATA BASE
def connect_db():
    conn = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWORD, db = "restbase")
    return conn

# SENDS JSON 200 OK HEADER
def http_json_ok():
    print("Content-Type: application/json")
    print("Status: 200 OK")
    print()

# SENDS HTML 200 OK HEADER
def http_200_ok():
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()

# SENDS A 404 NOT FOUND
def http_404():
    print("Status: 404 Not Found")
    print("Content-Type: text/html")
    print()
    print("""<html>
            <head>
                <title>404 Not Found</title>
            </head>
            <body>
                <h1>404 Not Found</h1>
                <p>The requested URL was not found on this server.</p>
            </body>
        </html>""")

# SENDS A 405 SAYING METHOD OPERATION NOT ALLOWED
def method_not_allowed():
    print("Status: 405 Method Not Allowed")
    print()

# SENDS A BAD REQUEST IF INPUT IS WRONG
def bad_request():
    print("Status: 400 Bad Request")
    print()

# REDIRECTS THE ROOT PAGE TO A "/" PATH
def redirect_root():
    print("Status: 302 Redirect")
    print("Location: /cgi-bin/petcare/")
    print()

# SENDS A FORBIDDEN FOR TRYING TO ACCESS A RESOURCE
def forbidden():
    print("Status: 403 Forbidden")
    print("Content-Type: text/html")
    print()
    print("""<html>
            <head>
                <title>403 Forbidden</title>
            </head>
            <body>
                <h1>Forbidden</h1>
                <p>You don't have permission to access this resource.</p>
            </body>
        </html>""")

if __name__ == '__main__':
    main()