all: dist

dist:
	./env/bin/pelican -s publishconf.py
	ghp-import -m "Generate documentation" -b gh-pages output/
