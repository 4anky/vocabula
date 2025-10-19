from alembic import command
from alembic.config import Config

command.upgrade(Config('alembic.ini'), 'head')
