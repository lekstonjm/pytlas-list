from sure import expect
from pytlas import settings
from pytlas.testing import create_skill_agent
import os


base_path = os.path.dirname(__file__)
test_folder_path = os.path.join(base_path,'.unit_tests_list_folder')
if os.path.exists(test_folder_path):
  os.removedirs(test_folder_path)

agent = create_skill_agent(os.path.dirname(__file__), lang='en')
settings.get('path',test_folder_path,section='pytlas_list')

class TestList:
  def test_enumerate_lists(self):
    agent.parse('enumerate lists')
    call = agent.model.on_answer.get_call()
    expect(call.text).to.equal('I found no list')

  def test_add_in_new_list(self):
    pass