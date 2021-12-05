# search_check
Prototype of a debugging tool for curation-scripts

Requirements:
python3
structlog
dictdiffer

Copy my_search_check.py to your directory
Create my_custom_action.py
run python my_custom_action.py
until you are happy with it

upload my_custom_action.py to github:
create a new directory under https://github.com/inspirehep/curation-scripts/tree/master/scripts 
add my_custom_action.py as new file 
swap the include file to from *inspirehep.curation.search_check_do import SearchCheckDo*
create PR
For updates edit the file directly on github
