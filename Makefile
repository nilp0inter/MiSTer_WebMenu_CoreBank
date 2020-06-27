USERS := db/users/MiSTer-devel.json db/users/MrX-8B.json db/users/mister-llapi.json db/users/Miguel-T80c.json db/users/theypsilon.json

ALL: db/users.json

clean:
	find db -type f -not -name .keep -delete

db/users.json: $(USERS)
	jq '{name, image, url}' db/users/*.json | jq -s > $@

db/users/%.json:
	python mister_repo_dump.py $(basename $(notdir $@)) > $@

