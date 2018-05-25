from flask import Flask
from flask import render_template
from flask import request
from flask import flash
import sys
from collections import defaultdict
from ff import GrammarParser

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def hello():
	return render_template('index.html', title = "Output comes here:", output = "", entered_grammar="", error_code = 0)

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
				return render_template('index.html', title = "Output comes here:", output = "", entered_grammar=input_grammar[:], error_code = 1)
			return render_template('index.html', title = "First Set", output = "\n".join(first_output), entered_grammar=input_grammar[:], error_code = 0)

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
				return render_template('index.html', title = "Output comes here:", output = "", entered_grammar=input_grammar[:], error_code = 1)
			return render_template('index.html', title = "Follow Set", output = "\n".join(follow_output), entered_grammar=input_grammar[:], error_code = 0)

		elif(request.form['parse_type'] == 'lalr'):
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
				return render_template('index.html', title = "Output comes here:", output = "", entered_grammar=input_grammar[:], error_code = 1)
			return render_template('index.html', title = "Follow Set", output = "\n".join(follow_output), entered_grammar=input_grammar[:], error_code = 0)

		elif(request.form['parse_type'] == 'lr'):
			input_grammar = request.form['grammar']
			return render_template('index.html', title = "Output comes here:", output = "", entered_grammar=input_grammar[:], error_code = 2)

		elif(request.form['parse_type'] == 'll'):
			input_grammar = request.form['grammar']
			return render_template('index.html', title = "Output comes here:", output = "", entered_grammar=input_grammar[:], error_code = 2)

		elif(request.form['parse_type'] == 'slr'):
			input_grammar = request.form['grammar']
			return render_template('index.html', title = "Output comes here:", output = "", entered_grammar=input_grammar[:], error_code = 2)

	else:
		return render_template('index.html', "Output comes here:", output = "", entered_grammar="", error_code = 1)

if __name__ == '__main__':
	app.debug = True
	app.run()
	app.run(debug = True)