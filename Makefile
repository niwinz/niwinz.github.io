all: dist

dist:
	./env/bin/pelican -s publishconf.py
	ghp-import -p -f -m "Generate documentation" -b gh-pages output/
