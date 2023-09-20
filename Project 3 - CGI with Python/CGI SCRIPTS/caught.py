#! /usr/bin/python3

import cgi

form = cgi.FieldStorage()

print("Content-Type: text/html")
print("Status: 200 OK")
print()

day = int(form["day"].value)

print("<html>")

print("""
<head>
    <style>
        body {
            background-image: url("/monster.jpg");
            background-repeat: no-repeat;
            background-size: 100% 100%;
            background-attachment: fixed;
        }
        .lose {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            border: 5px solid white;
            padding: 10px;
        }
        .losem {
            font-weight: bold;
            color: red;
            font-size: 100px;
            text-align: center;
        }
    </style>
    <title>YOU LOSE</title>
</head>""")

print("""
<body>
<div class="lose">
    <h1 class="losem">YOU LOSE</h1>
    <p style="color: white; font-size: 30px;">It was a valiant effort... But unfortunately you could not outrun it... Jack and Jill are no longer with us.</p>
    <p style="color: white; font-size: 35px;">Score: Survived {} Days</p>
    <form style="display:flex; justify-content: center; padding-top: 10px;" action="/cgi-bin/start">
        <button style="background-color: red; font-size: 30px;">RESTART</button>
    </form>
</div>
</body>""".format(day))

print("</html>")