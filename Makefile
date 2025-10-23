.PHONY: run test eval quantize export
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
test:
	pytest -q
eval:
	python eval.py
quantize:
	python tools/quantize.py
export:
	python tools/export.py
