#! /usr/bin/python3

import MySQLdb, passwords, os, sys, cgi, datetime

def main():
    # REDIRECTS PATH TO /WEBHOOKS/
    if "PATH_INFO" not in os.environ:
        print("Status: 302 Redirect")
        print("Location: /cgi-bin/webhooks/")
        print()

    else:
        # FINDS PATH AND REQUEST METHOD
        path = os.environ["PATH_INFO"]
        request_method = os.environ["REQUEST_METHOD"]

        # IF THE PATH IS JUST THE SCRIPT NAME with /, SEND FORBIDDEN (NOT ALLOWED TO ACCESS SCRIPT DIRECTLY)
        if path == "/":
            http_403()

        # POST PATH ONLY SUPPORTS POST METHOD
        elif path == "/post" or path == "/post/":
            if request_method == "POST":
                post_handler()

            # IF USER TRYS ANY OTHER METHOD, SENDS A 405 METHOD NOT ALLOWED
            else: http_405()

        # GET PATH ONLY SUPPORTS GET METHOD
        elif path == "/get" or path == "/get/":
            if request_method == "GET":
                get_handler()

            # IF USER TRY POST OR ANY OTHER METHOD, SENDS A 405 METHOD NOT ALLOWED
            else: http_405()

        # IF USER TRYS ANY OTHER PATH URL, IT SENDS A 404 NOT FOUND
        else:
            http_404()

# METHOD THAT HANDLES GET REQUESTS. DISPLAYS REQUEST IN ORDER OF MOST RECENT (TOP) TO LEAST (BOTTOM)
def get_handler():
    conn = connect_db()
    cursor = conn.cursor()

    get_sql = "SELECT * FROM requests ORDER BY request_time;"
    cursor.execute(get_sql)

    response = cursor.fetchall()

    # IF IT WORKS, SENDS A 200 OK MESSAGE
    http_200()

    if response:
        for record in response:
            time = record[-1]
            data = record[1]

            print("""<div style="border: 2px solid black">""")
            print("""<tr><td>TIME REQUESTED: {0}</td>
            <td><div><pre style="white-space: pre-wrap; word-wrap: break-word;">{1}</pre></div></td></tr>""".format(time,data))
            print("</div>")


    cursor.close()
    conn.close()

# METHOD THAT HANDLES THE POST REQUEST TO DB
def post_handler():
    conn = connect_db()
    cursor = conn.cursor()

    # READS RAW INPUT AND INSERTS IT INTO THE DATABASE WITH A TIMESTAMP
    try:
        sys_input = input_data = sys.stdin.read()
        post_sql = "INSERT INTO requests(request_data, request_time) VALUES(%s, NOW());"
        vals = (sys_input,)

        cursor.execute(post_sql, vals)

        # CHECKS IF THE REQUEST AMOUNT OVERFLOWED, IF SO DELETES OLDEST REQUST
        check_for_overflow(cursor)

        # SUCCESSFULLY EXECUTED, NOW COMMITS CHANGES AND CLOSES CONN
        http_302()
        cursor.close()
        conn.commit()
        conn.close()

    except:
        http_404()

# CHECKS TO SEE IF # OF REQUESTS EXCEED MAX ALLOWED. IF SO DELETS OLDEST REQUEST
def check_for_overflow(cursor):
    time_data = "SELECT id FROM requests ORDER BY request_time;"

    cursor.execute(time_data)
    result = cursor.fetchall()

    if result and len(result) > 15:
        del_id = result[0][0]

        delete = "DELETE FROM requests WHERE id=%s;"
        vals = (del_id,)

        cursor.execute(delete, vals)

'''
ALL METHODS BELOW PERTAIN TO HTTP HEADERS

200 OK
302 REDIRECT
404 BAD REQUEST
405 METHOD NOT ALLOWED
403 Forbidden
'''
def http_200():
    print("status: 200 OK")
    print("Content-Type: text/html")
    print()

def http_302():
    print("Status: 302 Redirect")
    print("Location: /cgi-bin/webhooks/get")
    print()

def http_403():
    print("Status: 403 Forbidden")
    print()

def http_404():
    print("Status: 404 Bad Request")
    print()

def http_405():
    print("Status: 405 Method Not Allowed")
    print("Location: /cgi-bin/webhooks/get")
    print()

# METHOD USED TO CONNECT TO DATABASE
def connect_db():
    conn = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWORD, db = "hookbase")
    return conn

if __name__ == '__main__':
    main()