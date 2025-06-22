.PHONY: run, window, run-cmd

	#wt --title "FastAPI" --command "bash -c 'cd $(shell pwd) && make run-cmd'"

window:
	wt -w new --title "FastAPI" -d $(CURDIR) cmd /k "make run-cmd"
run-cmd:
	pip install -r requirements.txt
	uvicorn app:app --reload

run: window 

