USERS := db/users/MiSTer-devel.json db/users/MrX-8B.json db/users/mister-llapi.json db/users/Miguel-T80c.json db/users/theypsilon.json db/users/jotego.json

ALL: db/users.json db/users/MiSTer-devel.curl

clean:
	find db -type f -not -name .keep -delete

db/users.json: $(USERS)
	jq '{name, image, url}' db/users/*.json | jq -s . > $@

db/users/jotego.json:
	python mister_repo_dump.py -r jtbin -f /mister jotego > $@

db/users/%.json:
	python mister_repo_dump.py $(basename $(notdir $@)) > $@

test:
	find db -type f -name '*.json' -exec jq . {} \+ > /dev/null

db/users/%.curl: db/users/%.json
	jq '.repos[].releases[]' $< | jq -c . | python tocurl.py > $@
