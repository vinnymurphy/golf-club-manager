# This is where the magic happens to update a player's handicap
from decimal import Decimal
from operator import itemgetter

from .models import Player, Game, GameType, GameScore


def handicap_calculator(player, score, gametype):
    handicap = player.handicap

    if score >= gametype.level_4:
        handicap_change = gametype.level_4_result
    elif gametype.level_3_min <= score <= gametype.level_3_max:
        handicap_change = gametype.level_3_result
    elif gametype.level_2_min <= score <= gametype.level_2_max:
        handicap_change = gametype.level_2_result
    elif gametype.level_1 >= score:
        handicap_change = gametype.level_1_result

    # Checks if the handicap should be increased or decreased to ensure
    # that the updated handicap never exceeds 44.6
    if (handicap_change + handicap) >= Decimal(44.6):
        new_handicap = Decimal(44.6)
        handicap_change = new_handicap - handicap
    else:
        new_handicap = handicap + handicap_change

    return new_handicap, handicap_change


def stableford_award_calculator(scores_list):
    """
    Receives a list of all active players, and all of their scores within the
    period defined by the user. For each player, identifies the top 6 scores
    achieved, calculates the average of those 6 scores, and returns a dictionary
    with "player":"average score" in descending order
    """
    results_list = []

    for item in scores_list:
        for player, scores in item.items():
            # Arrange scores in descending order
            sorted_scores = sorted(scores, reverse=True)

            if len(sorted_scores) < 6:
                break
                # Copy list and only keep the first 6 values
            top_six_scores = sorted_scores[: 6 or None]

            total = sum(top_six_scores)
            results_list.append(
                {"player": player.full_name_lastfirst, "result": total}
            )

    return sorted(results_list, key=lambda x: x["result"], reverse=True)
