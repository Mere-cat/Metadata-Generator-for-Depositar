IPYNB_FILES = $(shell find metadata_generator/docs -name "*.ipynb")
MD_FILES = $(IPYNB_FILES:.ipynb=.md)

all: nb2md rename build 

nb2md: $(MD_FILES)

%.md: %.ipynb | nb2md
	jupytext $^ --to myst

build:
	jupyter-book build metadata_generator/
	cp -r metadata_generator/assets/ metadata_generator/_build/html/

rename:
	@for file in $(MD_FILES); do \
	new_file="$${file%.md}_new.md"; \
	mv "$$file" "$$new_file"; \
	done

clean:
	@echo "Cleaning generated .md files"
	@find . -name "*_new.md" -exec rm {} +
	@echo "Cleaning _build/"
	rm -r metadata_generator/_build/