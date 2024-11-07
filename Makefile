# Paths
FRONTEND_DIR = frontend
BACKEND_DIR = backend
VENV_DIR = $(BACKEND_DIR)/venv

# Commands
install:
	# Install npm packages for frontend
	cd $(FRONTEND_DIR) && npm install

	# Install virtualenv if not already installed
	python3.11 -m pip install virtualenv

	# Create a Python virtual environment under backend/ and install backend requirements
	python3.11 -m virtualenv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r $(BACKEND_DIR)/requirements.txt

run-frontend:
	# Run Vite server in frontend directory
	cd $(FRONTEND_DIR) && npm run dev

run-backend:
	# Activate virtual environment under backend/ and start Uvicorn server
	. $(VENV_DIR)/bin/activate && cd $(BACKEND_DIR) && uvicorn main:app --reload --port 8000 --log-level debug

run:
	# Run both frontend and backend concurrently - TODO run in containers
	(make run-frontend &)
	(make run-backend &)
	wait
