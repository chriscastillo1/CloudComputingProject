#! /usr/bin/python3

import cgi
import MySQLdb
import passwords

form = cgi.FieldStorage()

def main():
    # PRINTS TITLE AND HEADER FOR SEARCH
    print_title()
    print_header()

    print_form()

    print_close()

def print_form():
    print("""<div style="text-align: center; padding-top: 50px;">""")
    print("""<table style="height: 100px;">""")
    print("""<tr><th>customerID <th>productID <th>productName <th>Sector <th>Qty <th>Price""")
    print("""
        <form action="/cgi-bin/searchresult" method="get">
            <tr><td><input type="text" name="customerID"> 
            <td><input type="text" name="productID"> 
            <td><input type="text" name="product_name"> 
            <td><select style="width:175px;" name="sector" id="table">
                    <option value="Not Selected">Not Selected</option>
                    <option value="Industrials">Industrials</option>
                    <option value="Consumer">Consumer</option>
                    <option value="Services">Services</option>
                    <option value="Resources">Resources</option>
                </select>

            <td><input type="text" name="qty"> 
            <td> <input type="text" name="price">
            </table>

            <div style="text-align: center;">
                <button style="background-color: white; font-size: 24px;">Search</button> 
            </div>
        </form>""")

    print("</div>")


def send_https():
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()

def print_header():
    print("<html>")
    print("""
    <head>
        <title>Search</title>
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
        </div>
        <div id="intro">
            <p>Search for an Order</p>
            <p style="font-size: 24px;" >NOTE: Can use any number of Field Parameters to Search</p>
        </div>""")

def print_close():
    print("</body>")
    print("</html>")

if __name__ == '__main__':
    send_https()
    print_header()
    main()