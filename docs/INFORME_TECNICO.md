# Informe técnico del repositorio

## 1. Propósito
Este repositorio documenta la evaluación de un clasificador de dificultad de consultas SQL sobre el dataset Spider. El enfoque se organiza en tres frentes:

1. benchmarking comparativo,
2. análisis de sesgo algorítmico,
3. diagnóstico de overfitting y underfitting.

## 2. Pipeline reproducido
El proyecto utiliza:
- carga de Spider desde Hugging Face,
- extracción de features SQL,
- extracción de features lingüísticas,
- TF-IDF con reducción PCA,
- clasificación multiclase en cuatro niveles: `easy`, `medium`, `hard`, `extra`.

## 3. Modelos incluidos
- Baseline aleatorio
- Baseline por clase más frecuente
- Árbol de decisión
- Regresión logística
- K-NN
- SVM con kernel RBF
- Random Forest
- Gradient Boosting
- XGBoost
- LightGBM

## 4. Fairness evaluado
Se estructura el análisis sobre:
- longitud de pregunta,
- presencia de JOIN,
- dominio de base de datos.

## 5. Generalización
Se incluyen:
- curvas de aprendizaje,
- análisis train vs validation,
- barrido de `max_depth`.

## 6. Hallazgo crítico
El repositorio deja explícito que existe una sospecha seria de **data leakage**. Varias features provienen del mismo SQL cuya estructura influye directamente en la etiqueta de dificultad, así que métricas casi perfectas no deben interpretarse como desempeño real sin reservas.

## 7. Recomendaciones
- migrar hacia clasificación desde lenguaje natural solamente,
- separar mejor variables de entrada y definición de etiqueta,
- fortalecer validación cross-domain,
- reemplazar representación manual por embeddings contextuales.
