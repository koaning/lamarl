from abc import ABCMeta, abstractmethod
from math import floor


def sum_scores(*player_scores):
    if len(player_scores) == 0:
        return {}
    return {
        player: sum(player_score[player] for player_score in player_scores)
        for player in player_scores[0].keys()
    }


def count_cards(player_cards, card_type):
    return {
        player: len([card for card in cards if isinstance(card, card_type)]) for player, cards in player_cards.items()
    }


def count_values(player_cards, card_type):
    return {
        player: sum([card.value for card in cards if isinstance(card, card_type)])
        for player, cards in player_cards.items()
    }


def zero_score(player_cards):
    return {player: 0 for player in player_cards.keys()}


def split_score(card_counts, target_count, score):
    n_matches = len([_ for _, cnt in card_counts.items() if cnt == target_count])
    split = floor(score/n_matches)
    return {
        player: split if cnt == target_count else 0
        for player, cnt in card_counts.items()
    }


class Card:
    __metaclass__ = ABCMeta
    persistent = False

    def __repr__(self):
        return '{cls}({name})'.format(
            cls=self.__class__.__name__,
            name='"{x}"'.format(x=self.name) if hasattr(self, 'name') else ''
        )

    @classmethod
    @abstractmethod
    def score(cls, player_cards, end_game, end_round):
        raise NotImplementedError


class CollectionCard(Card):
    __metaclass__ = ABCMeta
    set_size = None
    set_score = None

    @classmethod
    def score(cls, player_cards, end_game, end_round):
        return {
            player: floor(n_cards/cls.set_size)*cls.set_score
            for player, n_cards in count_cards(player_cards, card_type=cls).items()
        }


class TempuraCard(CollectionCard):
    set_size = 2
    set_score = 5


class SashimiCard(CollectionCard):
    set_size = 3
    set_score = 10


class NigiriCard(Card):

    def __init__(self, name):
        self.name = name
        if self.name == 'egg':
            self.value = 1
        elif self.name == 'salmon':
            self.value = 2
        elif self.name == 'squid':
            self.value = 3
        else:
            raise ValueError('No such nigiri card: {name}'.format(name=name))

    @classmethod
    def score(cls, player_cards, end_game, end_round):
        result = {}
        for player, cards in player_cards.items():
            wasabi = 0
            score = 0
            for card in cards:
                if isinstance(card, WasabiCard):
                    wasabi += 1
                elif isinstance(card, cls):
                    if wasabi > 0:
                        wasabi -= 1
                        score += card.value * 3
                    else:
                        score += card.value
            result[player] = score
        return result


class MakiCard(Card):

    def __init__(self, value):
        self.value = value

    @property
    def name(self):
        return self.value

    @classmethod
    def score(cls, player_cards, end_game, end_round):
        if not end_round:
            return zero_score(player_cards)
        maki_points = count_values(player_cards, card_type=cls)
        max_points = max(maki_points.values())
        if max_points == 0:
            return zero_score(player_cards)
        scores = split_score(maki_points, target_count=max_points, score=6)
        if len([score for score in scores.values() if score > 0]) > 1:
            return scores
        sub_points = max(points for points in maki_points.values() if points < max_points)
        if sub_points == 0:
            return scores
        sub_scores = split_score(maki_points, target_count=sub_points, score=3)
        return sum_scores(scores, sub_scores)


class WasabiCard(Card):

    @classmethod
    def score(cls, player_cards, end_game, end_round):
        return zero_score(player_cards)


class DumplingCard(Card):
    scores = {0: 0, 1: 1, 2: 3, 3: 6, 4: 10, 5: 15}

    @classmethod
    def score(cls, player_cards, end_game, end_round):
        return {
            player: cls.scores[n_cards] if n_cards in cls.scores else 15
            for player, n_cards in count_cards(player_cards, card_type=cls).items()
        }


class PuddingCard(Card):
    persistent = True

    @classmethod
    def score(cls, player_cards, end_game, end_round):
        if not end_game:
            return zero_score(player_cards)
        pudding_counts = count_cards(player_cards, card_type=cls)
        max_scores = split_score(card_counts=pudding_counts, target_count=max(pudding_counts.values()), score=6)
        if len(player_cards) == 2:
            return max_scores  # no negative scores applied when # players == 2
        min_scores = split_score(card_counts=pudding_counts, target_count=min(pudding_counts.values()), score=-6)
        return sum_scores(min_scores, max_scores)


class NonPersistentPuddingCard(PuddingCard):
    persistent = False


class ChopSticksCard(Card):

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def score(cls, player_cards, end_game, end_round):
        return {player: 0 for player in player_cards.keys()}
