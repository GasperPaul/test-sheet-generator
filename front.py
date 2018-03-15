from pylatex import Document, PageStyle, Head, LineBreak, MiniPage, NoEscape, Command, Tabular
from datetime import datetime


class AbstractFront:
	def _create_header(self, info):
		pass
	
	def _write_questions(self, info):
		pass
		
	def _add_page_separator(self):
		pass

	def _save(self, info):
		pass
		
	def _filename(self, info):
		return '{}_{}.{}'.format(info['seed'], info['run'], self.FILE_EXTENSION)
		
	def _date(self):
		return datetime.today().isoformat(sep=' ')
		
	def process(self, info):
		self._create_header(info)
		self._write_questions(info)
		self._save(info)
		
	def process_batch(self, batch, filename=None):
		if filename is None:
			self._filename = lambda info : '{}_{}.{}'.format(info['name'], info['seed'], self.FILE_EXTENSION)
		else:
			self._filename = lambda info : '{}.{}'.format(filename, self.FILE_EXTENSION)
		for info in batch:
			self._create_header(info)
			self._write_questions(info)
			self._add_page_separator()
		self._save(batch[0])

class PdfFront(AbstractFront):
	FILE_EXTENSION = 'pdf'
	PAGE_GEOMETRY = {
		'margin': '2.0cm'
	}
	PACKAGES = ['amsfonts']

	def __init__(self):
		self._doc = Document(
			geometry_options=PdfFront.PAGE_GEOMETRY,
			page_numbers=False
		)
		for package in PdfFront.PACKAGES:
			self._doc.preamble.append(Command('usepackage', arguments=package))
	
	def _create_header(self, info):
		style_name = NoEscape('header{}'.format(info['run']))
		header = PageStyle(style_name)
		with header.create(Head('L')):
			header.append(info['name'])
			header.append(LineBreak())
			header.append('Date: {}'.format(self._date()))
		with header.create(Head('R')):
			header.append('Seed: {}'.format(info['seed']))
			header.append(LineBreak())
			header.append('Run: {}'.format(info['run']))
		self._doc.preamble.append(header)
		self._doc.change_document_style(style_name)
		
	def _write_questions(self, info):
		self._doc.append(NoEscape(r'\flushleft'))
		i = 1
		for question, answers, hints in info['questions']:
			with self._doc.create(MiniPage(align='l')):
				self._doc.append('{}. {}'.format(i, question))
				self._doc.append(LineBreak())
				i += 1
				if len(answers) == 0:
					for _ in range(hints.get('max_lines', 1)):
						self._doc.append(LineBreak())
				else:
					l = hints.get('max_cols', 1)
					table_data = [answers[j:j+l] for j in range(0, len(answers), l)]
					with self._doc.create(Tabular('l'*l)) as table:
						for row in table_data:
							table.add_row(row, mapper = lambda x: NoEscape(r'$\Box~~$') + x, strict=False)
			self._doc.append(LineBreak())
		
	def _save(self, info):
		self._doc.generate_pdf(self._filename(info))
		
	def _add_page_separator(self):
		self._doc.append(NoEscape(r'\clearpage'))
		
class TexFront(PdfFront):
	def _save(self, ingo):
		self._doc.generate_tex(self._filename(info))

class PlainFront(AbstractFront):
	FILE_EXTENSION = 'txt'
	WIDTH = 80
	
	def __init__(self):
		from io import StringIO
		self.__doc = StringIO()
	
	def _create_header(self, info):
		self.__doc.write(u'='*PlainFront.WIDTH+u'\n')
		self.__doc.write(u' Test: {}\n'.format(info['name']))
		self.__doc.write(u' Seed: {}\n'.format(info['seed']))
		self.__doc.write(u' Run: {}\n'.format(info['run']))
		self.__doc.write(u' Date: {}\n'.format(self._date()))
		self.__doc.write(u'='*PlainFront.WIDTH+u'\n')

	def _write_questions(self, info):
		i = 1
		for question, answers, _ in info['questions']:
			self.__doc.write(u'{}. {}\n'.format(i, question))
			i += 1
			for answer in answers:
				self.__doc.write(u'\u25a1 {}\n'.format(answer))
			self.__doc.write(u'\n')
		
	def _save(self, info):
		from shutil import copyfileobj
		with open(self._filename(info), 'w', encoding='utf8') as file: 
			self.__doc.seek(0)
			copyfileobj(self.__doc, file)
		self.__doc.close()
		
	def _add_page_separator(self):
		self.__doc.write(u'='*PlainFront.WIDTH+u'\n\n')
	
class HtmlFront(AbstractFront):
	FILE_EXTENSION = 'html'
	TEMPLATE_PATH = './templates'
	TEMPLATE_NAME = 'testsheet.html'
	
	def __init__(self):
		from jinja2 import Environment, FileSystemLoader, select_autoescape
		env = Environment(
			loader=FileSystemLoader(HtmlFront.TEMPLATE_PATH),
			autoescape=select_autoescape(['html', 'xml'])
		)
		self.__doc = env.get_template(HtmlFront.TEMPLATE_NAME)
	
	def _write_questions(self, info):
		info['date'] = self._date()
		self.__html = self.__doc.render(info)
		
	def _save(self, info):
		with open(self._filename(info), 'w', encoding='utf-8') as file:
			file.write(self.__html)
	
	def process_batch(self, batch, filename):
		for info in batch:
			self.process(info)


def create_front(type):
	if type == 'pdf':
		return PdfFront()
	elif type == 'tex':
		return TexFront()
	elif type == 'html':
		return HtmlFront()
	elif type == 'plaintext':
		return PlainFront()
	else:
		raise ValueError('Unknown front type: {}'.format(type))