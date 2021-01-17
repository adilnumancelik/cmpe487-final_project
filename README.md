# cmpe487-final_project
# Group Members
- Yasin Kaya 
- Adil Numan Çelik

# Description
S0S! A new game based on classical SOS game.
You need to solve easy mathematical problems before your opponent to get right to make your move.

# Tested on
Windows 10 Operating System

We highly recommend you to use it on Windows 10. Ubuntu or other operating systems probably won't run the program.

# How to Run
- To run the client open ../game/client folder in your Windows Terminal (cmd) and type:
```bash
python client_app.py
```

-To run the server:


# How to Play
You need to follow instruction on GUI. 
Every time you get a new question fill the form and press enter as fast as you can.
You have unlimited number of tries before either you or your opponent knows the correct answer.
If you find the correct answer first you can make your move. 
To make move first pick either S or O and press a button on board. 

# Network Challenges
We calculate timestamp differences of two machines and average pings of players at last 6 messages. 
This allows us to understand the sources of time difference between two answers. 
- Timestamp difference is usually fixed and always considered while doing calculations.
- Ping difference is not fixed and calculated after every message to make sure players play on fair conditions.

To create a fair game we
- Make the player with faster connection wait as much as the ping difference between players.
- Calculate the time difference that two players receive the message using the average ping difference and timestamp difference. If this difference is more than 10 ms we update the question until we make sure that this difference is less than 10 ms.
