import random
import itertools as it
import sushigo
from chalice import Chalice

POSSIBLE_CARDS = list(set([str(_) for _ in sushigo.deck.StandardDeck()]))

class CustomPlayer(sushigo.player.Player):
    def __init__(self, order, name=None):
        super(CustomPlayer, self).__init__()
        self.name = 'custom-player'
        if name:
            self.name = name
        self.order = order
        if any([(_ not in order) for _ in POSSIBLE_CARDS]):
            raise ValueError("forgot card type in OrderedPlayer init")

    def act(self, reward, observation=None, action_space=None):
        if not action_space:
            raise ValueError("player received an empty set of actions")

        # the player can get a notion of possible cards, give them an order
        order = {j: i for i, j in enumerate(self.order)}
        # the action space consists of objects now, which we may need to string-sort
        ordered_actions = sorted(action_space, key = lambda _: order[str(_)])
        return ordered_actions[-1]


app = Chalice(app_name='sushigo')


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/cards')
def index():
    return {'cards': POSSIBLE_CARDS}


def sim_single_game(order):
    p1 = sushigo.player.Player(name="opponent")
    p2 = CustomPlayer(name="custom", order=order)
    game = sushigo.game.Game([p1, p2], deck=sushigo.deck.StandardDeck())
    game.simulate_game()
    return 1 if game.did_player_win("custom") else 0

print(sim_single_game(POSSIBLE_CARDS))

@app.route('/sushigo/{n_games}')
def sushigo_game(n_games):
    app.log.error("i am in it")
    # json_layload = app.current_request.json_body
    # app.log.error(f"this is the payload {json_payload}")
    res = []
    order = POSSIBLE_CARDS
    app.log.error(f"this is the order {order}")
    return sum([sim_single_game(order) for _ in range(n_games)])

def allow(perm):
    """
    This function acts as a predicate for allowed permutations.
    """
    # leaves us with 1108800/39916800 permutations
    order = {j: i for i, j in enumerate([str(_) for _ in perm])}
    if order['NigiriCard("egg")'] > order['NigiriCard("salmon")']:
        return False
    if order['NigiriCard("salmon")'] > order['NigiriCard("squid")']:
        return False
    if order['MakiCard("2")'] > order['MakiCard("3")']:
        return False
    if order['MakiCard("1")'] > order['MakiCard("2")']:
        return False
    return True
