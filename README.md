# search_check
Prototype of a debugging tool for curation-scripts

Requirements:
* python3
* structlog
* dictdiffer

How to use:
* Copy my_search_check.py to your directory
* Create my_custom_action.py
* run python my_custom_action.py
* until you are happy with it

Upload my_custom_action.py to github:
* Create a new directory under https://github.com/inspirehep/curation-scripts/tree/master/scripts 
* Add my_custom_action.py as new file. 
* Swap the include file to from *inspirehep.curation.search_check_do import SearchCheckDo*.
* Create PR.
* For updates edit the file directly on github
