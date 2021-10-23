from abc import ABC
import random
import time
from typing import List, Optional


def current_milli_time():
    return round(time.time() * 1000)


class Difficulty:
    def __init__(self,
                 x_min: int,
                 x_max: int,
                 y_min: int,
                 y_max: int,
                 point_modifier: int = 1):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.point_modifier = point_modifier


class Question(ABC):
    def __init__(self, difficulty):
        self.__user_provided_answer = None
        self.__answer = None
        self.__symbol = None

        # Grab the difficulty from the list and create the numbers
        self.__chosen_difficulty: Difficulty = self.difficulties[difficulty - 1]
        numbers: (int, int) = self.get_numbers(self.__chosen_difficulty)

        self.__number1: int = numbers[0]
        self.__number2: int = numbers[1]

    def get_numbers(self, d: Difficulty) -> (int, int):
        number1: int = random.randint(d.x_min, d.x_max)
        number2: int = random.randint(d.y_min, d.y_max)

        return number1, number2

    @property
    def chosen_difficulty(self) -> Difficulty:
        return self.__chosen_difficulty

    @chosen_difficulty.setter
    def chosen_difficulty(self, value: Difficulty):
        self.__chosen_difficulty = value

    @property
    def difficulties(self) -> Optional[List[Difficulty]]:
        return self.__difficulties

    @difficulties.setter
    def difficulties(self, value: Optional[List[Difficulty]]):
        self.__difficulties = value

    @property
    def answer(self):
        return self.__answer

    @answer.setter
    def answer(self, value):
        self.__answer = value

    @property
    def user_provided_answer(self):
        return self.__user_provided_answer

    @user_provided_answer.setter
    def user_provided_answer(self, value):
        self.__user_provided_answer = value

    @property
    def symbol(self):
        return self.__symbol

    @symbol.setter
    def symbol(self, value):
        self.__symbol = value

    @property
    def number1(self):
        return self.__number1

    @number1.setter
    def number1(self, value):
        self.__number1 = value

    @property
    def number2(self):
        return self.__number2

    @number2.setter
    def number2(self, value):
        self.__number2 = value

    def print_problem(self):
        print('  {}'.format(self.number1))
        print('{} {}'.format(self.symbol, self.number2))

    def is_correct(self):
        return self.answer == self.user_provided_answer


class AdditionQuestion(Question):
    @property
    def answer(self):
        return self.number1 + self.number2

    @property
    def symbol(self):
        return '+'

    @property
    def difficulties(self) -> Optional[List[Difficulty]]:
        return [
            Difficulty(1, 20, 1, 20),
            Difficulty(1, 100, 1, 200, 2),
            Difficulty(1, 500, 1, 500, 4),
            Difficulty(1, 1000, 100, 1000, 6)
        ]


class MultiplicationQuestion(Question):
    @property
    def answer(self):
        return self.number1 * self.number2

    @property
    def symbol(self):
        return 'x'

    @property
    def difficulties(self) -> Optional[List[Difficulty]]:
        return [
            Difficulty(1, 10, 1, 10, 2),
            Difficulty(1, 12, 1, 12, 3),
            Difficulty(1, 15, 1, 15, 5),
            Difficulty(1, 20, 1, 20, 7)
        ]


class SubtractionQuestion(Question):
    @property
    def answer(self):
        return self.number1 - self.number2

    @property
    def symbol(self):
        return '-'

    @property
    def difficulties(self) -> Optional[List[Difficulty]]:
        return [
            Difficulty(1, 20, 1, 20),
            Difficulty(1, 100, 1, 100, 2),
            Difficulty(1, 1000, 1, 100, 4),
            Difficulty(1, 1000, 1, 1000, 6)
        ]

    def get_numbers(self, d: Difficulty) -> (int, int):
        number1: int = random.randint(d.x_min, d.x_max)
        number2: int = random.randint(d.y_min, d.y_max)

        if number1 > number2:
            return number1, number2
        else:
            return self.get_numbers(d)


class DivisionQuestion(Question):
    @property
    def answer(self):
        return int(self.number1 / self.number2)

    @property
    def symbol(self):
        return '÷'

    @property
    def difficulties(self) -> Optional[List[Difficulty]]:
        return [
            Difficulty(1, 10, 1, 10, 2),
            Difficulty(1, 12, 1, 12, 4),
            Difficulty(1, 15, 1, 15, 6),
            Difficulty(1, 20, 1, 20, 8)
        ]

    def get_numbers(self, d: Difficulty) -> (int, int):
        number1: int = random.randint(d.x_min, d.x_max)
        number2: int = random.randint(d.y_min, d.y_max)
        denominator = number1 * number2

        return denominator, number1


__ADDITION__ = 'Addition'
__SUBTRACTION__ = 'Subtraction'
__MULTIPLICATION__ = 'Multiplication'
__DIVISION__ = 'Division'

__NUM_SECONDS__ = 10


class Game:
    def __init__(self):
        self.game = None
        self.difficulty = None
        self.questions = []
        self.score = None

    @staticmethod
    def print_new_screen():
        for j in range(1, 100):
            print('')

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
            print('correct question {} was worth {} points'.format(j + 1, current_question_worth))
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

        while current_milli_time() < start_time + (__NUM_SECONDS__ * 1000):
            Game.print_new_screen()
            if len(questions_asked) > 0:
                Game.print_single_answer_correctness(questions_asked)

            # Print out the number of seconds remaining to add a little pressure
            seconds_left = int((start_time + (__NUM_SECONDS__ * 1000) - current_milli_time()) / 1000)
            print('{} seconds left\n\n'.format(seconds_left))

            q = self.get_question()
            q.print_problem()

            q.user_provided_answer = Game.get_user_answer()
            questions_asked.append(q)

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

        print('\n\nThat\'s worth {} points!'.format(Game.calculate_score(correct_questions)))


if __name__ == '__main__':

    g = Game()
    g.choose_game()
    g.choose_difficulty()
    g.play_game()

