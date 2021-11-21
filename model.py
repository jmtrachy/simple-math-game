from abc import ABC
import random
from typing import List, Optional


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


class QuestionResult:
    def __init__(self,
                 question_type: str,
                 difficulty: int,
                 number1: int,
                 number2: int,
                 answer: int,
                 user_provided_answer: int):
        self.question_type = question_type
        self.difficulty = difficulty
        self.number1 = number1
        self.number2 = number2
        self.answer = answer
        self.user_provided_answer = user_provided_answer


class GameResults:
    def __init__(self,
                 correct_questions: List[QuestionResult],
                 incorrect_questions: List[QuestionResult],
                 game: str,
                 difficulty: int,
                 num_seconds: int,
                 points: int):
        self.correct_questions = correct_questions
        self.incorrect_questions = incorrect_questions
        self.game = game
        self.difficulty = difficulty
        self.num_seconds = num_seconds
        self.points = points

    @staticmethod
    def convert_question_for_storage(q: Question, difficulty: int) -> QuestionResult:
        return QuestionResult(
            str(type(q)),
            difficulty,
            q.number1,
            q.number2,
            q.answer,
            q.user_provided_answer
        )
