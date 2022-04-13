all: dist

dist:
	./env/bin/pelican -s publishconf.py
	ghp-import -p -m "Generate documentation" -b gh-pages output/
