import copy
from model import GameResults, QuestionResult
import json
from json import JSONEncoder
from typing import List


def record_results(player: str, results: GameResults):
    file_name: str = '{}.json'.format(player)

    previous_results: List[GameResults] = get_results(file_name)
    full_results = copy.deepcopy(previous_results)
    full_results.append(results)

    if full_results is not None:

        # serialize the list of results into json
        game_results_json = json.dumps(obj=full_results, indent=4, cls=GameResultsListEncoder)

        # Retrieve the current version of results
        with open('{}.json'.format(player), 'w') as file:
            file.write(game_results_json)


class GameResultsDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if 'question_type' in obj:
            return QuestionResult(**obj)
        elif 'correct_questions' in obj:
            return GameResults(**obj)
        else:
            return obj


def get_results(file_name: str) -> List[GameResults]:
    try:
        with open(file_name, 'r') as file:
            #return json.loads(file.read(), object_hook=lambda d: GameResults(**d))
            return json.loads(file.read(), cls=GameResultsDecoder)

    except FileNotFoundError:
        return []


class GameResultsListEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


if __name__ == '__main__':
    game_result = GameResults([], [], "tough", 3, 50, 4)
    gs: List[GameResults] = [game_result]

    print(get_results('james.json'))
    record_results('james', game_result)
    print(get_results('james.json'))
