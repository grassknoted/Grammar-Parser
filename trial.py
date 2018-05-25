from flask import Flask
from flask import render_template
from flask import request
import sys
from collections import defaultdict
from ff import GrammarParser


app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('index.html', title = "", output = "", entered_grammar="")

@app.route('/', methods=['GET', 'POST'])
def grammer_parser():
	if request.method == 'POST':
		if(request.form['parse_type'] == 'first'):
			input_grammar = request.form['grammar']
			write_to_file = open("temp_rules.txt", 'w')
			write_to_file.write(input_grammar)
			write_to_file.close()
			read_from_file = open("temp_rules.txt", 'r').read()
			try:
				gz = GrammarParser(read_from_file)
				#gz.print_first_set()
				first_output = gz.return_first_set()
			except:
				return render_template('index.html', title = "Incorrect Input!", output = "", entered_grammar=input_grammar[:])
			return render_template('index.html', title = "First Set", output = "\n".join(first_output), entered_grammar=input_grammar[:])

		elif(request.form['parse_type'] == 'follow'):
			input_grammar = request.form['grammar']
			write_to_file = open("temp_rules.txt", 'w')
			write_to_file.write(input_grammar)
			write_to_file.close()
			read_from_file = open("temp_rules.txt", 'r').read()
			try:
				gz = GrammarParser(read_from_file)
				#gz.print_follow_set()
				follow_output = gz.return_follow_set()
			except:
				return render_template('index.html', title = "Incorrect Input!", output = "", entered_grammar=input_grammar[:])
			return render_template('index.html', title = "Follow Set", output = "\n".join(follow_output), entered_grammar=input_grammar[:])

	else:
		return render_template('index.html', title = "", output = "", entered_grammar="")

if __name__ == '__main__':
	app.debug = True
	app.run()
	app.run(debug = True)