# Formatting the bibliography in the right order in BibLaTeX and plain LaTeX
How many times we need to submit articles with manual bibliographies, because of some annoying old BibTex/Natbib packages that simply do not work in a plain manner, but nonetheless are the "way to go" of common journals?
Wouldn't it be better if we had a tool just to do it last minute without worrying, after focusing on the article content, instead of the BibTeX errors and the correct order of the manual bibliography? 
This is the package for you. 

## Overview of the scripts
### Using BibLaTeX
1. format the citation keys present in a bibliography (e.g. a ``.bib`` file coming from Zotero) using ``format_keys.py``
2. write the damn article using those citation keys
3. extract the order of the citations appearing in the manuscript using ``extract_keys.py``
4. sort the bibliography file using ``sort_bib.py``
5. generate the manual bibliography using ``bib2source.py``

and the article is ready for shipping.

### Using manual bibliography
1. write the damn article using the citation keys you write inside the manual bibliography
3. extract the order of the citations appearing in the manuscript using ``extract_keys.py``
4. sort the bibliography file using ``sort_manual.py``
5. copy-paste the sorted bibliography back again in the source file

and the article is ready for shipping.

## Check if everything is in order
Just run ``check.py`` to verify that:
- the citations in the text are sorted in the same way as in the manual bibliography at the bottom
- all and only the citation in the text are appearing in the bibliography

Have fun