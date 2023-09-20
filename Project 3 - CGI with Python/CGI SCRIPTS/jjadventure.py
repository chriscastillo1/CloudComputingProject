#! /usr/bin/python3

import cgi
from random import randint, choice

form = cgi.FieldStorage()

# CHECKS FOR WIN OR LOSE CONDITION AND REDIRECTS THEM TO APPROPRIATE PAGE
if "day" not in form:
    print("Location: /cgi-bin/lose")
elif "monster_day" not in form:
    print("Location: /cgi-bin/lose")
elif (int(form["monster_day"].value) >= int(form["day"].value)):
    print("Location: /cgi-bin/caught?day={}".format(form["day"].value))
elif (int(form["day"].value) == 25):
    print("Location: /cgi-bin/win")

# START OF MAIN SCRIPT
def main():
    # CHECKS IF ONE PLAYER DIES --> PRINTS LOSE SCREEN
    if jack_h <= 0 or jill_h <= 0:
        print_lose_screen()

    # CONTINUES THE NORMAL GAME PROGRESSION
    else:
        if recovered_jack <= 0 or recovered_jill <=0:
            print_lose_screen()
        else:
            # PRINTS OUT HEALTH BOX HEADERS AND DAY / SCORE INDICATOR
            print_health_boxes()

            # PRINTS OUT JOURNAL MESSAGE OF THE DAY
            storytime()

            # PRINTS OUT DAMAGE MESSAGE
            paintime()

            # SUBMITS FORM WITH VARS FOR NEXT PAGE
            submit_form()

            # CLOSES HTML BODY
            print("</html>")

def send_https():
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()

def print_header():
    print("<html>")
    print("""
    <head>
    <link rel="stylesheet" type= "text/css" href="/styles.css">
    <title>J&J's Adventures</title>
    </head>""")

def submit_form():
    print("""
    <div class="buttonlayout">
        <form class="button1" action="/cgi-bin/jjadventure" method="get">
            <input type=hidden name="jack_health" value="{0}">
            <input type=hidden name="jill_health" value="{1}">
            <input type=hidden name="monster_day" value="{2}">
            <input type=hidden name="day" value="{3}">
            <button style="background-color: green; font-size: 30px;">Continue</button>
        </form>
        <form class="button2" action="/cgi-bin/jjadventure" method="get">
            <input type=hidden name="jack_health" value="{4}">
            <input type=hidden name="jill_health" value="{5}">
            <input type=hidden name="monster_day" value="{6}">
            <input type=hidden name="day" value="{7}">
            <button style="background-color: red; font-size: 30px;">Rest</button>
        </form>
    </div>
    </body>""".format(recovered_jack, recovered_jill, m_day, new_day, rest_jack, rest_jill, m_rest, day_num))

def storytime():
    print("""<div class="storytime">""")
    if day_num == 1:
        print("""<p>Its Day 1. Me and Jack are setting off towards the glistening peaks. Oh how I've waited to go exploring on this mountain. I just hope Jack starts to man up... On our way here we passed by a couple of warning signs, something like "Beware the ---". It was scratched out but I really don't think a couple of signs can stop me. "Oh we should turn back" or "This isnt safe" blah blah blah... That might be the only thing I can't stand - hearing Jack whine all day. Any good exploration HAS to have some danger right?? I expect to get a few scrapes and bruises, which is why I brough extra bandages. We can't go back now, onward towards adventure!</p></div>""")
    elif day_num == 2:
        print("""<p>Day 2. As we were hiking along I started noticing strange sounds. It was like hearing another set of foot steps as we hiked. But every time Jack and I stopped, the footsteps stop. The first night was a little eerie but I thought nothing of it. However, I cant help but feel like something is watching us... I think we are being followed... by something. I have yet to tell Jack, I dont want to scare him... or hear "I told you so"... I guess we will keep on going.</p></div>""")
    else:
        print("""<p>Day {0}. {1}</p></div>""".format(day_num, message()))

def paintime():
    print("""<div class="aftermath">""")
    print("""<p>{0}</p>""".format(pain().format(damage_jack, damage_jill, recov_pts_jack, recov_pts_jill)))
    print("""</div>""")

    print("""<div style="font-size: 20px; text-align: center; padding-bottom: 5px;">Jacks End HP: {0} Jills End HP: {1}</div>""".format(recovered_jack, recovered_jill))

def print_health_boxes():
    print("""
    <body>
    <div class="container">
        <div class="score">Day {0}</div>
        <table style="width:40%">
            <tr>
                <th>Jack</th>
                <th>Jill</th>
            </tr>
            <tr>
                <th>Start HP: {1}</th>
                <th>Start HP: {2}</th>
            </tr>
        </table>
    </div>""".format(day_num, jack_h, jill_h))

def print_lose_screen():
    # Prints Death Message w/ SCORE = NUMBER OF DAYS SURVIVED
    print("""
        <div class="gameover">
            <p style="font-size:30px;">Today was the day, they thought, to make it to the very top! But fate had other plans. Jack and Jill were so very close, but then a thunder arose. There they went, down the hill, tumbling to their deaths.</p>""")
    print("""<p style="font-size:30px">Score: Survived {0} Day(s)""".format(day_num))

    # CREATES A RESTART BUTTON THAT SENDS IT BACK TO START PAGE
    print("""
        <form style="display:flex; justify-content: center; padding-top: 20px;" action="/cgi-bin/start">
            <button style="background-color: green; font-size: 30px;">RESTART</button>
        </form></div>""")

# DAMAGE MESSAGE BANK. USES RANDOM CHOICE TO CHOOSE A MESSAGE
def pain():
    message = []

    a = "It was bound to happen but Jack tripped over a rock pulling Jill along for the ride. Jack sustained {0} damage while Jill took {1} damage. Although irate, Jill took out her bandages and patched them both up. After an hour, Jack recovered {2} HP and Jill recovered {3} HP."

    b = "As Jack and Jill were hiking, a bear suddenly came out of no where! It swiped its paw at Jack with enough force to throw him off his feet. Jill fared no better. Jack sustained {0} damage while Jill took {1} damage. However, thankfully the bear left soon after. With a few bandages and a couple of hours, Jack recovered {2} HP and Jill recovered {3} HP."

    c = "Jill thought this trip would be the death of them. What happend? An avalanche. A rock slide Jack caused by throwing rocks... It was a hailstorm as Jack and Jill had to run desparately to safety. Finally they found a little ledge cave that sheltered them. However, they were not without injury. Jack sustained {0} damage while Jill took {1} damage. Taking out her trusty bandages, Jack recovered {2} HP and Jill recovered {3} HP."

    message.append(a); message.append(b); message.append(c)
    return choice(message)

# JOURNAL MESSAGE BANK. USES RANDOM CHOICE TO CHOOSE A MESSAGE
def message():
    message = []
    a = "After I woke up, it started raining. Just my luck. I tried to go back to sleep but the wind kept rustling the little tent. I looked over to Jack and I have no idea how he can sleep through this. Im jealous. But what uneased me this morning was I swore I saw a shadow of a figure on the tent. But as soon as I made some noise it disappeared. It must be the wind and sun casting a shadow. But I am now 60 percent confident that we are being followed. I bet its some of Jack's hooligan friends trying to prank us... I hope."
    b = "I discovered an amazing crevas that goes at least 100ft deep. Of course Jack threw a rock down there but I was curious too. I just barely heard the splash of the rock. I think Jack is warming up to this adventure though, he seems excited. Though even though he hasnt told me yet, sometimes when I talk with Jack, I see his eyes drift off behind me. But every time I ask him, he says its nothing. I just know Jack has quite the imagination. But today is a new day! So Onward!"
    c = "Absolutely Drenched. I hate this trip. I woke up to it pouring and guess what I find??? Jack forgot to zip up the tent flap all the way so now I am soaked. I bet its payback since I didn't let him eat my candy. Now I am all sore and in a bad mood. Jack better not get on my nerves... The pathway has become muddier and very hard to see but I'm not too worried. I have a great sense of direction. Anyhow, today will be much harder of a trek."
    d = "It was quite an early morning, but I had a good feeling. Me and Jack made a huge amount of progress yesterday. Though I thought I almost died when I accidentally tripped near the ledge... Not fun but thankfully Jack grabbed my arm and pulled me away. Currently we are taking a break and just enjoying the day. Though when we were eating lunch, I thought I heard leaves crunching like someone was walking over them… When I looked there was nothing, I think its just because I’ve been exhausted all day."
    e = "This is a bit of a later entry, but the sun is starting to set, and I just had to write about the beautiful dusk sun peaking over the trees. This is why I wanted to go exploring. Beautiful. Absolutely beautiful. Though when we were hiking Jack was ahead of me and I swore I thought I saw some looming shadow to my right… I think it was just the trees shadows but that really scared me. I called out to Jack but when he turned around the shadow disappeared. Maybe I’m just too tired."
    f = "This is weird… I’m not used to keeping a “diary” but every time we stop, I see Jill always writing in her little journal of hers. I figured I’d give it a try. I’ve known Jill for quite a while, and I know when something is up… I may be a little too energetic sometimes, but I think Jill seems on edge about something. I’m not sure what it is but I think she should just relax and enjoy the journey right? As she would say, “Onward towards adventure”! Though admittedly I do love a good adventure myself."
    g = "Okay so I woke up to the sound of whistling. I looked over and Jill was sound asleep. Because I’m super brave I went to check it out. Plus I don’t want to hear Jill’s annoying pestering saying that I woke her up for no reason. God… I think she finds every little thing I do is wrong. I’m trusting my gut instinct here. But aside from that rant, what I discovered was far more creepy --- I mean far more startling than I expect. It was hard to distinguish but I know I saw it. It was a huge shadow cast against the tree line… Maybe it’s this is what Jill was worrying about…"
    h = "Jack… I think I have a love hate relationship with him. I think we are so close to the top, but he insisted that we stop. Okay maybe I am being a little harsh, he did trip but that’s because he wasn’t looking at where he was going. Plus, I was on a rather good pace. I got some amazing photos today too! Can’t wait to scrapbook them… It just annoying… Where is his sense of adventure?"
    i = "I know something is following us. I’m beginning to suspect Jack knows that I’ve been off a little lately. I didn’t want to admit it but I now have proof. We took a little detour to explore a waterfall off to the side of the trial. However, I secretly dropped little crumbs of bread behind us, small enough where only if you were looking would you notice. When we came back those pieces of bread were pressed into the ground. Like something stepped on them. I haven’t told Jack yet… I don’t know how too and I don’t want to freak him out… All I can say is we are picking up the pace."

    message.append(a); message.append(b); message.append(c); message.append(d); message.append(e)
    message.append(f); message.append(g); message.append(h); message.append(i);
    return choice(message)

# THIS SETS AND CREATES ALL THE FORM VARIABLES NEEDED FOR THE GAME TO WORK
# NOTE: EVERY FUNCTION ACCESSES THE VARIABLES GLOBALLY. SO NO NEED TO PASS PARAMS TO ANY FUNCTION
def create_vars():
    global jack_h, jill_h, day_num, m_day, damage_jack, damage_jill
    global new_jack_health, new_jill_health, recov_pts_jack, recov_pts_jill, new_day
    global recovered_jack, recovered_jill, rest_jack, rest_jill, m_rest
    # ESTABLISHES GLOBAL FORM VARIABLES (CARRY ON TO NEXT PAGE RELOAD)
    jack_h, jill_h = int(form["jack_health"].value), int(form["jill_health"].value)
    day_num, m_day = int(form["day"].value), int(form["monster_day"].value)

    # CHANGE TO SET GAME BALANCE (HIGHER = MORE DAMAGE DEALT)
    damage_jack, damage_jill = randint(10,45), randint(10,45)
    # HEALTH VALUES IF PLAYER CHOOSES CONTINUE
    new_jack_health, new_jill_health = jack_h - damage_jack, jill_h - damage_jill
    # CHANGE TO SET GAME BALANCE (HIGHER = MORE HEALTH RECOVERY)
    recov_pts_jack, recov_pts_jill = randint(5, 25), randint(5, 25)
    new_day = day_num + 1
    recovered_jack, recovered_jill = new_jack_health + recov_pts_jack, new_jill_health + recov_pts_jill
    # SETS HEALTH VALUES IF PLAYER CHOOSES REST OPTION
    rest_jack, rest_jill = jack_h + randint(5, 25), jill_h + randint(5,25)

    # CHECKS IF HEALTH GOES ABOVE 100, IT JUST SETS IT TO 100
    if rest_jack >= 100:
        rest_jack = 100
    if rest_jill >= 100:
        rest_jill = 100
    if recovered_jack >= 100:
        recovered_jack = 100
    if recovered_jill >= 100:
        recovered_jill = 100

    # IF PLAYERS REST, THIS IS HOW MANY DAYS THE MONSTER WILL GAIN ON THEM    
    m_rest = m_day + randint(2,4)
    # IF PLAYERS CONTINUE, THIS IS HOW MANY DAYS MONSTER WILL GAIN / LOSE ON THEM
    m_day += randint(-1,1)

if __name__ == '__main__':
    send_https()
    print_header()
    create_vars()
    main()