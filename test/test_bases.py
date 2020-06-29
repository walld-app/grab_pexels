import sys
from pathlib import Path
from walld_db.models import BASE, get_psql_dsn
from walld_db.helpers import DB

path = Path().cwd().parent
sys.path.insert(0, str(path))
sys.path.insert(1, str(path / 'src'))

print(sys.path)
from grab_wall import do_stuff
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DSN = get_psql_dsn(DB_USER, DB_PASS, DB_HOST, DB_HOST, DB_NAME)

DB.get_engine(DSN, echo=False)

BASE.metadata.create_all()

def test_passing():
    assert (1, 2, 3) == (1, 2, 3)

def test_dry_run():
    print('sdasdasd')
    assert do_stuff(infinite=False) == None
