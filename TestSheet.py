from question import create_question
from question_pool import create_question_pool


class TestSheet(object):
	def __init__(self, name, pools, schema):
		self.__name = name
		self.__pools = pools
		self.__schema = schema
	
	def generate(self, rng):
		result = {
			'name': self.__name,
			'questions': []
		}
		for pool_name, args in self.__schema:
			q = self.__pools[pool_name].get_question(rng)
			result['questions'].append((q.get_question(), q.get_choices(rng, *args)))
		return result
		
		
	@classmethod
	def from_json(this, json_obj):
		import json
		obj = json.load(json_obj)
		name = obj['name']
		pools = {}
		for pool in obj['pools']:
			questions = []
			for question in pool['questions']:
				questions.append(create_question(question['type'], 
					question = question["question"], 
					answers = question.get("answers"),
					fixed_answers = question.get("fixed_answers")))
			pools[pool['name']] = create_question_pool(pool['type'], 
				name = pool['name'],
				questions = questions)
		schema = [(q['pool_name'], q['args']) for q in obj['schema']]
		return this(name, pools, schema)