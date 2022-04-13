all: dist

dist:
	./env/bin/pelican -s publishconf.py
	ghp-import -p -f --cname=niwi.nz -m "Generate documentation" -b gh-pages output/
