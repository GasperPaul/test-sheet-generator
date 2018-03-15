class OpenQuestion(object):
	def __init__(self, question, display_hints = {}, **kwargs):
		self._question = question
		self._display_hints = display_hints
		
	def get_question(self):
		return self._question
		
	def get_answers(self):
		return []
		
	def get_choices(self, *args):
		return []
		
	def get_display_hints(self):
		return self._display_hints
		
	def __str__(self):
		return self.get_question()
		

class ChoiceQuestion(OpenQuestion):
	def __init__(self, question, answers, **kwargs):
		super().__init__(question, **kwargs)
		self.__answers = answers
		
	def get_answers(self):
		return self.__answers
		
	def get_choices(self, rng, count = 1):
		return rng.sample(self.__answers, min(count, len(self.__answers)))
		

class FixedChoiceQuestion(ChoiceQuestion):
	def __init__(self, question, answers, fixed_answers, **kwargs):
		super().__init__(question, answers, **kwargs)
		self.__fixed_answers = fixed_answers
		
	def get_answers(self):
		return super().get_answers() + self.__fixed_answers
		
	def get_choices(self, rng, count = 1):
		return super().get_choices(rng, count) + self.__fixed_answers
	

def create_question(type, *args, **kwargs):
	if type == 'open':
		return OpenQuestion(*args, **kwargs)
	elif type == 'choice':
		return ChoiceQuestion(*args, **kwargs)
	elif type == 'fixed':
		return FixedChoiceQuestion(*args, **kwargs)
	else:
		raise ValueError('Unknown type of question: {}'.format(type))