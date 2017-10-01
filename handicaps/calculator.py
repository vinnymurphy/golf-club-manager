# This is where the magic happens to update a player's handicap
from decimal import Decimal
from operator import itemgetter

from .models import Player, Game, GameType, GameScore

def handicap_calculator(player, score, gametype):
    # Initialize values
    handicap = player.handicap

    if score >= gametype.level_4:
        # Checks if the handicap should be increased or decreased to ensure
        # that the updated handicap never exceeds 44.5
        if gametype.level_4_result > 0:
            if handicap + gametype.level_4_result >= Decimal(44.5):
                new_handicap = Decimal(44.5)
            else:
                new_handicap = handicap + gametype.level_4_result
        else:
            new_handicap = handicap + gametype.level_4_result
    elif gametype.level_3_min <= score <= gametype.level_3_max:
        new_handicap = handicap + gametype.level_3_result
    elif gametype.level_2_min <= score <= gametype.level_2_max:
        new_handicap = handicap + gametype.level_2_result
    elif gametype.level_1 >= score:
        if gametype.level_1_result > 0:
            if handicap + gametype.level_1_result >= Decimal(44.5):
                new_handicap = Decimal(44.5)
            else:
                new_handicap = handicap + gametype.level_1_result
        else:
            new_handicap = handicap + gametype.level_1_result

    handicap_change = new_handicap - handicap

    return new_handicap, handicap_change

def stableford_award_calculator(scores_list):
    '''
    Receives a list of all active players, and all of their scores within the
    period defined by the user. For each player, identifies the top 6 scores
    achieved, calculates the average of those 6 scores, and returns a dictionary
    with "player":"average score" in descending order
    '''
    results_list = []

    for item in scores_list:
        for player, scores in item.items():
            name = player.full_name_lastfirst
            # Arrange scores in descending order
            sorted_scores = sorted(scores, reverse=True)

            if len(sorted_scores) < 6:
                break
            else:
                # Copy list and only keep the first 6 values
                top_six_scores = sorted_scores[0:6 or None]

                total = 0
                for score in top_six_scores:
                    total += score

                average_score = total / len(top_six_scores)
                result = round(average_score, 2)

                results_list.append({'player': name, 'result': result})

    results_list_descending = sorted(
        results_list, key=lambda x:x['result'], reverse=True
    )

    return results_list_descending
