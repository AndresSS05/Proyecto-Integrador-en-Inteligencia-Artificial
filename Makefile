install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest -q

notebook:
	jupyter notebook notebooks/01_evaluacion_modelos_spider_uees.ipynb
