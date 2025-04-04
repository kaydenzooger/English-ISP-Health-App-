.PHONY: all setup clean run

all: setup clean run

setup:
	pip install scikit-learn nltk
	npm install cors express

clean:
	rm -f output.txt user_input.txt
	touch output.txt user_input.txt

run:
	node server.js
