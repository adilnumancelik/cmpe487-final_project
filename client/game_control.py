import pickle
import client_app

def process_message(inc_message):
    if str(inc_message) != "WRONG":
        client_app.game = pickle.loads(inc_message)

    player_action(client_app.game)

def player_action(game):
    utils.update(game)
    # TODO Get changes from user.
    if game.state == "Move":
        message_object= {"TYPE": "MOVE","PAYLOAD": "oynadım lan"}
    elif game.state == "Answer":
        message_object= {"TYPE": "ANSWER","PAYLOAD": "40 yapar"}
    elif game.state == "ready":
        message_object= {"TYPE": "ANSWER","PAYLOAD": "bizhazır doğmuşuz kardeş"}    
    message=json.dumps(message_object)
    network.send_message(client_app.SERVER, client_app.SERVER_IP, client_app.PORT, message)