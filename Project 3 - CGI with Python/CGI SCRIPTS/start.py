#! /usr/bin/python3

import cgi

# Initializes the HTTP request, stating its HTML
print("Content-Type: text/html")
print("Status: 200 OK")
print()

form = cgi.FieldStorage()

print("""
<html>
<head>
    <style>
        body {
            background-image: url("/mountain.jpeg");
            background-repeat: no-repeat;
            background-size: 100% 160%;
            background-attachment: fixed;
        }

        .title {
            text-align: center;
            font-size: 30px;
            border: 3px solid black;
        }

        .explain {
            margin: auto;
            width: 50%;
            font-size: 20px;
            text-align: center;
        }
    </style>

    <title>J&J's Adventures</title>
</head>""")
print("<body>")

print("""
<h1 class="title">Welcome to Jack and Jill's Mountain Adventures!</h1>

<div class="explain">
<p style="font-weight: bold;">HOW TO PLAY:</p>
<p>Jack and Jill were on a journey through the mountains... until one night they noticed someone following them... No something following. Now Jack and Jill are on a race against the clock to reach the top of the mountain before whatever thats following them catches up. Can you help them survive?</p>
<p>Its a race against the clock, so time is limited. However, the monster is an unknown number of days behind Jack and Jill. You can choose to click Continue, gaining 1-3 days ahead of the monster. But be warned, travelling is dangerous and you will take severe damage. Make sure to pay attention to Jack and Jills Health Bar. You can choose to Rest, which will regain some lost HP. However, this will allow monster to catch up a certain number of days. You must reach the top to win. Choose Wisely.</p>
</div>

<form style="display:flex; justify-content: center; padding-top: 20px;" action="/cgi-bin/jjadventure" method="get">
    <input type=hidden name="jack_health" value="100">
    <input type=hidden name="jill_health" value="100">
    <input type=hidden name="monster_day" value="-2">
    <input type=hidden name="day" value="1">
    <button style="background-color: 4CAF50; font-size: 30px;">Start Game</button>
</form>""")

print("</body>")
print("</html>")