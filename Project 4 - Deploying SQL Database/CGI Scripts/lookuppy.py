#! /usr/bin/python3

import cgi
import MySQLdb
import passwords

form = cgi.FieldStorage() 

def main():
    # PRINTS TITLE FOR PAGE AND PRINT FORM SELECT & MANUAL SEARCH
    print_title()
    print_form()

    print_submission()

    # CLOSES OUT HTML
    print_close()

def print_submission():
    print("""<div style="text-align: center; padding-top: 50px;">""")

    # CHECKS FORM SUBMISSION CONDITIONS
    table_con = table_conditions()
    if table_con == "DNE":
        print("<h2>Table You Searched For Does Not Exist</h2>")
    elif table_con == "USED_BOTH":
        print("<h2>Use Only One Search: Either Select OR Manual Search")
    elif table_con == "BLANK":
        print("<h2>Please Select a Table</h2>")
    else:
        make_table(table_con)

    #conn.close()
    print("</div>")

# CONSTRUCTS A TABLE BASED OFF DIFFERENT TABLE PARAMETERS
def make_table(user_input):
    conn = connect_db()
    cursor = conn.cursor()

    # PRINTS OUT TABLE STYLING
    print("""<table style="height: 400px;">""")

    if user_input == "Orders":
        print("""<tr> <th style="width:25px;">ID <th>customerID <th>productID <th>Quantity <th>Price <th> Date""")
    if user_input == "Products":
        print("""<tr> <th style="width:25px;">ID <th>Product Name <th>Sector <th>Quantity <th>Price""")
    if user_input == "Customers":
        print("""<tr> <th style="width:25px;">ID <th>First <th>Last <th>Address <th>City <th>Postal <th>Country""")

    # NEED TO SANATIZE RESULTS -----------------------
    sql = "SELECT * FROM %s"
    vals = (user_input,)
    cursor.execute(sql % vals)
    results = cursor.fetchall()

    # GOES THROUGH EVERY TABLE AND TURNS IT INTO AN HTML TABLE RECORD
    for record in results:
        print("<tr>")

        for item in record:
            print("<td> %s" % (item,))

    cursor.close()
    conn.close()
    print("</table>")

# CHECKS USER INPUT AND CONDITIONS
def table_conditions():
    select = form["table"].value

    # IF USER DOES MANUAL SEARCH -- CHECKS IF TABLE IS VALID
    if select == "Not Selected" and "usr_input" in form:
        user_input = form["usr_input"].value
        if user_input in ["Orders", "Customers", "Products"]:
            return user_input
        else: return "DNE"

    elif select != "Not Selected" and "usr_input" not in form:
        return select

    elif select != "Not Selected" and "usr_input" in form:
        return "USED_BOTH"

    else: return "BLANK"

# CREATES AN SQL CONNECTION AND RETURNS A USUABLE CONNECTION
def connect_db():
    conn = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWORD, db = "salesbase")

    return conn

# SENDS THE HTTP HEADER RESPONSE
def send_https():
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()

# PRINTS OUT HTML HEAD FOR WEBSITE
def print_header():
    print("<html>")
    print("""
    <head>
        <title>Table Lookup</title>
        <style type="text/css">

            html {
                background-image: url("/grad_back.jpg");
                background-repeat: no-repeat;
                background-size: 100% 100%;
                background-attachment: fixed;
            }

            h2 {
                color: #ff1c1c;
            }

            #intro {
                font-size: 40px;
                text-align: center;
            }

            table { margin-top:  20px; display: inline-block; overflow: auto; }
            th {
                font-size: 25px;
                width: 175px;
            }

            td {
                text-align: center;
            }

            table { border-collapse: collapse; }
            tr:nth-child(even) { background: #1fb0ff; }
        </style>
    </head>""")

# PRINTS EXPLANATORY PHRASE FOR PAGE
def print_title():
    print("""
        <div style="text-align: center;">
            <h1 style="font-size: 70px; margin-bottom: 5px;">Table Lookup</h1>
            <form action="/" method="get">
                <button style="font-size: 20px;">Go Back</button>
            </form>
        </div>
        <div id="intro">
            <p>Lookup a Table in the Database using either the Drop Down or Manual Search</p>
            <p style="font-size: 24px;" >Warning: Manual Search is CASE-SENSITIVE</p>
        </div>""")

# PRINTS OUT TABLE SELECT OR MANUAL SEARCH FORM
def print_form():
    print("""
        <div style="text-align: center;">
            <form action="/cgi-bin/lookup" method="get">
                <label style="font-size: 20px;" for="table">Select a Table:</label>

                <select name="table" id="table">
                    <option value="Not Selected">Not Selected</option>
                    <option value="Orders">Orders</option>
                    <option value="Products">Products</option>
                    <option value="Customers">Customers</option>
                </select>

                <label style="font-size: 20px; padding-left: 5px;" for="blank">Enter a Table Name:</label>
                <input type="text" name="usr_input" value="">

                <div style="text-align: center; padding-top: 20px;">
                   <button style="background-color: white; font-size: 20px;">Search</button> 
                </div>
            </form>
        </div>
        """)

# PRINTS CLOSING HTML
def print_close():
    print("</body>")
    print("</html>")

if __name__ == '__main__':
    send_https()
    print_header()
    main()