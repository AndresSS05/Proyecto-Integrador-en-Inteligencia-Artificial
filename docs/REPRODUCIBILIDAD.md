# Reproducibilidad

## Entorno mínimo
- Python 3.10+
- pip
- conexión a internet para descargar Spider desde Hugging Face

## Pasos
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/01_evaluacion_modelos_spider_uees.ipynb
```

## Recomendación de trabajo
- usa el notebook para exploración,
- usa `src/` para lógica reutilizable,
- conserva resultados finales en `reports/`.
