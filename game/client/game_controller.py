import pickle
import client_app
sys.path.append('..')

from game import Game, GameState

class GameController():
    game
    player_id
    is_message_received
    received_message

    def __init__(self):
        self.game = Game(10, 10)

    def process_message():
        is_message_received = False
        inc_message = self.received_message
        
        if inc_message["TYPE"] == "NAME":
            self.player_id = inc_message["PAYLOAD"]
        else:
            self.game = pickle.loads(inc_message)
            if self.game.state == "waiting":
                return
            elif self.game.state == "question":
                player_action_question()
            elif self.game.state == "move" and self.game.turn == player_id:
                player_action_move()
            else:
                return

    def player_action_question():
        print(self.game.question)
        ans = input("Enter your answer: ")
        while timeoutans != self.game.answer:
            print("Wrong answer.")
            ans = input("Enter your answer: ")
        
        # TODO Get changes from user.
        if self.game.state == "Move":
            message_object= {"TYPE": "MOVE","PAYLOAD": "oynadım lan"}
        elif self.game.state == "Answer":
            message_object= {"TYPE": "ANSWER","PAYLOAD": "40 yapar"}
        elif self.game.state == "ready":
            message_object= {"TYPE": "ANSWER","PAYLOAD": "bizhazır doğmuşuz kardeş"}    
        message=json.dumps(message_object)
        client_app.send_message(message)
        # return message

    def player_action_move():
        print(self.game.board)
