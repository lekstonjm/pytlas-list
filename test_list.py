from sure import expect
from pytlas.testing import create_skill_agent
import os

class TestList:

  def test_add_in_new_list(self):
    agent = create_skill_agent(os.path.dirname(__file__), lang='en')
    pass