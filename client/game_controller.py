import pickle
import client_app

class GameController():

    def __init__(self):
        self.game = Game(10, 10)

    def process_message(inc_message):
        if str(inc_message) != "WRONG":
            self.game = pickle.loads(inc_message)

        # return self.player_action()

    def player_action():
        utils.update(game)
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