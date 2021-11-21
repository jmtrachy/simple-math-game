import art
from dal import record_results
from model import AdditionQuestion, DivisionQuestion, GameResults, MultiplicationQuestion, \
    Question, QuestionResult, SubtractionQuestion
import time
from typing import List


def current_milli_time():
    return round(time.time() * 1000)


__player_1__: str = 'Lauren'
__player_2__: str = 'Carter'
__player_3__: str = 'James'


__ADDITION__: str = 'Addition'
__SUBTRACTION__: str = 'Subtraction'
__MULTIPLICATION__: str = 'Multiplication'
__DIVISION__: str = 'Division'

__NUM_SECONDS__ = 60


class Game:
    def __init__(self):
        self.game = None
        self.difficulty = None
        self.questions = []
        self.score = None
        self.player = Game.pick_player()

    @staticmethod
    def print_new_screen():
        newlines = ''
        if newlines == '':
            for j in range(1, 100):
                newlines += '\n'

        print(newlines)

    @staticmethod
    def pick_player() -> str:
        Game.print_new_screen()
        print('Who is playing right now?')
        print('1) {}'.format(__player_1__))
        print('2) {}'.format(__player_2__))
        player_str = input('Type the number for the player and hit enter: ')

        try:
            player = int(player_str)
            if player < 1 or player > 3:
                return Game.pick_player()

            if player == 1:
                return __player_1__.lower()
            elif player == 2:
                return __player_2__.lower()
            elif player == 3:
                return __player_3__.lower()
        except:
            return Game.pick_player()

    def choose_game(self):
        Game.print_new_screen()

        print('What type of game would you like to play? Options are: ')
        print('1) {}'.format(__ADDITION__))
        print('2) {}'.format(__SUBTRACTION__))
        print('3) {}'.format(__MULTIPLICATION__))
        print('4) {}'.format(__DIVISION__))
        game_input = int(input('Enter a number then press the return key: '))

        if game_input == 1:
            self.game = __ADDITION__
        elif game_input == 2:
            self.game = __SUBTRACTION__
        elif game_input == 3:
            self.game = __MULTIPLICATION__
        elif game_input == 4:
            self.game = __DIVISION__
        else:
            self.choose_game()

    def choose_difficulty(self):
        Game.print_new_screen()

        print('You chose {}\n'.format(self.game))
        print('How difficult would you like it to be? Please select from the following options:')
        print('1) Easiest')
        print('2) Easy')
        print('3) Medium')
        print('4) Hard')
        self.difficulty = int(input('Enter a number then press the return key: '))

        if self.difficulty > 4 or self.difficulty < 1:
            self.choose_difficulty()

    def get_question(self) -> Question:
        if self.game == __ADDITION__:
            q = AdditionQuestion(self.difficulty)
        elif self.game == __MULTIPLICATION__:
            q = MultiplicationQuestion(self.difficulty)
        elif self.game == __SUBTRACTION__:
            q = SubtractionQuestion(self.difficulty)
        elif self.game == __DIVISION__:
            q = DivisionQuestion(self.difficulty)
        else:
            q = None

        return q

    @staticmethod
    def print_single_answer_correctness(questions_asked: List[Question]):
        previous_q = questions_asked[len(questions_asked) - 1]
        if previous_q.is_correct():
            print('CORRECT!')
        else:
            print('WRONG!')
        print('\n\n')

    @staticmethod
    def calculate_score(correct_questions: List[Question]) -> int:
        total_worth = 0
        for j in range(0, len(correct_questions)):
            q = correct_questions[j]
            current_question_worth = (j + 1) * q.chosen_difficulty.point_modifier
            #print('correct question {} was worth {} points'.format(j + 1, current_question_worth))
            total_worth += current_question_worth

        return total_worth

    @staticmethod
    def print_wrong_questions(incorrect_questions: List[Question]):
        for question in incorrect_questions:
            print('For {} {} {} you answered {} but the actual answer was {}'.format(
                question.number1, question.symbol, question.number2, question.user_provided_answer, question.answer
            ))

    @staticmethod
    def get_user_answer() -> int:
        try:
            return int(input('= '))
        except ValueError:
            return Game.get_user_answer()

    def play_game(self):
        start_time = current_milli_time()
        questions_asked = []
        correct_questions = 0

        # get the art for this game
        the_art: List[str] = art.get_art_for_game()

        while current_milli_time() < start_time + (__NUM_SECONDS__ * 1000):
            Game.print_new_screen()

            # Print the art if appropriate
            if correct_questions > 0:
                if correct_questions < len(the_art):
                    print('{}\n\n'.format(the_art[correct_questions]))
                else:
                    print('{}\n\n'.format(the_art[len(the_art) - 1]))

            if len(questions_asked) > 0:
                Game.print_single_answer_correctness(questions_asked)

            # Print out the number of seconds remaining to add a little pressure
            seconds_left = int((start_time + (__NUM_SECONDS__ * 1000) - current_milli_time()) / 1000)
            print('{} seconds left\n\n'.format(seconds_left))

            q = self.get_question()
            q.print_problem()

            q.user_provided_answer = Game.get_user_answer()
            questions_asked.append(q)
            if q.is_correct():
                correct_questions += 1

        Game.print_single_answer_correctness(questions_asked)

        correct_questions = [
            question
            for question in questions_asked
            if question.is_correct()
        ]

        incorrect_questions = [
            question
            for question in questions_asked
            if not question.is_correct()
        ]

        print('You were able to get {} questions right, and {} questions wrong in {} seconds'.format(
            len(correct_questions), len(incorrect_questions), __NUM_SECONDS__))
        Game.print_wrong_questions(incorrect_questions)

        calculated_score = Game.calculate_score(correct_questions)
        print('\n\nThat\'s worth {} points!'.format(calculated_score))

        # Convert the questions into the data storage model
        storage_corrects: List[QuestionResult] = \
            [GameResults.convert_question_for_storage(q, self.difficulty) for q in correct_questions]
        storage_incorrects: List[QuestionResult] = \
            [GameResults.convert_question_for_storage(q, self.difficulty) for q in incorrect_questions]

        game_results = GameResults(
            storage_corrects,
            storage_incorrects,
            self.game,
            self.difficulty,
            __NUM_SECONDS__,
            calculated_score
        )
        record_results(self.player, game_results)


def play_game(g: Game):
    """
    A simple method for executing gameplay. It keeps the player selection the same, but allows for selecting
    different games
    """
    playing_game = True
    while playing_game:
        g.choose_game()
        g.choose_difficulty()
        g.play_game()

        play_another = input('Would you like to play again? Enter \'y\' for yes or \'n\' for no: ')
        if play_another.lower() != 'y':
            playing_game = False


if __name__ == '__main__':
    g = Game()
    play_game(g)

