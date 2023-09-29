from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'background'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    gender_option = [('male', 'male'), ('female', 'female'), ('non_binary', 'non-binary')]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        gender_option = C.gender_option.copy()
        random.shuffle(gender_option)
        p.participant.vars['gender_seq'] = gender_option

        # Manually record the order of options one by one
        p.gender_seq0 = gender_option[0][0]
        p.gender_seq1 = gender_option[1][0]
        p.gender_seq2 = gender_option[2][0]

        # More efficiently, use a loop to record the order of options
        # for i in range(0, 3):
        #     str_gender = 'gender_seq%s' % i
        #     setattr(p, str_gender, gender_option[i][0])


class Player(BasePlayer):
    birth_year = models.IntegerField(
        label='In which year are you born?',
        blank=True
    )
    gender = models.StringField(
        # choices=[('male', 'male'), ('female', 'female'), ('non_binary', 'non-binary')],
        widget=widgets.RadioSelect,
        label='What is your gender?',
        blank=True
    )
    gender_seq0 = models.StringField(
        blank=True
    )
    gender_seq1 = models.StringField(
        blank=True
    )
    gender_seq2 = models.StringField(
        blank=True
    )
    education = models.StringField(
        label='What was your level of education? '
              'Please choose the option that best describes the highest level of education you had completed.',
        widget=widgets.RadioSelect,
        choices=[('lower_secondary', 'Lower secondary education'),
                 ('upper_secondary', 'Upper secondary level education'),
                 ('bachelor', 'Bachelor\'s or equivalent level'),  # Use \ if there is ' in the string
                 ('master', 'Master\'s or equivalent level or doctoral level'),
                 ('no_answer', 'Prefer not to answer')],
        blank=True
    )


def gender_choices(player):
    choices = player.participant.vars['gender_seq']
    return choices


# PAGES
class Demographic(Page):
    form_model = 'player'  # Always need this line
    form_fields = ['birth_year', 'gender', 'education']  # Include all form fields that are included in the page

    @staticmethod
    def error_message(player: Player, values):
        if not values['birth_year'] or not values['gender'] or not values['education']:
            return 'Please answer all questions.'  # Return an error message when any of the questions is not answered.
        elif not (1900 <= values['birth_year'] <= 2023):
            return 'Please input a sensible birth year'


page_sequence = [Demographic]
