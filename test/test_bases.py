import sys
from pathlib import Path

path = Path().cwd()
sys.path.insert(0, str(path))
sys.path.insert(1, str(path / 'src'))

from grab_wall import do_stuff

def test_passing():
    assert (1, 2, 3) == (1, 2, 3)

def test_dry_run():
    print('sdasdasd')
    assert do_stuff(infinite=False) == None
