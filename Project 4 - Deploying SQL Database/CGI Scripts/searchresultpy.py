#! /usr/bin/python3

import cgi
import MySQLdb
import passwords

form = cgi.FieldStorage()

if "customerID" not in form and "productID" not in form and "product_name" not in form and form["sector"].value == "Not Selected" and "qty" not in form and "price" not in form:
    print("Location: /cgi-bin/search")

def main():
    # PRINTS TITLE AND HEADER FOR SEARCH
    print_title()
    print_header()

    process_results()

    print_close()

def process_results():
    conn = connect_db()
    cursor = conn.cursor()
    print("""<div style="text-align: center; padding-top: 50px;">""")

    sql = "SELECT Orders.ID, Orders.customerID, Orders.productID, Products.product_name, Products.sector, Orders.qty, Orders.price FROM Orders, Products WHERE Orders.productID = Products.ID AND customerID LIKE %s AND productID LIKE %s AND product_name LIKE %s AND sector LIKE %s AND Orders.qty LIKE %s AND Orders.price LIKE %s;"

    count = 0

    if "customerID" not in form:
        cID = '%'
        count += 1
    else: cID = form["customerID"].value

    if "productID" not in form:
        pID = '%'
        count += 1
    else: pID = form["productID"].value

    if "product_name" not in form:
        pname = '%'
        count += 1
    else: pname = form["product_name"].value

    if form["sector"].value == "Not Selected":
        sec = '%'
        count += 1
    else: sec = form["sector"].value

    if "qty" not in form:
        quant = '%'
        count += 1
    else: quant = form["qty"].value

    if "price" not in form:
        p = '%'
        count += 1
    else: p = form["price"].value

    vals = (cID, pID, pname, sec, quant, p)

    cursor.execute(sql, vals)
    results = cursor.fetchall()

    if not results or count == 6:
        print("<h2>No Results</h2>")
    else:
        print("""<table style="height: 400px;">""")
        print("""<tr><th style="width:25px;">ID <th>customerID <th>productID <th>Product Name <th>Sector <th> Qty <th>Price""")

        for record in results:
            print("<tr>")

            for item in record:
                print("<td> %s" % (item,))

    print("</table>")
    print("</div>")


def print_header():
    print("<html>")
    print("""
    <head>
        <title>Results</title>
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

def print_title():
    print("""
        <div style="text-align: center;">
            <h1 style="font-size: 70px; margin-bottom: 5px;">Search</h1>
            <form action="/" method="get">
                <button style="font-size: 20px;">Go Back</button>
            </form>
        </div>""")

def send_https():
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()

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