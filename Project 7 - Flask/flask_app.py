import os, cgi, sys, json, passwords, MySQLdb, random
from flask import Flask, request, render_template, url_for, redirect, make_response

app = Flask(__name__)

@app.route("/")
def root():
    # IF USER HAS NON-EXPIRED COOKIES --> GOES TO LOGGED IN VIEW
    if valid_cookie():
        uname = get_username()

        # INDEX 0 - UNAME; INDEX 1 - WRITTEN; INDEX 2 - JOINED
        user_data = user_info(uname)
        pub_blogs = get_pub_sav_blogs(uname, 1)
        saved_blogs = get_pub_sav_blogs(uname, 0)

        return render_template("logged_in.html", username=uname, joined=user_data[2], published=pub_blogs, saved=saved_blogs)

    # IF USER DOESNT HAVE EXISTING COOKIES
    else:
        return render_template("index.html")

@app.route("/setcookie", methods=["POST", "GET"])
def setcookie():
    # RETRIEVES USERNAME FROM LOGIN
    username = request.form["username"]
    if username:
        # IF USERNAME IS VALID, MAKES A SESSION ID FOR USER
        sessionID_int = random.randint(0, 16**64)
        sessionID = "%064x" % sessionID_int

        # TRYS AND INSERTS SESSION AND USER INTO SESSION TABLE
        try:
            insert_user(sessionID, username)
            add_user(username)

            resp = redirect("/flask_app")
            resp.set_cookie("sessionID", sessionID, max_age=60*60)

            return resp
        # IF IT FAILS, SENDS BACK TO INDEX PAGE
        except:
            return render_template("index.html")

    # IF NO USERNAME, SENDS BACK TO INDEX PAGE
    else:
        return render_template("index.html")

# LOGS USER OUT BY DELETING THEIR COOKIES
@app.route("/logout")
def logout():
    resp = redirect("/flask_app")
    resp.delete_cookie("sessionID")
    return resp

# SHOWS LIST OF ALL BLOGS POSTED FROM MOST RECENT TO LEAST
@app.route("/blogs_list")
def blogs_list():
    if valid_cookie():
        conn = connect_db()
        cursor = conn.cursor()

        get_blogs = "SELECT username, blog_title, blog_body, date_published FROM blogs WHERE published=1 ORDER BY date_published DESC;"

        cursor.execute(get_blogs)
        resp = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template("blogs_list.html", response=resp)
    else:
        return redirect("/flask_app")

# CREATES A LIST OF ALL USERS ALPHABETICALL
@app.route("/list_users")
def list_users():
    if valid_cookie():
        conn = connect_db()
        cursor = conn.cursor()

        get_users = "SELECT * FROM users ORDER BY username ASC;"

        cursor.execute(get_users)
        resp = cursor.fetchall()

        return render_template("list_users.html", response=resp)
    else:
        return redirect("/flask_app")

# ADDS USER BLOGS TO DATABASE THEN REDIRECTS TO SUCCESS PAGE
@app.route("/add_blog", methods=["POST"])
def add_blog():
    if valid_cookie():
        uname = get_username()
        b_title = request.form["blog_title"]
        b_body = request.form["blog_post"]

        if "POST" in request.form:
            r_method = 1
        elif "SAVE" in request.form:
            r_method = 0

        insert_blog(uname, b_title, b_body, r_method)

        return redirect("/flask_app/operation_successful")

    else:
        return redirect("/flask_app")

# VIEWS ALL USER'S SAVED BLOGS DESCENDING FROM RECENT TO LEAST
@app.route("/view_saved")
def view_saved():
    if valid_cookie():
        uname = get_username()

        conn = connect_db()
        cursor = conn.cursor()

        get_saved = "SELECT id, blog_title, blog_body, date_published FROM blogs WHERE username=%s AND published=0 ORDER BY date_published DESC;"
        vals = (uname,)

        cursor.execute(get_saved, vals)
        resp = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template("update_or_save.html", response=resp)

    else:
        return redirect("/flask_app")

# IF USER DECIDES TO UPDATE OR POST A SAVED BLOG IT WILL GET UPDATED AND SUBMITTED
@app.route("/update_or_post", methods=["POST"])
def update_or_post():
    if valid_cookie():
        blogID = request.form["blogID"]
        blog_body = request.form["blog_post"]

        if "POST" in request.form:
            r_method = 1
        elif "SAVE" in request.form:
            r_method = 0

        saved_blog_up_post(blogID, blog_body, r_method)

        return redirect("/flask_app/operation_successful")

    else:
        return redirect("/flask_app")

# UPDATES OR POSTS THE BLOG OF USERS
def saved_blog_up_post(blogID, blogBody, method):
    conn = connect_db()
    cursor = conn.cursor()

    sql = "UPDATE blogs SET date_published= NOW(), blog_body=%s, published=%s WHERE id=%s;"
    vals = (blogBody, method, blogID)

    cursor.execute(sql, vals)

    cursor.close()
    conn.commit()
    conn.close()

# INSERTS BLOG INTO THE DATABASE AND UPDATES BLOGS WRITTEN IN USERS
def insert_blog(uname, title, body, method):
    conn = connect_db()
    cursor = conn.cursor()

    add_blog = "INSERT INTO blogs (username, blog_title, blog_body, date_published, published) VALUES (%s, %s, %s, NOW(), %s);"
    vals = (uname, title, body, method)

    cursor.execute(add_blog, vals)
    cursor.close()
    conn.commit()
    conn.close()

    update_user_blog(uname)

# UPDATES USER INFORMATION ABOUT TOTAL WRITTEN BLOGS
def update_user_blog(username):
    user_data = user_info(username)
    curr_blogs = user_data[1]

    conn = connect_db()
    cursor = conn.cursor()

    update_blogs = "UPDATE users SET blogs_written=%s WHERE username=%s;"
    new_blogs = curr_blogs + 1
    vals = (new_blogs, username)

    cursor.execute(update_blogs, vals)

    cursor.close()
    conn.commit()
    conn.close()

# IF USER POSTS OR SAVES BLOG --> SENDS THEM TO A SUCCESS PAGE
@app.route("/operation_successful")
def blog_successful():
    return render_template("add_blog.html")

# GETS PUBLISHED OR SAVED BLOGS OF THE USER
def get_pub_sav_blogs(username, is_published):
    conn = connect_db()
    cursor = conn.cursor()

    get_user_saved = "SELECT published FROM blogs WHERE username = %s AND published = %s;"
    vals = (username, is_published)

    cursor.execute(get_user_saved, vals)
    response = cursor.fetchall()

    if response:
        return len(response)
    else:
        return 0

    cursor.close()
    conn.close()

# GETS A USERS INFORMATION
# GETS USERNAME, # BLOGS WRITTEN, AND DATE JOINED
def user_info(username):
    conn = connect_db()
    cursor = conn.cursor()

    get_join_date = "SELECT username, blogs_written, joined FROM users WHERE username = %s;"
    vals = (username,)

    cursor.execute(get_join_date, vals)
    response = cursor.fetchall()

    return response[0]


# METHOD TO CHECK IF THE USER HAS A VALID COOKIE
def valid_cookie():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # IF COOKIE NAME VALID, CONTINUES TO TEST SESSION ID
        sessionID = request.cookies.get("sessionID")

        valid_session = "SELECT username FROM session WHERE sessionID = %s;"
        vals = (sessionID,)

        cursor.execute(valid_session, vals)
        response = cursor.fetchall()

        # IF RESPOSNE IS NONE, SENDS USER BACK TO INDEX PAGE
        if response:
            return True
        else:
            return False

    # COOKIE NAME IS INVALID, DELETES OLD COOKIE AND SENDS BACK TO INDEX PAGE
    except:
        resp = redirect("/flask_app")
        resp.set_cookie("invalid", "invalid", max_age=0)

        return resp

# GETS USERNAME FROM SESSIONID FROM COOKIE IN BROWSER
# BECAUSE OF VALID_COOKIE() METHOD, CAN ASSUME THIS WILL NOT FAIL
def get_username():
    conn = connect_db()
    cursor = conn.cursor()

    # GETS SESSION ID FROM COOKIE
    sessionID = request.cookies.get("sessionID")

    # FINDS USERNAME THAT MATCHES SESSIONID
    find_username = "SELECT username FROM session WHERE sessionID = %s;"
    vals = (sessionID,)

    cursor.execute(find_username, vals)
    response = cursor.fetchall()

    return response[0][0]

# METHOD THAT INSERTS A USERNAME AND SESSION ID
def insert_user(sessionID, username):
    conn = connect_db()
    cursor = conn.cursor()

    add_user = "INSERT INTO session (sessionID, username) VALUES (%s, %s);"
    vals = (sessionID, username)

    cursor.execute(add_user, vals)

    cursor.close()
    conn.commit()
    conn.close()

# INSERTS A NEW USER INTO THE USERS TABLE
def add_user(username):
    conn = connect_db()
    cursor = conn.cursor()

    does_exist = "SELECT * FROM users WHERE username = %s;"
    vals = (username,)

    cursor.execute(does_exist, vals)
    response = cursor.fetchall()

    # IF RESPONSE IS EMPTY, IT ADDS THE NEW USER TO THE DATABASE
    if not response:
        add = "INSERT INTO users (username, blogs_written, joined) VALUES (%s, %s, NOW());"
        user_vals = (username, 0)

        cursor.execute(add, user_vals)

    cursor.close()
    conn.commit()
    conn.close()

# METHOD TO CONNECT TO DATABASE
def connect_db():
    conn = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWORD, db = "flaskbase")
    return conn