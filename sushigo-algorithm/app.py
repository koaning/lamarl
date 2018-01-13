import random
import math
from chalice import Chalice

app = Chalice(app_name='sushigo-algorithm')


def sort_hand(hand, order):
    card_dict = {card: i for i, card in enumerate(order)}
    return sorted(hand, key=lambda x: card_dict[x])


def score_table(hand_player, hand_opponent):
    score = 0
    multiplier = 1
    for card in hand_player:
        if card == "wasabi":
            multiplier = multiplier * 2
        if card == "egg":
            score += 1 * multiplier
            multiplier = 1
        if card == "salmon":
            score += 2 * multiplier
            multiplier = 1
        if card == "squid":
            score += 3 * multiplier
            multiplier = 1
    player_maki = sum([int(c.replace("maki-", "")) for c in hand_player if "maki" in c])
    opponent_maki = sum([int(c.replace("maki-", "")) for c in hand_opponent if "maki" in c])
    if player_maki > opponent_maki:
        score += 6
    elif player_maki > 1:
        score += 3
    player_sashimi = sum([1 for c in hand_player if c == "sashimi"])
    score += math.floor(player_sashimi/3)

    player_tempura = sum([1 for c in hand_player if c == "tempura"])
    score += math.floor(player_tempura / 3)

    player_dumpling = sum([1 for c in hand_player if c == "dumpling"])
    dumpling_scores = [0, 1, 3, 6, 10, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]
    score += dumpling_scores[player_dumpling]

    player_tofu = sum([1 for c in hand_player if c == "tofu"])
    tofu_scores = [0, 2, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    score += tofu_scores[player_tofu]

    player_eel = sum([1 for c in hand_player if c == "eel"])
    eel_scores = [0, -3, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
    score += eel_scores[player_eel]

    player_temaki = sum([1 for c in hand_player if c == "temaki"])
    opponent_temaki = sum([1 for c in hand_opponent if c == "temaki"])
    if player_temaki > opponent_temaki:
        score += 4
    return score


def simulate(order):
    """
    There's 14 cards, so there's 14! = 87178291200 possibilities! 
    Such complexity! Must have compute power! 
    """
    cards = ["maki-1", "maki-2", "maki-3", "sashimi",
             "egg", "salmon", "squid", "wasabi", "pudding",
             "tempura", "dumpling", "tofu", "eel", "temaki"]
    deck = cards * 5
    random.shuffle(deck)

    deck, hand_player = deck[10:], deck[:10]
    deck, hand_opponent = deck[10:], deck[:10]
    hand_player = sort_hand(hand_player, order)
    random.shuffle(hand_opponent)
    table_player, table_opponent = [], []
    while len(hand_player) > 0:
        table_player.append(hand_opponent.pop())
        table_opponent.append(hand_player.pop())
        hand_player, hand_opponent = hand_opponent, hand_player
    return score_table(table_player, table_opponent) > score_table(table_opponent, table_player)

@app.route('/')
def index():
    return {'hello': 'sim'}

@app.route('/mirror', methods=['POST'])
def mirror():
    json_body = app.current_request.json_body
    return json_body

@app.route('/sim/{n}', methods=['POST'])
def simulation_endpoint(n):
    json_body = app.current_request.json_body
    return sum(simulate(json_body['order']) for _ in range(int(n)))

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
