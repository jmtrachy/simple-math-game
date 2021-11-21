from mickey import mickey_mouse
from reaper import grim_reaper
import random
from typing import List


artworks: List[List[str]] = [
    mickey_mouse,
    grim_reaper
]


def get_art_for_game() -> List[str]:
    return artworks[random.randint(0, len(artworks) - 1)]


if __name__ == '__main__':

    art = get_art_for_game()
    step = 0

    for stage in art:
        step += 1
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
              '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print(stage)
        input('currenty on step {} of {}...more'.format(step, len(art)))