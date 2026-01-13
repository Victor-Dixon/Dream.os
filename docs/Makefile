# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom targets for Agent Cellphone V2 documentation
setup:
	pip install -r requirements.txt

clean-all:
	rm -rf $(BUILDDIR)/*
	rm -rf api/
	rm -rf examples/
	rm -rf _static/

autodoc:
	sphinx-apidoc -f -o api/ ../src/

html:
	$(SPHINXBUILD) -b html $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/html

serve:
	cd $(BUILDDIR)/html && python -m http.server 8000

deploy: clean-all autodoc html
	@echo "Documentation built successfully!"
	@echo "To serve locally: make serve"
	@echo "To deploy to GitHub Pages: configure GitHub Actions"