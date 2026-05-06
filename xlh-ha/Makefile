HOST=192.168.1.131
USER=xlh
PASSWORD=xlh

help:
	@echo "up"
	@echo "down"
	@echo "compose"
	@echo "compose_log"
	@echo "clean"

up:
	docker compose -f compose_xlh_ha.yml up -d

down:
	docker compose -f compose_xlh_ha.yml down

compose:
	docker compose -f compose_xlh_ha.yml down --remove-orphans
	docker compose -f compose_xlh_ha.yml up --pull always -d

compose_log:
	docker compose -f compose_xlh_ha.yml down --remove-orphans
	docker compose -f compose_xlh_ha.yml up --pull always

clean:
	sudo rm -rf zigbee2mqtt;
	mkdir zigbee2mqtt;
	sudo rm -rf node_red;
	mkdir node_red;
	sudo chown -R 1000:1000 node_red;
	sudo chmod -R 755 node_red;
	sudo ls;

#ssh_clean:
#	sshpass -p "${PASSWORD}" ssh -o "StrictHostKeyChecking=no" ${USER}@${HOST} "cd xemax/docker/xlh-ha && ls"

#ssh_dev: ssh_down ssh_upload
#	 sshpass -p "${PASSWORD}" ssh "${USER}@${HOST}" "$(MAKE) -C ~/xemax/xlh-ha up"

ssh_down: ssh_upload
	 sshpass -p "${PASSWORD}" ssh "${USER}@${HOST}" "$(MAKE) -C ~/xemax/xlh-ha compose"

ssh_upload:
	sshpass -p "${PASSWORD}" rsync -av --delete -e "ssh -o StrictHostKeyChecking=no" \
		--exclude codesys \
		--exclude misc \
		--exclude docs \
		--exclude data/zigbee2mqtt \
		--exclude data/node_red \
		--exclude README.md \
		--exclude weblinks.md \
		./ ${USER}@${HOST}:xemax/xlh-ha

ssh_download:
	sshpass -p "${PASSWORD}" rsync -av --delete -e "ssh -o StrictHostKeyChecking=no" \
		--exclude log \
		${USER}@${HOST}:xemax/xlh-ha/data/zigbee2mqtt/ ./backup/demo/