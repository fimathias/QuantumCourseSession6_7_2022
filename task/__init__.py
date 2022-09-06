from otree.api import *
import numpy
# If an error happens when importing numpy (a red line under "numpy"), type "pip install numpy" in Terminal


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    list_risk_choice = ['win', 'loss']  # Define the possible outcomes of the game


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        list_risk_seq = C.list_risk_choice.copy()  # Call the list you defined, ['win', 'loss']

        # Randomly draw one from 'win' and 'loss', with probability 0.33 an 0.67, respectively
        # You need to import numpy to randomly draw
        p.participant.vars['risk_outcome'] = numpy.random.choice(list_risk_seq, p=[0.33, 0.67])

        # Define participant var to attach the drawn outcome to a subject.
        # This is to help call/use the var for a subject in other apps in the same project.
        p.risk_outcome = p.participant.vars['risk_outcome']


class Player(BasePlayer):
    risk_choice = models.IntegerField(blank=True)
    risk_outcome = models.StringField(blank=True)


# PAGES
class Task(Page):
    form_model = 'player'
    form_fields = ['risk_choice']


class Outcome(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):  # Define the variables that are used in page template.
        if player.risk_outcome == 'win':
            outcome = 100 + player.risk_choice * 2.5  # Assign value to outcome when a subject wins.
        else:
            outcome = 100 - player.risk_choice  # Assign value to outcome when a subject loses.
        return {  # Return variables with the values that you have defined. 'var_name': local_variable
            'outcome': outcome
        }


page_sequence = [Task, Outcome]
