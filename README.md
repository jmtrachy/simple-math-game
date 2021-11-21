# Fun Math game
This game emulates a game I used to play as a kid called Monster Math. The whole point of the game was to try and
answer as many addition, subtraction, multiplication, or division questions as you could in one minute.
The more questions you got right, the more of an ASCII monster was drawn on the screen.

While the gameplay in this version is almost identical there are also some experimental features at work such as
history persistence, player identification, and a more random set of images. Expect this to change wildly
as hopefully it continues to grow - which should continue as long as my kids continue to play it.

### How to run
I _think_ the minimum version for this is python 3.5 because of typing, but really haven't explored versions yet.
Development was primarily done in 3.9.7.

To run simply type:
```
python3 fun_math.py
```

To change any of the runtime values (player names, time per game) look in the `fun_math.py` file and change the
constants (values starting with `__`) at the top of the file.

### Saving history
Right now history saving is super basic, something that was thrown together in an hour to try and see how the kids were
doing. Eventually things are going to have to change, for example it shouldn't be loading the entire history of all
their games into memory just to save one new game.

Eventually it should do things like print their personal record, show averages and whatnot, we'll see.

### Points
The points system is a total mess, but the goal is to tie points to some sort of rewards system. Half the reason history
is getting stored is so some analysis can be done on how the point system works and what makes the most sense.
