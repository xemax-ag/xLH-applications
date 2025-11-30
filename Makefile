help:
	# done

venv_build:
	rm -rf .venv && rm -rf uv.lock && uv sync

venv_update:
	uv lock --upgrade && uv sync

zone:
	find . -name "*Zone.Identifier" -type f -delete

install_uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

download_repo:
	gh repo clone xemax-ag/xLH-projects

win_venv_sync:
	powershell uv sync

win_venv_update:
	powershell uv lock --upgrade;
	powershell uv sync

win_venv_rebuild:
	powershell rm -r -fo .venv -ErrorAction SilentlyContinue;
	powershell rm -fo uv.lock -ErrorAction SilentlyContinue;
	powershell uv sync

win_install_uv:
	powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

win_install_scoop:
	Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
	Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

win_install_make:
	scoop install main/make

win_install_gh:
	scoop install main/gh

