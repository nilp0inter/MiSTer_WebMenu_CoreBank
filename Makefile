ALL: db/users/MiSTer-devel.json db/users/MrX-8B.json

db/users/%.json:
	python mister_repo_dump.py $(basename $(notdir $@)) > $@
