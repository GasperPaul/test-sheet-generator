class QuestionPool(object):
	def __init__(self, name, questions):
		self.__name = name
		self._questions = questions
		
	def get_question(self, rng):
		return rng.choice(self._questions)
		
	def __len__(self):
		return len(self._questions)
		
	def __iter__(self):
		yield self.get_question()
		
		
class ExhaustQuestionPool(QuestionPool):
	def __init__(self, name, questions, exaust_strategy = lambda p, q: True):
		super().__init__(name, questions)
		self.__exaust_pool = []
		self.__exaust_strategy = exaust_strategy
		self.__prev_question = None
		
	def get_question(self, rng):
		if len(self._questions) == 0:
			self.__reset()
		q = super().get_question(rng)
		while q == self.__prev_question:
			q = super().get_question(rng)
		self.__prev_question = q
		if self.__exaust_strategy(self, q):
			self._questions.remove(q)
			self.__exaust_pool.append(q)
		return q
		
	def __reset(self):
		self._questions.extend(self.__exaust_pool)
		self.__exaust_pool = []


def create_question_pool(type, *args, **kwargs):
	if type == 'simple':
		return QuestionPool(*args, **kwargs)
	elif type == 'exhaust':
		return ExhaustQuestionPool(*args, **kwargs)
	else:
		raise ValueError('Unknown type of question pool: {}'.format(type))