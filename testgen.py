import argparse
from sys import maxsize
from random import randrange, Random

from TestSheet import TestSheet
from front import create_front

VERSION = 1.0
FRONTS = ['pdf','tex','html','plaintext']


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate new test sheets')
	parser.add_argument('filename', help='filename of the test sheet template')
	parser.add_argument('-s', '--seed', type=int, help='use specified seed for generation')
	parser.add_argument('-n', type=int, default=1, help='generate %(dest)s test sheets (default: %(default)s)')
	parser.add_argument('-f', '--front', choices=FRONTS, default='pdf',
		help='frontend that generates the test sheet view (default: %(default)s)')
	parser.add_argument('-b', '--batch', action='store_true', help='generate all test sheets in one file')
	parser.add_argument('-o', '--outfile', default=None, help='name of the file with batch generation results')
	parser.add_argument('--version', action='version', version='%(prog)s v.{}'.format(VERSION))

	args = parser.parse_args()

	with open(args.filename) as file:
		template = TestSheet.from_json(file)

	rng = Random()
	seed = args.seed if args.seed else randrange(maxsize)
	rng.seed(args.seed)
	
	sheets = []
	for n in range(args.n):
		sheet = template.generate(rng)
		sheet['seed'] = seed
		sheet['run'] = n
		sheets.append(sheet)

	front = create_front(args.front)
	if not args.batch:
		for sheet in sheets:
			front.process(sheet)
	else:
		front.process_batch(sheets, args.outfile)