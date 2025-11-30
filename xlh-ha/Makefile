HOST=192.168.1.31
USER=xlh

help:
	@echo "compose"
	@echo "compose_log"


compose:
	docker compose -f compose_xlh_ha.yml down --remove-orphans
	docker compose -f compose_xlh_ha.yml up --pull always -d

compose_log:
	docker compose -f compose_xlh_ha.yml down --remove-orphans
	docker compose -f compose_xlh_ha.yml up --pull always -d


upload:
	rsync -av --delete \
		./ ${USER}@${HOST}:home/xlh/xemax/docker/xlh-ha