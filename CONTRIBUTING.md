# Guía de Contribución

¡Gracias por tu interés en contribuir al Proyecto Integrador en Inteligencia Artificial! Este documento resume las directrices para proponer mejoras, reportar problemas o extender el trabajo.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
- [Flujo de Trabajo con Git](#flujo-de-trabajo-con-git)
- [Estilo de Código](#estilo-de-código)
- [Commits](#commits)
- [Pull Requests](#pull-requests)

---

## Código de Conducta

Este proyecto es un trabajo académico de la Maestría en Inteligencia Artificial de la UEES. Se espera que todos los participantes mantengan un trato profesional, respetuoso y constructivo.

- **Sé respetuoso:** las críticas deben ser constructivas y enfocarse en el trabajo, no en la persona.
- **Sé claro:** explica tu razonamiento con evidencia técnica o referencias académicas.
- **Sé colaborativo:** busca el consenso y estás dispuesto a revisar tu posición.

---

## ¿Cómo puedo contribuir?

### 🐛 Reportar un problema

Si encuentras un error en el código, en los resultados, en la documentación o en el informe, abre un *Issue* describiendo:

1. **Qué esperabas que ocurriera.**
2. **Qué ocurrió realmente.**
3. **Pasos para reproducir el problema.**
4. **Entorno:** versión de Python, sistema operativo, versiones de paquetes relevantes.

### 💡 Proponer una mejora

Antes de implementar un cambio significativo, abre un *Issue* de tipo "enhancement" y discútelo con los autores. Esto evita duplicar esfuerzos y asegura que el cambio encaje con los objetivos del proyecto.

### 🔬 Extender el análisis

Las extensiones más valiosas para este proyecto son:

- **Reemplazar el pipeline actual** por uno libre de *data leakage* (ver Sección 5 del informe).
- **Incorporar embeddings contextuales** (CodeBERT, SchemaLinking) como features.
- **Ejecución empírica directa** de las APIs comerciales en vez de estimaciones.
- **Validación cross-domain reforzada** con intervalos de confianza por bootstrap.
- **Tests unitarios** sobre las funciones de feature engineering.

---

## Flujo de Trabajo con Git

Este repositorio sigue un flujo **GitHub Flow** simplificado:

```bash
# 1. Hacer fork del repositorio en GitHub

# 2. Clonar tu fork
git clone https://github.com/<TU_USUARIO>/Proyecto-Integrador-Inteligencia-Artificial.git
cd Proyecto-Integrador-Inteligencia-Artificial

# 3. Crear una rama descriptiva
git checkout -b feat/nueva-metrica-fairness
# o
git checkout -b fix/corregir-bug-pipeline
# o
git checkout -b docs/mejorar-readme

# 4. Hacer cambios y commits siguiendo la convención
git add .
git commit -m "feat(fairness): agregar métrica de Equal Opportunity Difference"

# 5. Subir a tu fork
git push origin feat/nueva-metrica-fairness

# 6. Abrir un Pull Request desde GitHub hacia el repositorio principal
```

### Convenciones de Nombrado de Ramas

| Prefijo | Uso | Ejemplo |
|---------|-----|---------|
| `feat/` | Nueva funcionalidad | `feat/embeddings-codebert` |
| `fix/` | Corrección de bug | `fix/pipeline-memory-leak` |
| `docs/` | Cambios en documentación | `docs/traducir-readme-ingles` |
| `refactor/` | Refactorización sin cambio funcional | `refactor/extraer-modulos-src` |
| `test/` | Añadir o corregir tests | `test/cubrir-feature-engineering` |
| `chore/` | Mantenimiento (deps, CI, etc.) | `chore/actualizar-dependencias` |

---

## Estilo de Código

### Python

- **Seguir PEP 8** con línea máxima de 100 caracteres.
- **Usar type hints** en funciones públicas.
- **Docstrings en formato Google** para funciones y clases.
- **Preferir f-strings** sobre `.format()` o concatenación.

Ejemplo:

```python
def compute_disparate_impact(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    groups: np.ndarray
) -> float:
    """Calcula el Disparate Impact Ratio entre grupos.

    Args:
        y_true: Etiquetas reales.
        y_pred: Etiquetas predichas.
        groups: Etiquetas de grupo para cada muestra.

    Returns:
        Ratio entre el accuracy del grupo con peor desempeño y el mejor.
        Valor por debajo de 0.80 indica sesgo significativo.
    """
    ...
```

### Notebooks

- **Celdas markdown antes de cada sección** explicando el objetivo.
- **Reproducibilidad:** fijar `random_state` en todos los estimadores y splits.
- **Limpiar outputs** antes de commit si el notebook pesa más de 5 MB.
- **No ejecutar celdas lentas** en el commit final salvo que aporten valor visual.

---

## Commits

Este proyecto sigue la convención **Conventional Commits**:

```
<tipo>(<alcance opcional>): <descripción breve>

<cuerpo opcional explicando el porqué>

<footer opcional con referencias a issues>
```

### Tipos Válidos

| Tipo | Cuándo usar |
|------|-------------|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `docs` | Solo cambios en documentación |
| `style` | Formato, espacios, sin cambio funcional |
| `refactor` | Refactorización sin añadir ni corregir |
| `perf` | Mejora de rendimiento |
| `test` | Añadir o corregir tests |
| `chore` | Mantenimiento (build, deps, CI) |

### Ejemplos

```bash
git commit -m "feat(benchmarking): agregar comparación con CatBoost"
git commit -m "fix(fairness): corregir división por cero en Disparate Impact"
git commit -m "docs(readme): actualizar tabla de resultados con nuevos runs"
git commit -m "refactor(pipeline): extraer feature engineering a src/features.py"
```

---

## Pull Requests

Un Pull Request bien hecho facilita la revisión y acelera la integración.

### Checklist Antes de Abrir el PR

- [ ] El código sigue el estilo descrito arriba.
- [ ] Los commits siguen Conventional Commits.
- [ ] El notebook se ejecuta de principio a fin sin errores.
- [ ] Se actualizó el `CHANGELOG.md` bajo la sección `[Unreleased]`.
- [ ] Si se añadieron dependencias, están en `requirements.txt` con versión mínima.
- [ ] Se añadió o actualizó documentación relevante.
- [ ] Se incluyó una descripción clara en el PR explicando **qué** cambia y **por qué**.

### Plantilla Sugerida para el PR

```markdown
## Descripción

Explicar brevemente qué hace este PR.

## Motivación

¿Por qué es necesario este cambio? ¿Qué problema resuelve?

## Cambios

- Cambio 1
- Cambio 2
- Cambio 3

## Tipo de cambio

- [ ] Bug fix (cambio que corrige un problema)
- [ ] Nueva funcionalidad (cambio que añade capacidad)
- [ ] Breaking change (cambio que rompe compatibilidad)
- [ ] Documentación

## ¿Cómo se probó?

Describir los pasos para verificar que el cambio funciona.

## Capturas de pantalla (si aplica)
```

---

## ❓ Preguntas

Si tienes dudas sobre cómo contribuir, abre un *Issue* con la etiqueta `question` o contacta a los autores del proyecto.

¡Gracias por contribuir! 🎓
