run-local-server:
	cd app && python3 application.py

local-setup:
	cd app && python3 -m pip install --no-cache-dir -r requirements.txt
