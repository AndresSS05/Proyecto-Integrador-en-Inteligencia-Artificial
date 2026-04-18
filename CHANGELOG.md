# Changelog

Todos los cambios notables a este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [1.0.0] — 2026-04-17

### Añadido

- Notebook `01_evaluacion_modelos_spider.ipynb` con el pipeline completo de evaluación.
- Tres actividades de evaluación implementadas:
  - **Benchmarking comparativo** con 10 modelos locales y 3 APIs comerciales estimadas.
  - **Análisis de sesgo algorítmico** con métricas Disparate Impact Ratio y Equalized Odds Gap.
  - **Diagnóstico de overfitting/underfitting** con curvas de aprendizaje 5-fold y barrido de `max_depth`.
- Informe final en formato Word (`.docx`) y PDF siguiendo el formato institucional UEES.
- Cuatro figuras principales generadas desde el notebook e incluidas en `reports/figures/`.
- Análisis crítico transversal sobre fuga de información (data leakage) en el pipeline de feature engineering.
- Referencias bibliográficas verificadas en formato APA 7ª edición.
- Guía de presentación en `docs/GUIA_PRESENTACION.md`.
- Estructura sugerida de diapositivas en `docs/ESTRUCTURA_SUGERIDA_SLIDES.md`.
- Workflow de CI/CD para validación automática del notebook.

### Pipeline Técnico

- Descarga automática del dataset Spider desde Hugging Face Hub.
- Feature engineering de 35 variables SQL + 35 variables lingüísticas.
- Representación TF-IDF de preguntas reducida por PCA a 50 componentes.
- Pipeline de preprocesamiento con `RobustScaler` y `SimpleImputer`.
- Entrenamiento paralelizado con cálculo de class weights balanceados.

### Resultados Destacados

- Profundidad óptima empírica del Random Forest identificada en `max_depth = 14`.
- Métricas de fairness dentro del umbral aceptable para las tres variables sensibles.
- Hallazgo crítico sobre data leakage documentado y explicado con referencia a Kaufman et al. (2012).

---

## [Unreleased]

### Planeado para versiones futuras

- Refactorización del notebook a módulos reutilizables en `src/`.
- Tests unitarios con `pytest` sobre las funciones de feature engineering.
- Experimentación con embeddings contextuales (CodeBERT) para superar el data leakage.
- Evaluación empírica directa sobre APIs comerciales (no solo estimadas).
- Redefinición de la tarea como clasificación desde la pregunta natural únicamente.
- Bootstrap para intervalos de confianza en todas las métricas reportadas.
