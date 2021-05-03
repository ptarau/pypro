from .natlog import natlog
from .ndb import *

class neural_natlog(natlog):
  """
  overrrides natlog's database constructor
  to use a neurally indexed nd instead of db
  """
  def db_init(self):
    self.db=ndb()

