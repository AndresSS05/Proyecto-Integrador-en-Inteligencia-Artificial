# Proyecto Integrador en Inteligencia Artificial
## Evaluación de Modelos IA sobre Spider (Text-to-SQL)

Repositorio profesional y reproducible del proyecto de **benchmarking comparativo, análisis de sesgo algorítmico y diagnóstico de overfitting/underfitting** sobre el dataset Spider.

Este repositorio reorganiza el trabajo original en una estructura limpia de ingeniería, separando:
- **documentación técnica**
- **código reutilizable**
- **notebooks reproducibles**
- **pruebas básicas**
- **automatización CI**

## Qué incluye

- Pipeline de carga del dataset Spider desde Hugging Face.
- Extracción de features SQL y lingüísticas.
- Preprocesamiento con variables numéricas + TF-IDF + PCA.
- Benchmarking con baselines, Random Forest, Logistic Regression, SVM, Gradient Boosting, XGBoost y LightGBM.
- Análisis de fairness por longitud de pregunta, presencia de JOIN y dominio.
- Diagnóstico de generalización con curvas de aprendizaje y barrido de `max_depth`.
- Documentación técnica basada en el informe académico y el notebook entregado.

## Estructura

```text
.
├── .github/workflows/ci.yml
├── docs/
│   ├── FUENTES_DEL_REPOSITORIO.md
│   ├── GUIA_PRESENTACION.md
│   ├── INFORME_TECNICO.md
│   ├── ESTRUCTURA_SUGERIDA_SLIDES.md
│   └── REPRODUCIBILIDAD.md
├── notebooks/
│   ├── 01_evaluacion_modelos_spider_uees.ipynb
│   └── README.md
├── reports/
│   └── README.md
├── src/
│   ├── __init__.py
│   ├── benchmark.py
│   ├── config.py
│   ├── fairness.py
│   ├── features.py
│   ├── generalization.py
│   └── pipeline.py
├── tests/
│   └── test_structure.py
├── .gitignore
├── CHANGELOG.md
├── CITATION.cff
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── pyproject.toml
└── requirements.txt
```

## Flujo recomendado

```bash
make install
make test
make notebook
```

## Resultado esperado

El proyecto queda listo para:
1. presentación académica,
2. mantenimiento futuro,
3. migración del notebook a código modular,
4. versión portafolio o tesis,
5. incorporación posterior de artefactos binarios finales en `reports/`.

## Nota metodológica clave

Los resultados muy altos observados en varios modelos deben interpretarse con cautela por la sospecha fundada de **data leakage**, ya que varias features derivan de la propia estructura del SQL usada para inferir la dificultad.

## Autores

- Joel David Cabrera Parrales
- Aníbal Andrés Sánchez Arévalo

Universidad de Especialidades Espíritu Santo  
Maestría en Inteligencia Artificial
