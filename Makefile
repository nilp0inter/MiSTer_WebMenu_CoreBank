ALL: db/users/MiSTer-devel.json db/users/MrX-8B.json db/users/mister-llapi.json db/users/Miguel-T80c.json db/users/theypsilon.json

db/users/%.json:
	python mister_repo_dump.py $(basename $(notdir $@)) > $@
