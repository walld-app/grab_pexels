import sys

sys.path.insert(0, '..') # TODO BAD

from src.grab_wall import do_stuff

def test_passing():
    assert (1, 2, 3) == (1, 2, 3)

def dry_run():
    do_stuff(infinite=False)
