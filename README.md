# Test sheet generator

This is a simple tool to prepare test sheets. It uses JSON schemas to represent questions and rules to randomly generate test sets and present them in a number of formats.

## JSON schema

Each question is an object of the form:

```json
{
    "type": "<type>",
    "question": "<question>",
    "answers": [],
    "fixed_answers": []
}
```

Here `type` is a string representing a type of the question (see below) and `question` is a text of the question. `answers` and `fixed_answers` are optional arrays of strings.

Questions are grouped into pools, that represent sets of questions to draw from. Question pools are objects of the form:

```json
{
    "name": "<name>",
    "type": "<type>",
    "questions": []
}
```

`name` is a unique id of the pool inside current schema used to reference it in the rules. `type` is a string specifying a type of pool (see below). `questions` is an array of question objects.

Each test sheet template contains a number of pools and rules that describe the resulting test sheet. It has following structure:

```json
{
    "name": "<name>",
    "schema": [
		{ "pool_name": "<name>", "args": [] }
	],
	"pools": []
}
```

`name` specifies the name of the schema/template. `schema` is an _ordered_ array of rules objects, that have two fields: `pool_name` is a name of the pool to draw question from and `args` is an array of additional options to pass to the generator (see below). `pools` is an array of question pool objects.
 
### Questions and pools

Supported pool types are:

- Simple pools (`'simple'`): questions are uniformly randomly selected from this pool.
- Exhaust pools (`'exhaust'`): once selected, questions are exhausted from the pool, until there are no questions left. After that, the pool resets.

Supported question types are:

- Open questions (`'open'`): questions with no designated answer options.
- Choice questions (`'choice'`): single or multiple choice questions.
- Choice questions w/ fixed answers (`'fixed'`): same as choice questions, but some answer options are fixed and will appear on all sheets (i.e. are exempt from random generation).

### Schema rules arguments 

Currently schema rules can contain only one argument --- max number of options to get from the `answers` array.

## Command line options

Usage:

```
testgen filename [-n N] [-f {pdf,tex,html,plaintext}] [-s SEED]
           [-b] [-o OUTFILE] 
           [-h] [--version]
```

- `filename` is a name of a template file with JSON schema
- `-n`: specifies the number of test sheets to generate (default: 1)
- `-f` or `--front`: specifies the front-end generator (default: pdf)
- `-s` or `--seed`: provide a seed for RNG
- `-b` or `--batch`: generate all sheets in a single file
- `-o` or `--outfile`: specifies the name for the batch file (only for `-b` mode)

## Requirements

- pylatex for pdf and tex fronts
- jinja2 for HTML front
