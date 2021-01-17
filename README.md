# cmpe487-final_project
# Group Members
- Yasin Kaya 
- Adil Numan Çelik

# Description
S0S! A new game based on classical SOS game.
You need to solve easy mathematical problems before your opponent to get right to make your move.

# Tested on
Windows 10 Operating System

We highly recommend you to run it on Windows 10. Ubuntu or another operating system probably won't run the program.

However, if you want to run it on Ubuntu you will need to install Tkinter following this [tutorial](https://www.techinfected.net/2015/09/how-to-install-and-use-tkinter-in-ubuntu-debian-linux-mint.html)

# How to Run
- To run the client open ../game/client folder in your Windows Terminal (cmd) and type:
```bash
python client_app.py
```

- To run the server:

During the presentation we will deploy our server on an AWS EC2 instance located on Frankfurt. 
However, anytime you'd like to play the game you'll need to run the server on a machine of your choice. 
When you run your own server you'll need to change the hard coded SERVER_IP value in client_app.py file's 63rd line.
Then, you can open ../game/server folder in your Windows Terminal (cmd) and type:
```bash
python receiver.py
```



# How to Play
You need to follow instruction on GUI. 
Every time you get a new question fill the form and press enter as fast as you can.
You have unlimited number of tries before either you or your opponent finds the correct answer.
If you find the correct answer first, you can make your move. 
To make move, first pick either S or O and press a button on board. 

# Network Challenges
We calculate timestamp differences of two machines and average pings of players at last 6 messages. 
This allows us to understand the sources of time difference between two answers. 
- Timestamp difference is usually fixed and always considered while doing calculations.
- Ping difference is not fixed and calculated after every message to make sure players play on fair conditions.

To create a fair game we
- Make the player with faster connection wait as much as the ping difference between players.
- Calculate the time difference that two players receive the message using the average ping difference and timestamp difference. If this difference is more than 10 ms we update the question until we make sure that this difference is less than 10 ms.
