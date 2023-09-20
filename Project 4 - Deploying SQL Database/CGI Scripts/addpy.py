#! /usr/bin/python3

import cgi
import MySQLdb
import passwords

form = cgi.FieldStorage() 

def main():
    # PRINTS TITLE FOR PAGE AND PRINT FORM SELECT & MANUAL SEARCH
    print_title()
    table_select()

    print_submission()

    # CLOSES OUT HTML
    print_close()

def print_submission():
    print("""<div style="text-align: center; padding-top: 50px;">""")

    if form["table"].value == "Not Selected":
        print("""<h2 style="text-align:center;">Please Select A Table<h2>""")
    else: 
        selection = form["table"].value

        print("""<table style="height: 100px;">""")

        if selection == "Customers":
            print("""<tr><th>First <th>Last <th>Address <th>City <th>Postal <th>Country""")
            print("""
                <form action="/cgi-bin/submit" method="get">
                    <tr><td><input type="text" name="first_name"> 
                    <td><input type="text" name="last_name"> 
                    <td><input type="text" name="address"> 
                    <td><input type="text" name="city"> 
                    <td><input type="text" name="postal_code"> 
                    <td> <input type="text" name="country">
                    </table>

                    <input type="hidden" name="table" value="{0}">
                    <div style="text-align: center;">
                        <button style="background-color: white; font-size: 24px;">Submit Consumer Record</button> 
                    </div>
                </form>""".format(selection))

        if selection == "Products":
            print("""<tr><th>Name <th>Sector <th>Curr_Qty <th>Price""")
            print("""
                <form action="/cgi-bin/submit" method="get">
                    <tr><td><input type="text" name="product_name"> 
                    <td><select style="width:175px;" name="sector" id="table">
                            <option value="Industrials">Industrials</option>
                            <option value="Consumer">Consumer</option>
                            <option value="Services">Services</option>
                            <option value="Resources">Resources</option>
                        </select>

                    <td><input type="text" name="curr_qty"> 
                    <td><input type="text" name="price"> 
                    </table>

                    <input type="hidden" name="table" value="{0}">
                    <div style="text-align: center;">
                        <button style="background-color: white; font-size: 24px;">Submit Product Record</button> 
                    </div>
                </form>""".format(selection))

        if selection == "Orders":
            print("""<tr><th>customerID <th>productID <th>Qty <th>Price <th>Purchase Date""")
            print("""
                <form action="/cgi-bin/submit" method="get">
                    <tr><td><input type="text" name="customerID"> 
                    <td><input type="text" name="productID"> 
                    <td><input type="text" name="qty"> 
                    <td><input type="text" name="price"> 
                    <td><input type="text" name="purchase_date"> 
                    </table>

                    <input type="hidden" name="table" value="{0}">
                    <div style="text-align: center;">
                        <button style="background-color: white; font-size: 24px;">Submit Order Record</button> 
                    </div>
                </form>""".format(selection))            

    print("</div>")

# SENDS THE HTTP HEADER RESPONSE
def send_https():
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()

# PRINTS OUT HTML HEAD FOR WEBSITE
def print_header():
    print("<html>")
    print("""
    <html>
    <head>
        <title>Add record</title>

        <style type="text/css">
            
            html {
                background-image: url("/grad_back.jpg");
                background-repeat: no-repeat;
                background-size: 100% 100%;
                background-attachment: fixed;
            }

            #intro {
                font-size: 40px;
                text-align: center;
            }

            h2 {
                color: #ff1c1c;
            }

            table { margin-top:  20px; display: inline-block; overflow: auto; }
        
            th {
                font-size: 25px;
                width: 175px;
            }
        </style>
    </head>""")

# PRINTS EXPLANATORY PHRASE FOR PAGE
def print_title():
    print("""
        <div style="text-align: center;">
            <h1 style="font-size: 70px; margin-bottom: 5px;">Add Record</h1>
            <form action="/" method="get">
                <button style="font-size: 20px;">Go Back</button>
            </form>
        </div>

        <div id="intro">
            <p>Add a Record to A Table in the Database</p>
            <p style="font-size: 24px;" >NOTE: When Adding to Orders, Must have Valid Product & Customer ID</p>
        </div>""")

# PRINTS FORM SUBMISSION TO SELECT A TABLE
def table_select():
    print("""
        <div style="text-align: center;">
            <form action="/cgi-bin/add" method="get">
                <label style="font-size: 20px;" for="table">Select a Table:</label>

                <select name="table" id="table">
                    <option value="Not Selected">Not Selected</option>
                    <option value="Orders">Orders</option>
                    <option value="Products">Products</option>
                    <option value="Customers">Customers</option>
                </select>

                <div style="text-align: center; padding-top: 20px;">
                   <button style="background-color: white; font-size: 20px;">Continue</button> 
                </div>
            </form>
        </div>""")

# PRINTS CLOSING HTML
def print_close():
    print("</body>")
    print("</html>")

if __name__ == '__main__':
    send_https()
    print_header()
    main()