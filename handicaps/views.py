from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.db.models import Avg, Sum
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .calculator import handicap_calculator, stableford_award_calculator
from .forms import (
    AttendanceForm,
    EditGameScoreForm,
    EditPlayerForm,
    GradeForm,
    NewGameForm,
    NewGameScoreForm,
    NewGameTypeForm,
    NewPlayerForm,
)
from .grade import get_graded_list
from .models import Game, GameScore, GameType, Grade, Player


@login_required
def player_list(request):
    players = Player.objects.filter(active=True).order_by("last_name")

    context = {
        "players": players,
    }

    return render(request, "handicaps/player_list.html", context)


@login_required
def game(request):
    players = Player.objects.filter(active=True).order_by("last_name")

    GameScoreFormSet = formset_factory(NewGameScoreForm, extra=0)

    if request.method == "POST":
        game_form = NewGameForm(request.POST)
        score_formset = GameScoreFormSet(request.POST)

        if game_form.is_valid() and score_formset.is_valid():
            # Save game info
            game = game_form.save()

            # Save the data for each player and score in the formset
            new_scores = []

            if game.game_type.name == "Fun match":
                for score_form in score_formset:
                    player = score_form.cleaned_data.get("player")
                    score = score_form.cleaned_data.get("score")
                    attendance = score_form.cleaned_data.get("attendance")

                    if player and score:
                        if score == 0:
                            break
                        new_scores.append(
                            GameScore(
                                player=player,
                                game=game,
                                score=None,
                                handicap=player.handicap,
                                handicap_change=0.0,
                                attendance=attendance,
                            )
                        )

                        player.latest_game = game.game_date
                        player.save()
            else:
                for score_form in score_formset:
                    player = score_form.cleaned_data.get("player")
                    score = score_form.cleaned_data.get("score")
                    attendance = score_form.cleaned_data.get("attendance")

                    if player and score:
                        if score == 0:
                            break
                        # Get new handicap values
                        calc_result = handicap_calculator(
                            player, score, game.game_type
                        )

                        new_scores.append(
                            GameScore(
                                player=player,
                                game=game,
                                score=score,
                                handicap=player.handicap,
                                handicap_change=calc_result[1],
                                attendance=attendance,
                            )
                        )

                        player.handicap = calc_result[0]
                        player.latest_handicap_change = calc_result[1]
                        player.latest_game = game.game_date

                        player.save()

            try:
                with transaction.atomic():
                    GameScore.objects.bulk_create(new_scores)
                    messages.success(request, "New game saved.")
                    return redirect("player_list")

            except IntegrityError:  # If the transaction failed
                messages.error(request, "There was an error saving the game.")
                return redirect("game")
        else:
            messages.error(
                request, "There was an error in the data provided."
            )
            return redirect("game")  # Temp to identify fail point
    else:
        new_game_form = NewGameForm()
        score_formset = GameScoreFormSet(
            initial=[{"player": player, "score": 0} for player in players]
        )

        context = {
            "game_form": new_game_form,
            "score_formset": score_formset,
        }

        return render(request, "handicaps/game.html", context)


@login_required
def settings(request):
    gametypes = GameType.objects.filter(active=True).order_by("create_date")
    context = {
        "gametypes": gametypes,
    }

    return render(request, "handicaps/settings.html", context)


@login_required
def new_game_type(request):
    if request.method == "POST":
        form = NewGameTypeForm(request.POST)
        if form.is_valid():
            gametype = form.save()
            gametype.create_date = timezone.now()
            gametype.active = True
            return redirect("settings")
    else:
        new_game_type_form = NewGameTypeForm()
        context = {
            "form": new_game_type_form,
        }

        return render(request, "handicaps/new_game_type.html", context)


@login_required
def edit_game_type(request, pk):
    gametype = get_object_or_404(GameType, pk=pk)

    if request.method == "POST":
        form = NewGameTypeForm(request.POST, instance=gametype)
        if form.is_valid():
            gametype = form.save()
            return redirect("settings")
        # else:
        #     return redirect('settings')
    else:
        edit_game_type_form = NewGameTypeForm(instance=gametype)
        context = {
            "form": edit_game_type_form,
        }

        return render(request, "handicaps/edit_game_type.html", context)


@login_required
def new_player(request):
    if request.method == "POST":
        form = NewPlayerForm(request.POST)
        if form.is_valid():
            player = form.save()
            return redirect("player_list")
    else:
        new_player_form = NewPlayerForm()
        context = {
            "form": new_player_form,
        }

        return render(request, "handicaps/new_player.html", context)


@login_required
def edit_player(request, pk):
    player = get_object_or_404(Player, pk=pk)

    if request.method == "POST":
        form = EditPlayerForm(request.POST, instance=player)
        if form.is_valid():
            player = form.save()
            return redirect("player_list")
    else:
        edit_player_form = EditPlayerForm(instance=player)
        context = {
            "form": edit_player_form,
        }

        return render(request, "handicaps/edit_player.html", context)


@login_required
def game_list(request):
    games = Game.objects.order_by("-game_date")

    return render(request, "handicaps/game_list.html", {"games": games})


@login_required
def expand_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    scores = GameScore.objects.filter(game=pk).order_by("player__last_name")

    context = {"game": game, "scores": scores}

    return render(request, "handicaps/expand_game.html", context)


@login_required
def inactive_players(request):
    players = Player.objects.filter(active=False).order_by("last_name")

    context = {
        "players": players,
    }

    return render(request, "handicaps/inactive_players.html", context)


@login_required
def grade(request):
    grade_dict = get_graded_list()
    context = {
        "grade_dict": grade_dict,
    }

    return render(request, "handicaps/grade.html", context)


@login_required
def config_grade(request):
    grade = Grade.objects.get(pk=1)

    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save()
            return redirect("grade")
    else:
        grade_form = GradeForm(instance=grade)

        context = {
            "form": grade_form,
        }

        return render(request, "handicaps/config_grade.html", context)


@login_required
def expand_player(request, pk):
    player = get_object_or_404(Player, pk=pk)
    game_history = GameScore.objects.filter(player=pk).order_by(
        "-game__game_date"
    )
    context = {
        "player": player,
        "game_history": game_history,
    }
    return render(request, "handicaps/expand_player.html", context)


@login_required
def edit_gamescore(request, pk):
    gamescore = get_object_or_404(GameScore, pk=pk)
    if request.method == "POST":
        form = EditGameScoreForm(request.POST, instance=gamescore)
        player = gamescore.player.id

        if form.is_valid():
            gamescore = form.save()
            return redirect("expand_player", player)
    else:
        edit_gamescore_form = EditGameScoreForm(instance=gamescore)
        context = {
            "gamescore": gamescore,
            "form": edit_gamescore_form,
        }

        return render(request, "handicaps/edit_gamescore.html", context)


@login_required
def attendance(request):
    attendance_form = AttendanceForm()
    heading = "Attendance Points"
    th = "Points"
    context = {
        "attendance_form": attendance_form,
        "heading": heading,
        "th": th,
    }
    if request.method == "GET":
        form = AttendanceForm(request.GET)
        if form.is_valid():
            start = form.cleaned_data.get("start")
            end = form.cleaned_data.get("end")

            gamescores = (
                GameScore.objects.filter(
                    game__game_date__gte=start, game__game_date__lte=end
                )
                .values("player__last_name", "player__first_name")
                .annotate(output=Sum("attendance"))
                .order_by("-output")
            )

            context |= {
                "results": gamescores,
                "start_txt": start,
                "end_txt": end,
            }

    return render(request, "handicaps/attendance.html", context)


@login_required
def stableford(request):
    attendance_form = AttendanceForm()
    heading = "Stableford Award"
    th = "Agg. Score"
    context = {
        "attendance_form": attendance_form,
        "heading": heading,
        "th": th,
    }
    if request.method == "GET":
        form = AttendanceForm(request.GET)
        if form.is_valid():
            start = form.cleaned_data.get("start")
            end = form.cleaned_data.get("end")

            scores_list = []
            players = Player.objects.filter(active=True)

            for player in players:
                gamescores = GameScore.objects.filter(
                    game__game_date__gte=start,
                    game__game_date__lte=end,
                    game__game_type=1,
                    player=player,
                )

                if gamescores:
                    scores = [score.score for score in gamescores]
                    scores_list.append({player: scores})

            results = stableford_award_calculator(scores_list)

            context |= {
                "results": results,
                "start_txt": start,
                "end_txt": end,
            }

    return render(request, "handicaps/attendance.html", context)


@login_required
def update_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    players = (
        Player.objects.filter(active=True)
        .order_by("last_name")
        .exclude(gamescore__game=pk)
    )

    GameScoreFormSet = formset_factory(NewGameScoreForm, extra=0)

    if request.method == "POST":
        score_formset = GameScoreFormSet(request.POST)

        if score_formset.is_valid():
            # Save the data for each player and score in the formset
            new_scores = []

            if game.game_type.name == "Fun match":
                for score_form in score_formset:
                    player = score_form.cleaned_data.get("player")
                    score = score_form.cleaned_data.get("score")
                    attendance = score_form.cleaned_data.get("attendance")

                    if player and score and attendance:
                        if score == 0:
                            break
                        new_scores.append(
                            GameScore(
                                player=player,
                                game=game,
                                score=None,
                                handicap=player.handicap,
                                handicap_change=0.0,
                                attendance=attendance,
                            )
                        )

                        player.latest_game = game.game_date
                        player.save()
            else:
                for score_form in score_formset:
                    player = score_form.cleaned_data.get("player")
                    score = score_form.cleaned_data.get("score")
                    attendance = score_form.cleaned_data.get("attendance")

                    if player and score:
                        if score == 0:
                            break
                        # Get new handicap values
                        calc_result = handicap_calculator(
                            player, score, game.game_type
                        )

                        new_scores.append(
                            GameScore(
                                player=player,
                                game=game,
                                score=score,
                                handicap=player.handicap,
                                handicap_change=calc_result[1],
                                attendance=attendance,
                            )
                        )

                        player.handicap = calc_result[0]
                        player.latest_handicap_change = calc_result[1]
                        player.latest_game = game.game_date

                        player.save()

            try:
                with transaction.atomic():
                    GameScore.objects.bulk_create(new_scores)
                    messages.success(request, "New game saved.")
                    return redirect("expand_game", pk=pk)

            except IntegrityError:  # If the transaction failed
                messages.error(request, "There was an error saving the game.")
        else:
            messages.error(
                request, "There was an error in the data provided."
            )
    else:
        update_game_form = GameScoreFormSet(
            initial=[{"player": player, "score": 0} for player in players]
        )

        context = {"game": game, "form": update_game_form}

        return render(request, "handicaps/update_game.html", context)


@login_required
def delete_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    gamescores = GameScore.objects.filter(game=pk)

    for gamescore in gamescores:
        player = Player.objects.get(pk=gamescore.player.id)
        player.handicap -= gamescore.handicap_change
        player.latest_handicap_change = -gamescore.handicap_change
        player.save()
        gamescore.delete()

    game.delete()
    return redirect("player_list")
