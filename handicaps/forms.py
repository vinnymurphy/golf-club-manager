from django import forms
from .models import GameType, Player, Game, GameScore, Grade
from django.forms.formsets import BaseFormSet

class NewGameTypeForm(forms.ModelForm):
    class Meta:
        model = GameType
        fields = ('name', 'level_4', 'level_4_result',
                'level_3_min', 'level_3_max', 'level_3_result',
                'level_2_min', 'level_2_max', 'level_2_result',
                'level_1', 'level_1_result')

class NewPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'handicap')

class EditPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'handicap', 'active')

class NewGameForm(forms.ModelForm):
    game_type = forms.ModelChoiceField(
        queryset=GameType.objects, empty_label=None
    )

    class Meta:
        model = Game
        fields = ('game_date', 'game_type')
        widgets = {
            'game_date': forms.DateInput(attrs={'type': 'date'})
        }

class NewGameScoreForm(forms.ModelForm):
    player = forms.ModelChoiceField(
        queryset=Player.objects, empty_label=None
    )

    class Meta:
        model = GameScore
        fields = ('player', 'score')

    def __init__(self, *args, **kwargs):
        super(NewGameScoreForm, self).__init__(*args, **kwargs)
        self.fields['score'].widget.attrs['style'] = 'width: 60'
        self.fields['player'].widget.attrs['style'] = 'width: 180'

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('grade_use', 'grade_a_min', 'grade_a_max', 'grade_b_min',
            'grade_b_max', 'grade_c_min', 'grade_c_max', 'grade_d_min',
            'grade_d_max', 'grade_e_min', 'grade_e_max')

class EditGameScoreForm(forms.ModelForm):
    class Meta:
        model = GameScore
        fields = ('score', 'attendance')
