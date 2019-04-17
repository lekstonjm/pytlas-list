from sure import expect
from pytlas import settings
from pytlas.testing import create_skill_agent
from nose import with_setup
import os
import shutil

agent = None

def get_test_tmp_folder_path():
  base_path = os.path.dirname(__file__)
  test_tmp_folder_path = os.path.join(base_path,'.test_tmp_folder')
  return test_tmp_folder_path

def remove_test_tmp_folder():
  test_tmp_folder_path = get_test_tmp_folder_path()
  if os.path.exists(test_tmp_folder_path):
    shutil.rmtree(test_tmp_folder_path)

def create_test_tmp_folder():
  test_tmp_folder_path = get_test_tmp_folder_path()
  if not os.path.exists(test_tmp_folder_path):
    os.makedirs(test_tmp_folder_path)

def setup_module(module):
  global agent
  remove_test_tmp_folder()
  test_tmp_folder_path = get_test_tmp_folder_path()
  settings.set('path',test_tmp_folder_path,section='pytlas_list')
  agent = create_skill_agent(os.path.dirname(__file__), lang='en')
 
def teardown_module(module):
  remove_test_tmp_folder()

def my_setup_function():
  create_test_tmp_folder()

def my_teardown_function():
  remove_test_tmp_folder()
 
@with_setup(my_setup_function, my_teardown_function)
def test_enumerate_lists_with_no_list():
  agent.parse('enumerate lists')
  call = agent.model.on_answer.get_call()
  expect(call.text).to.equal('I found no list')

@with_setup(my_setup_function, my_teardown_function)
def test_add_egg_in_shopping_list():
  agent.parse('add egg in my shoping list')
  call = agent.model.on_ask.get_call()
  expect(call.text).to.equal('Hummm! The list "{0}" seems not exists. Would you like create it?'.format('shoping list'))
  agent.parse('Yes')
  call = agent.model.on_ask.get_call()
  expect(call.text).to.equal('Ok, "{0}" has been added in your list "{1}"'.format('egg', 'shopping list'))