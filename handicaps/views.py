from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from django.db import IntegrityError, transaction
import collections


from .models import Player, GameType, GameScore, Game, Grade
from .forms import NewGameTypeForm, NewPlayerForm, NewGameForm, \
    NewGameScoreForm, EditPlayerForm, GradeForm
from .calculator import handicap_calculator


def player_list(request):
    players = Player.objects.filter(active=True).order_by('last_name')
    
    context = {
        'players': players,
    }
    
    return render(request, 'handicaps/player_list.html', context)

@login_required    
def game(request):
    players = Player.objects.filter(active=True).order_by('last_name')
    
    GameScoreFormSet = formset_factory(NewGameScoreForm, extra=0)
    
    if request.method == "POST":
        game_form = NewGameForm(request.POST)
        score_formset = GameScoreFormSet(request.POST)
        
        if game_form.is_valid() and score_formset.is_valid():
            # Save game info
            game = game_form.save()
            
            # Save the data for each player and score in the formset
            new_scores = []
            update_players = []
            
            for score_form in score_formset:
                player = score_form.cleaned_data.get('player')
                score = score_form.cleaned_data.get('score')
                
                if player and score:
                    if score == 0:
                        break
                    else:
                        new_scores.append(GameScore(player=player, 
                            game=game, score=score))
                        
                        # Get new handicap values
                        calc_result = handicap_calculator(player, score, 
                            game.game_type)
                        
                        player.handicap = calc_result[0]
                        player.latest_handicap_change = calc_result[1]
                        player.latest_game = game.game_date
                        
                        player.save()
                    
            try:
                with transaction.atomic():
                    GameScore.objects.bulk_create(new_scores)
                    messages.success(request, 'New game saved.')
                    return redirect('player_list')
            
            except IntegrityError: # If the transaction failed
                messages.error(request,
                    'There was an error saving the game.')
                return redirect('game')
        else:
            messages.error(request,
                'There was an error in the data provided.')
            return redirect('game') # Temp to identify fail point
    else:
        new_game_form = NewGameForm()
        score_formset = GameScoreFormSet(initial=[{'player': player, 'score': 0}
            for player in players
        ])
        
        context = {
            'game_form': new_game_form,
            'score_formset': score_formset,
        }
        
        return render(request, 'handicaps/game.html', context)

def settings(request):
    gametypes = GameType.objects.filter(active=True).order_by(
        'create_date')
    context = {
        'gametypes': gametypes,
    }
    
    return render(request, 'handicaps/settings.html', context)

@login_required    
def new_game_type(request):
    if request.method == "POST":
        form = NewGameTypeForm(request.POST)
        if form.is_valid():
            gametype = form.save()
            gametype.create_date = timezone.now()
            gametype.active = True
            return redirect('settings')
    else:
        new_game_type_form = NewGameTypeForm()
        context = {
            'form': new_game_type_form,
        }
        
        return render(request, 'handicaps/new_game_type.html',
            context)

@login_required
def edit_game_type(request, pk):
    gametype = get_object_or_404(GameType, pk=pk)
    
    if request.method == "POST":
        form = NewGameTypeForm(request.POST, instance=gametype)
        if form.is_valid():
            gametype = form.save()
            return redirect('settings')
        # else:
        #     return redirect('settings')
    else:
        edit_game_type_form = NewGameTypeForm(instance=gametype)
        context = {
            'form': edit_game_type_form,
        }
        
        return render(request, 'handicaps/edit_game_type.html', context)

@login_required            
def new_player(request):
    if request.method == "POST":
        form = NewPlayerForm(request.POST)
        if form.is_valid():
            player = form.save()
            return redirect('player_list')
    else:
        new_player_form = NewPlayerForm()
        context = {
            'form': new_player_form,
        }
        
        return render(request, 'handicaps/new_player.html', context)

@login_required
def edit_player(request, pk):
    player = get_object_or_404(Player, pk=pk)
    
    if request.method == "POST":
        form = EditPlayerForm(request.POST, instance=player)
        if form.is_valid():
            player = form.save()
            return redirect('player_list')
    else:
        edit_player_form = EditPlayerForm(instance=player)
        context = {
            'form': edit_player_form,
        }
        
        return render(request, 'handicaps/edit_player.html', context)

def game_list(request):
    games = Game.objects.order_by('-game_date')
    
    return render(request, 'handicaps/game_list.html', {'games': games})
    
def inactive_players(request):
    players = Player.objects.filter(active=False).order_by('last_name')
    
    context = {
        'players': players,
    }
    
    return render(request, 'handicaps/inactive_players.html', context)
    
def grade(request):
    grades = Grade.objects.get(pk=1)
    
    grade_dict = collections.OrderedDict()
    a_dict = collections.OrderedDict()
    b_dict = collections.OrderedDict()
    c_dict = collections.OrderedDict()
    d_dict = collections.OrderedDict()
    e_dict = collections.OrderedDict()
    
    a_dict = {
        player.full_name_lastfirst: player.rounded for player in Player.objects.filter(
        active=True,
        handicap_rounded__gte = grades.grade_a_min,
        handicap_rounded__lte = grades.grade_a_max
        ).order_by('last_name')
    }
    
    b_dict = {
        player.full_name_lastfirst: player.rounded for player in Player.objects.filter(
        active=True,
        handicap_rounded__gte = grades.grade_b_min,
        handicap_rounded__lte = grades.grade_b_max
        ).order_by('last_name')
    }
    
    c_dict = {
        player.full_name_lastfirst: player.rounded for player in Player.objects.filter(
        active=True,
        handicap_rounded__gte = grades.grade_c_min,
        handicap_rounded__lte = grades.grade_c_max
        ).order_by('last_name')
    }
    
    d_dict = {
        player.full_name_lastfirst: handicap_rounded for player in Player.objects.filter(
        active=True,
        handicap_rounded__gte = grades.grade_d_min,
        handicap_rounded__lte = grades.grade_d_max
        ).order_by('last_name')
    }
    
    e_dict = {
        player.full_name_lastfirst: player.rounded for player in Player.objects.filter(
        active=True,
        handicap_rounded__gte = grades.grade_e_min,
        handicap_rounded__lte = grades.grade_e_max
        ).order_by('last_name')
    }
    
    a_ordered = collections.OrderedDict(sorted(a_dict.items(), key=lambda t: t[0]))
    b_ordered = collections.OrderedDict(sorted(b_dict.items(), key=lambda t: t[0]))
    c_ordered = collections.OrderedDict(sorted(c_dict.items(), key=lambda t: t[0]))
    d_ordered = collections.OrderedDict(sorted(d_dict.items(), key=lambda t: t[0]))
    e_ordered = collections.OrderedDict(sorted(e_dict.items(), key=lambda t: t[0]))
    
    if grades.grade_use == 3:
        grade_dict['A'] = a_ordered
        grade_dict['B'] = b_ordered
        grade_dict['C'] = c_ordered
    elif grades.grade_use == 4:
        grade_dict['A'] = a_dict
        grade_dict['B'] = b_dict
        grade_dict['C'] = c_dict
        grade_dict['D'] = d_dict
    else:
        grade_dict['A'] = a_dict
        grade_dict['B'] = b_dict
        grade_dict['C'] = c_dict
        grade_dict['D'] = d_dict
        grade_dict['E'] = e_dict
    
    context = {
        'grades': grades,
        'grade_dict': grade_dict,
        'a_dict': a_dict,
    }
    
    return render(request, 'handicaps/grade.html', context)
    
def config_grade(request):
    grade = Grade.objects.get(pk=1)
    
    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save()
            return redirect('grade')
    else:
        grade_form = GradeForm(instance=grade)

        context = {
            'form': grade_form,
        }
            
        return render(request, 'handicaps/config_grade.html', context)