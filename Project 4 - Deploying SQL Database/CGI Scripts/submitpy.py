#! /usr/bin/python3

import cgi
import MySQLdb
import passwords

form = cgi.FieldStorage()

def main():
    print_header()
    print_title()

    # MAKES A CONNECTION TO DATABASE
    conn = connect_db()
    cursor = conn.cursor()

    # ADDS A RECORD TO THE TABLE
    add_record(cursor)

    # COMMITS CHANGES TO THE DATABASE AND CLOSES THE CONNECTION
    conn.commit()
    conn.close()
    print_close()

def add_record(cursor):
    table = form["table"].value
    try:
        if table == "Customers":
            sql = "INSERT INTO Customers (first_name, last_name, address, city, postal_code, country) VALUES (%s, %s, %s, %s, %s, %s);"

            vals = (form["first_name"].value, form["last_name"].value, form["address"].value, form["city"].value, form["postal_code"].value, form["country"].value)

            cursor.execute(sql, vals)

            print("""<h2 style="text-align:center;">Record Submitted Successfully! </h2>""")
            print("""<h2 style="text-align:center;">Rows Affected: {0}</h2>""".format(cursor.rowcount))

        if table == "Products":
            sql = "INSERT INTO Products (product_name, sector, curr_qty, price) VALUES (%s, %s, %s, %s)"

            vals = (form["product_name"].value, form["sector"].value, form["curr_qty"].value, form["price"].value)

            cursor.execute(sql, vals)

            print("""<h2 style="text-align:center;">Record Submitted Successfully!</h2>""")
            print("""<h2 style="text-align:center;">Rows Affected: {0}</h2>""".format(cursor.rowcount))

        if table == "Orders":
            insert_order(cursor)
    except:
        print("""<h2 style=text-align:center;">WAS NOT EXECUTED</h2>""")
        print("""<h3 style=text-align:center;">!Could Be Missing A FIELD!</h3>""")


    cursor.close()

def insert_order(cursor):
    sql = "INSERT INTO Orders (customerID, productID, qty, price, purchase_date) VALUES (%s, %s, %s, %s, %s)"

    pid, cid = form["productID"].value, form["customerID"].value

    cursor.execute("SELECT 1 FROM Products WHERE id = %s", (pid,))
    check = cursor.fetchall()

    cursor.execute("SELECT 1 FROM Customers WHERE id = %s", (cid,))
    check2 = cursor.fetchall()

    if not check or not check2:
        print("""<h2 style=text-align:center;">WAS NOT EXECUTED</h2>""")
        print("""<h3 style=text-align:center;">Please Enter A Valid Product and Customer ID</h3>""")
    else:
        try:
            vals = (cid, pid, form["qty"].value, form["price"].value, form["purchase_date"].value)

            cursor.execute(sql, vals)

            print("""<h2 style="text-align:center;">Record Submitted Successfully!</h2>""")
            print("""<h2 style="text-align:center;">Rows Affected: {0}</h2>""".format(cursor.rowcount))
        except:
            print("""<h2 style=text-align:center;">WAS NOT EXECUTED</h2>""")
            print("""<h3 style=text-align:center;">!Could Be Missing A FIELD!</h3>""")


def print_title():
    print("""
        <div style="text-align: center;">
            <h1 style="font-size: 70px; margin-bottom: 5px;">Record Sent!</h1>
            <form action="/cgi-bin/add" method="get">
                <button style="font-size: 20px;">Go Back</button>
            </form>
        </div>""")

def send_https():
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()

def print_header():
    print("<html>")
    print("""
    <html>
    <head>
        <title>Submitted!</title>

        <style type="text/css">
            
            html {
                background-image: url("/grad_back.jpg");
                background-repeat: no-repeat;
                background-size: 100% 100%;
                background-attachment: fixed;
            }

        </style>
    </head>""")

def print_close():
    print("</body>")
    print("</html>")

def connect_db():
    conn = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWORD, db = "salesbase")

    return conn

if __name__ == '__main__':
    send_https()
    print_header()
    main()