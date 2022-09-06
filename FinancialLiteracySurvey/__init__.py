from otree.api import *


author = 'Marco'

doc = """
A survey of questions about financial literacy.
"""


class C(BaseConstants):
    NAME_IN_URL = 'FinancialLiteracySurvey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    question1 = models.IntegerField(
        label="Suppose you had $100 in a savings account and the interest rate was 2% per year."
              " After 5 years, how much do you think you would have in the account if you left the money to grow?",
        choices=[
            [1, 'More than $102'],
            [2, 'Exactly $102'],
            [3, 'Less than $102'],
            [9, 'Don`t know'],
            [0, 'Prefer not to say'],
        ],
        widget=widgets.RadioSelect
    )
    question2 = models.IntegerField(
        label="Imagine that the interest rate on your savings account was 1% per year and inflation was 2% per year. "
              "After 1 year, how much would you be able to buy with the money in this account?",
        choices=[
            [1, 'More than today'],
            [2, 'Exactly the same'],
            [3, 'Less than today'],
            [9, 'Don’t know'],
            [0, 'Prefer not to say'],
        ],
        widget=widgets.RadioSelect
    )
    question5 = models.IntegerField(
        label="Buying a single company’s stock usually provides a safer return than a stock mutual fund.",
        choices=[
            [1, 'True'],
            [2, 'False'],
            [9, 'Don’t know'],
            [0, 'Prefer not to say'],
        ],
        widget=widgets.RadioSelect
    )

    q_correct = models.IntegerField()

    def count_correct(self):
        self.q_correct = 0
        if self.question1 == 1:
            self.q_correct = self.q_correct + 1
        if self.question2 == 3:
            self.q_correct = self.q_correct + 1
        if self.question5 == 2:
            self.q_correct = self.q_correct + 1


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question5']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.count_correct()


class Results(Page):
    form_model = 'player'


page_sequence = [MyPage, Results]
