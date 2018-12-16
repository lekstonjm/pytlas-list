from pytlas import intent, training, translations
import json
import os
import unicodedata
import re
# This entity will be shared among training data since it's not language specific

"""
%[add_list]
  add @[item_name] in list @[list_name]
  add in @[list_name]

%[remove_list]
  remove @[item_name] from @[list_name]

%[delete_list]
  delete list @[list_name]


%[list_content]
  list content of @[list_name]
  enumerate @[list_name]
  what have I in @[list_name]
"""


@training('en')
def en_data(): return """
%[create_list]
  create a new list named @[list_name]
  create a list
  add a list
  new list with name @[list_name]

%[add_list]
  add @[item_name] in list @[list_name]
  add @[item_name] in my @[list_name]
  add @[item_name] in @[list_name]
  I want add something in may @[list_name]

@[list_name]
  shoping list
  todo list
  wish list
  christmas list
  gift list

@[item_name]
  garlic
  salt
  walk the dog
  call mother
  bread
  eggs
  trip  
"""

#@training('fr')
#def fr_data(): return """
#"""

#@translations('fr')
#def fr_translations(): return {
#}

def slugify(value):
  """
  Normalizes string, converts to lowercase, removes non-alpha characters,
  and converts spaces to hyphens.
  """
  slug_value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
  slug_value = re.sub(r'[^\w\s-]', '', slug_value).strip().lower()
  slug_value = re.sub(r'[-\s]+', '_', slug_value)
  return slug_value

def default_pytlas_list_path():
  return os.path.join(os.path.expanduser('~'),'.pytlas-list')


@intent('create_list')
def on_create_list(req):
  list_name = req.intent.slot('list_name').first().value
  if not list_name:
    return req.agent.ask('list_name',req._('Please choose a name for your list.'))
  list_dir_path = req.agent.meta.get('PYTLAS-LIST-PATH')

  if not list_dir_path:
    list_dir_path = default_pytlas_list_path()
  
  if not os.path.exists(list_dir_path):
    os.makedirs(list_dir_path)
  
  list_filename = slugify(list_name)+'.json'  
  list_path = os.path.join(list_dir_path,list_filename)
  
  if os.path.exists(list_path):
    req.agent.answer(req._('Oops! This list already exists.'))
    return req.agent.done()

  with open(list_path,'w') as json_file:
    list_content = { 'name' : list_name, 'items' : [] }
    json.dump(list_content, json_file)

  req.agent.answer(req._('Ok your list has been created.'))
  return req.agent.done()

@intent('add_list')
def on_add_item(req):
  list_name = req.intent.slot('list_name').first().value
  if not list_name:
    return req.agent.ask('list_name',req._('In which list?'))

  list_dir_path = req.agent.meta.get('PYTLAS-LIST-PATH')  
  if not list_dir_path:
    list_dir_path = default_pytlas_list_path()
  
  list_filename = slugify(list_name)+'.json'  
  list_path = os.path.join(list_dir_path,list_filename)
  if not os.path.exists(list_path):
    req.agent.answer(req._('Hummm! This list does\'t exists.'))
    return req.agent.done()

  item_name = req.intent.slot('item_name').first().value
  if not item_name:
    return req.agent.ask('item_name', req._('What do you want to add in your list?'))

  list_content = { 'name' : list_name, 'items' : [] }
  with open(list_path,'r') as json_file:
    list_content = json.load(json_file)
    list_content['items'].append(item_name)

  with open(list_path,'w') as json_file:
    json.dump(list_content, json_file)

  req.agent.answer(req._('Ok, item has been added in your list'))
  return req.agent.done()
  

