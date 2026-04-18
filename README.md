# Proyecto Integrador en Inteligencia Artificial

> **Evaluación de Modelos de IA sobre el dataset Spider (Text-to-SQL):** Benchmarking comparativo, análisis de sesgo algorítmico y diagnóstico de overfitting/underfitting.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.0+-0E83CD)](https://lightgbm.readthedocs.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-00599C)](https://xgboost.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![UEES](https://img.shields.io/badge/UEES-Maestría%20IA-821538)](https://www.uees.edu.ec/)
[![Status](https://img.shields.io/badge/Status-Completado-success)]()

---

## 📑 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Objetivos](#-objetivos)
- [Dataset](#-dataset)
- [Metodología](#-metodología)
- [Resultados Principales](#-resultados-principales)
- [Visualizaciones](#-visualizaciones)
- [Estructura del Repositorio](#-estructura-del-repositorio)
- [Instalación y Uso](#-instalación-y-uso)
- [Hallazgo Metodológico Relevante](#-hallazgo-metodológico-relevante)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Equipo](#-equipo)
- [Referencias](#-referencias)
- [Licencia](#-licencia)

---

## 📖 Descripción del Proyecto

Este repositorio contiene la **tercera fase del Proyecto Integrador en Inteligencia Artificial** correspondiente a la Maestría en Inteligencia Artificial de la **Universidad de Especialidades Espíritu Santo (UEES)**. El trabajo aborda la evaluación sistemática de un clasificador de dificultad de consultas SQL entrenado sobre el dataset **Spider** (Yu et al., 2018), benchmark estándar de la tarea Text-to-SQL.

El estudio se articula en **tres actividades** alineadas con la rúbrica oficial de la asignatura:

| # | Actividad | Descripción |
|:-:|-----------|-------------|
| 1️⃣ | **Benchmarking Comparativo** | Comparación del modelo Random Forest propuesto contra 10 modelos locales (baselines, estado del arte) y 3 APIs comerciales estimadas. |
| 2️⃣ | **Análisis de Sesgo Algorítmico** | Evaluación de equidad sobre 3 variables sensibles mediante métricas estándar (Disparate Impact Ratio, Equalized Odds Gap). |
| 3️⃣ | **Diagnóstico Overfitting/Underfitting** | Construcción de curvas de aprendizaje y barrido paramétrico de `max_depth` para diagnosticar la capacidad de generalización. |

---

## 🎯 Objetivos

### Objetivo General

Determinar el valor real del clasificador de dificultad SQL desarrollado en fases anteriores, comparándolo contra referencias simples, contra el estado del arte y contra servicios comerciales, mientras se audita su comportamiento ético y su capacidad de generalización.

### Objetivos Específicos

- Cuantificar la mejora del modelo propuesto frente a baselines triviales y modelos simples.
- Posicionar el clasificador respecto a algoritmos de estado del arte en clasificación tabular (Gradient Boosting, XGBoost, LightGBM).
- Evaluar la competitividad frente a APIs comerciales (Google AutoML, Amazon Comprehend, Azure ML).
- Identificar posibles sesgos del modelo en grupos sensibles y proponer estrategias de mitigación.
- Diagnosticar la presencia de overfitting o underfitting mediante curvas de aprendizaje.
- Proponer un plan de mejora técnica fundamentado en evidencia empírica.

---

## 📊 Dataset

**Spider** (Yu et al., 2018) — *A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task.*

| Característica | Valor |
|----------------|-------|
| **Fuente** | Hugging Face Hub (`xlangai/spider`) |
| **Tamaño total** | 8.034 ejemplos (7.000 train + 1.034 validation) |
| **Dominios** | 138 dominios, 200 bases de datos |
| **Variable objetivo** | Dificultad SQL: `easy`, `medium`, `hard`, `extra` |
| **Split** | Cross-domain (20 dominios de validación no aparecen en entrenamiento) |
| **Licencia** | CC BY-SA 4.0 |
| **Referencia** | [arXiv:1809.08887](https://arxiv.org/abs/1809.08887) • [ACL Anthology](https://aclanthology.org/D18-1425/) |

---

## 🔬 Metodología

### Pipeline de Feature Engineering

Se construyó un vector de **85 características** combinando:

- **35 features numéricas especializadas** extraídas de la consulta SQL: cantidad de cláusulas `SELECT`, `WHERE`, `GROUP BY`, `HAVING`; presencia de `JOIN`, subconsultas y funciones de agregación; profundidad de anidamiento.
- **Features lingüísticas** de la pregunta en lenguaje natural: conteo de palabras, palabras interrogativas (WH-words), palabras de agregación, stopwords, entidades nombradas.
- **50 componentes TF-IDF** de la pregunta natural, reducidos mediante PCA.

### Modelos Evaluados

```
├── Baselines Triviales
│   ├── DummyClassifier (Stratified)
│   └── DummyClassifier (Most Frequent)
│
├── Modelos Simples
│   ├── Árbol de Decisión (max_depth=5)
│   └── K-NN (k=7)
│
├── Modelos Lineales
│   └── Regresión Logística (L2)
│
├── Modelo Propuesto
│   └── Random Forest (n_estimators=200) ★
│
├── Estado del Arte Tabular
│   ├── Gradient Boosting
│   ├── XGBoost
│   └── LightGBM
│
├── SVM
│   └── SVM (kernel RBF)
│
└── APIs Comerciales (estimadas)
    ├── Google AutoML NLP
    ├── Amazon Comprehend
    └── Azure ML AutoML
```

### Métricas Aplicadas

- **Desempeño**: Accuracy, F1-score (macro y weighted), Precision, Recall macro.
- **Generalización**: Overfitting gap (train − val), curvas de aprendizaje 5-fold.
- **Fairness**: Disparate Impact Ratio (umbral 0,80), Equalized Odds Gap (umbral 0,10).

---

## 📈 Resultados Principales

### Ranking de Benchmarking (F1 Macro sobre Validación)

| Modelo | Acc Val | F1 Macro | F1 Weighted | Gap | Tiempo (s) |
|--------|:-------:|:--------:|:-----------:|:---:|:----------:|
| LightGBM | 1,0000 | **1,0000** | 1,0000 | 0,0000 | 2,88 |
| SVM (RBF) | 1,0000 | **1,0000** | 1,0000 | -0,0009 | 6,93 |
| XGBoost | 1,0000 | **1,0000** | 1,0000 | 0,0000 | 1,81 |
| Gradient Boosting | 1,0000 | **1,0000** | 1,0000 | 0,0000 | 131,68 |
| Regresión Logística | 0,9971 | 0,9967 | 0,9971 | 0,0020 | 3,82 |
| **Random Forest (Propuesto)** ★ | **0,9961** | **0,9910** | **0,9961** | **0,0039** | **4,70** |
| Árbol de Decisión | 0,9913 | 0,9800 | 0,9914 | 0,0027 | 0,42 |
| K-NN (k=7) | 0,9816 | 0,9690 | 0,9814 | 0,0099 | 0,01 |
| Baseline: Más Frecuente | 0,4497 | 0,1551 | 0,2790 | 0,0467 | 0,00 |
| Baseline: Aleatorio | 0,3453 | 0,2476 | 0,3389 | 0,0133 | 0,00 |

### Resumen de Fairness

| Variable Sensible | Disparate Impact | Eq. Odds Gap | Estado |
|-------------------|:----------------:|:------------:|:------:|
| Longitud de pregunta | 0,9909 | 0,0091 | ✅ Aceptable |
| Presencia de JOIN | 0,9902 | 0,0098 | ✅ Aceptable |
| Dominio BD (Top 10) | 0,9783 | 0,0217 | ✅ Aceptable |

### Diagnóstico de Generalización

- **Profundidad óptima empírica:** `max_depth = 14` (F1 Val = 0,9933)
- **Gap final Random Forest:** 0,0096 → Buen equilibrio aparente
- ⚠️ *Ver [Hallazgo Metodológico Relevante](#-hallazgo-metodológico-relevante).*

---

## 📊 Visualizaciones

<div align="center">

### Figura 1 — Benchmarking Comparativo
![Benchmarking](reports/figures/fig1_benchmarking.png)

*Paneles: (a) ranking de F1 macro, (b) accuracy train vs validation, (c) métricas por clase del modelo propuesto, (d) matriz de confusión.*

---

### Figura 2 — Análisis de Sesgo Algorítmico
![Fairness](reports/figures/fig2_fairness.png)

*Paneles: (a) accuracy por longitud de pregunta, (b) accuracy por presencia de JOIN, (c) accuracy por dominio Top 10, (d) distribución de errores por dificultad.*

---

### Figura 3 — Curvas de Aprendizaje
![Learning Curves](reports/figures/fig3_curvas_aprendizaje.png)

*Evolución del F1 macro en entrenamiento y validación para cuatro modelos comparativos. Gaps finales entre 0,0014 y 0,0096.*

---

### Figura 4 — Diagnóstico por Complejidad (max_depth)
![Max Depth](reports/figures/fig4_max_depth.png)

*Panel izquierdo: F1 macro vs max_depth con óptimo en profundidad 14. Panel derecho: overfitting gap vs complejidad con umbrales de referencia.*

</div>

---

## 📂 Estructura del Repositorio

```
Proyecto-Integrador-Inteligencia-Artificial/
│
├── 📄 README.md                          ← Este archivo
├── 📄 LICENSE                            ← Licencia MIT
├── 📄 CITATION.cff                       ← Metadatos de citación académica
├── 📄 requirements.txt                   ← Dependencias Python
├── 📄 .gitignore                         ← Archivos ignorados por git
├── 📄 CHANGELOG.md                       ← Historial de cambios
├── 📄 CONTRIBUTING.md                    ← Guía de contribución
│
├── 📁 notebooks/
│   └── 01_evaluacion_modelos_spider.ipynb   ← Notebook principal ejecutable
│
├── 📁 reports/
│   ├── Informe_Evaluacion_Modelos_IA_Spider_UEES.docx   ← Informe final (Word)
│   ├── Informe_Evaluacion_Modelos_IA_Spider_UEES.pdf    ← Informe final (PDF)
│   └── 📁 figures/
│       ├── fig1_benchmarking.png
│       ├── fig2_fairness.png
│       ├── fig3_curvas_aprendizaje.png
│       └── fig4_max_depth.png
│
├── 📁 docs/
│   ├── Apuntes_de_clase_Tutoria_3.pdf    ← Material de apoyo docente
│   ├── Rubrica_de_Evaluacion_de_Modelos_IA.pdf   ← Rúbrica oficial
│   ├── GUIA_PRESENTACION.md              ← Guía para defender el proyecto
│   └── ESTRUCTURA_SUGERIDA_SLIDES.md     ← Esqueleto de diapositivas
│
├── 📁 src/
│   └── README.md                         ← Código fuente modular (pendiente)
│
├── 📁 data/
│   └── .gitkeep                          ← Datos descargados on-the-fly desde HF Hub
│
└── 📁 .github/
    └── 📁 workflows/
        └── validate-notebook.yml         ← CI para validación del notebook
```

---

## ⚙️ Instalación y Uso

### Requisitos Previos

- Python 3.10 o superior
- pip / conda
- ~4 GB de espacio en disco (para el dataset y modelos)
- Opcional: GPU para acelerar Gradient Boosting

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/<TU_USUARIO>/Proyecto-Integrador-Inteligencia-Artificial.git
cd Proyecto-Integrador-Inteligencia-Artificial

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Ejecución

```bash
# Lanzar Jupyter y abrir el notebook principal
jupyter notebook notebooks/01_evaluacion_modelos_spider.ipynb
```

O desde VS Code / Cursor con la extensión de Jupyter instalada, abrir directamente el notebook y ejecutar `Run All`.

### Tiempo Estimado de Ejecución

| Etapa | Duración aproximada |
|-------|---------------------|
| Descarga del dataset (HF Hub) | ~1 min |
| Feature engineering | ~2 min |
| Entrenamiento de 10 modelos | ~3 min |
| Gradient Boosting (el más lento) | ~2 min |
| Curvas de aprendizaje (5-fold × 4 modelos) | ~5 min |
| Barrido de max_depth | ~2 min |
| **Total** | **~15 min** (CPU moderna) |

---

## ⚠️ Hallazgo Metodológico Relevante

El análisis crítico del estudio identificó un hallazgo técnico que **cualifica la interpretación de los resultados cuantitativos**: la sospecha fundada de **fuga de información (*data leakage*)** entre el vector de características y la etiqueta objetivo (Kaufman et al., 2012).

### Evidencia

- Prácticamente todos los modelos entrenados superan el **98% de F1 macro** sobre validación.
- Cuatro algoritmos (LightGBM, SVM RBF, XGBoost, Gradient Boosting) alcanzan **desempeño perfecto** (F1 = 1,0000).
- Incluso un árbol de decisión simple obtiene **F1 = 0,98**.
- Los gaps entre entrenamiento y validación son **casi nulos** en todos los modelos.

### Causa Raíz

La etiqueta de dificultad en Spider se calcula **algorítmicamente a partir de propiedades estructurales del SQL** (cláusulas, JOINs, subconsultas, agregaciones). Al extraer esas mismas propiedades como features (`has_join`, `num_select`, `nested_depth`, etc.), se construye un vector que es esencialmente una **reformulación numérica de la función que genera la etiqueta**.

### Implicación

> El ejercicio es didácticamente válido para practicar las tres actividades de evaluación. Los **valores absolutos** de las métricas **no deben interpretarse** como estimación realista del desempeño sobre datos no contaminados.

### Corrección Propuesta para Trabajo Futuro

- Redefinir la tarea como clasificación de dificultad **desde la pregunta natural únicamente** (sin ver el SQL de respuesta).
- Aplicar validación estrictamente cross-domain o temporal.
- Reemplazar TF-IDF + PCA por **embeddings contextuales tipo CodeBERT**.
- Reportar métricas con intervalos de confianza mediante bootstrap.

Este hallazgo se discute en detalle en la **Sección 5 del informe final**.

---

## 🛠️ Tecnologías Utilizadas

### Stack Principal

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

### Modelos de Boosting

![XGBoost](https://img.shields.io/badge/XGBoost-00599C?style=for-the-badge)
![LightGBM](https://img.shields.io/badge/LightGBM-0E83CD?style=for-the-badge)

### Visualización y Procesamiento

![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge)
![Seaborn](https://img.shields.io/badge/Seaborn-4C72B0?style=for-the-badge)
![NLTK](https://img.shields.io/badge/NLTK-009688?style=for-the-badge)

### Entorno

![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-FFD21E?style=for-the-badge)

---

## 👥 Equipo

| Rol | Nombre |
|-----|--------|
| **Autor** | Cabrera Parrales Joel David |
| **Autor** | Sánchez Arévalo Aníbal Andrés |
| **Tutora** | Mg. Alexandra J. Arciniegas C. |
| **Institución** | Universidad de Especialidades Espíritu Santo (UEES) |
| **Programa** | Maestría en Inteligencia Artificial |
| **Asignatura** | Proyecto Integrador en Inteligencia Artificial |
| **Período** | Abril 2026 |
| **Ubicación** | Samborondón, Ecuador |

---

## 📚 Referencias

Las referencias completas en formato **APA 7ª edición** se encuentran en la Sección 7 del [informe final](reports/Informe_Evaluacion_Modelos_IA_Spider_UEES.pdf). A continuación las principales:

1. **Yu, T., et al.** (2018). Spider: A large-scale human-labeled dataset for complex and cross-domain semantic parsing and text-to-SQL task. *EMNLP*, 3911–3921. [DOI:10.18653/v1/D18-1425](https://doi.org/10.18653/v1/D18-1425)

2. **Mehrabi, N., et al.** (2021). A survey on bias and fairness in machine learning. *ACM Computing Surveys*, 54(6), 1–35. [DOI:10.1145/3457607](https://doi.org/10.1145/3457607)

3. **Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O.** (2012). Leakage in data mining: Formulation, detection, and avoidance. *ACM TKDD*, 6(4), 1–21. [DOI:10.1145/2382577.2382579](https://doi.org/10.1145/2382577.2382579)

4. **Scholak, T., Schucher, N., & Bahdanau, D.** (2021). PICARD: Parsing incrementally for constrained auto-regressive decoding from language models. *EMNLP*, 9895–9901.

5. **Barocas, S., & Selbst, A. D.** (2016). Big data's disparate impact. *California Law Review*, 104(3), 671–732.

6. **Géron, A.** (2019). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (2.ª ed.). O'Reilly Media.

---

## 🎓 Cómo Citar este Trabajo

Si este trabajo te resulta útil para investigación o referencia académica, por favor cita:

```bibtex
@misc{cabrera_sanchez_2026_spider_uees,
  author       = {Cabrera Parrales, Joel David and Sánchez Arévalo, Aníbal Andrés},
  title        = {Evaluación de Modelos de IA sobre el Dataset Spider:
                  Benchmarking, Sesgo Algorítmico y Diagnóstico de Generalización},
  year         = {2026},
  institution  = {Universidad de Especialidades Espíritu Santo (UEES)},
  howpublished = {\url{https://github.com/<TU_USUARIO>/Proyecto-Integrador-Inteligencia-Artificial}},
  note         = {Proyecto Integrador en Inteligencia Artificial, Maestría en IA}
}
```

Alternativamente, usa el archivo [`CITATION.cff`](CITATION.cff) incluido en este repositorio — GitHub lo detecta automáticamente y muestra un botón "Cite this repository" en la página del repo.

---

## 📄 Licencia

Este proyecto está licenciado bajo la **Licencia MIT** — consulta el archivo [LICENSE](LICENSE) para más detalles.

El dataset Spider está licenciado bajo **CC BY-SA 4.0** por sus autores originales.

---

<div align="center">

**Universidad de Especialidades Espíritu Santo — Maestría en Inteligencia Artificial**

*Samborondón, Ecuador · Abril 2026*

[![UEES](https://img.shields.io/badge/🎓-UEES-821538?style=for-the-badge)](https://www.uees.edu.ec/)

</div>
