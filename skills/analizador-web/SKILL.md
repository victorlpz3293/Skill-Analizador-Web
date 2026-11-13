---
name: analizador-web
description: "Inspect and audit public websites with Chromium and Playwright for Python. Use when asked to analyze, review, audit, compare, inspect, or navigate a website, landing page, or online store; capture desktop/mobile screenshots; examine technical SEO, performance indicators, accessibility signals, security headers, browser errors, or internal links. Responde y genera informes en español o inglés según el idioma solicitado por el usuario."
---

# Analizador-Web

> **Bilingual skill / Skill bilingüe:** The instructions below are provided in Spanish and English. / Las instrucciones siguientes se ofrecen en español e inglés.

## 1. Idioma y comportamiento / Language and behavior

### Español
- Responde en el idioma utilizado por el usuario. Si el usuario solicita explícitamente otro idioma, utiliza ese idioma.
- Puedes generar informes completos en español o inglés. Conserva los nombres técnicos, comandos, rutas, identificadores y valores originales cuando traducirlos pueda causar ambigüedad.
- No mezcles idiomas dentro de una misma sección del informe, salvo para términos técnicos, nombres propios o cuando sea necesario para mantener la precisión.
- La documentación de esta Skill está disponible en ambos idiomas: consulta `references/checklist.es.md` para la lista de verificación en español y `references/checklist.en.md` para la versión inglesa.

### English
- Respond in the language used by the user. If the user explicitly requests another language, use that language.
- You can produce complete reports in Spanish or English. Preserve technical names, commands, paths, identifiers, and original values whenever translating them could create ambiguity.
- Do not mix languages within the same report section, except for technical terms, proper names, or when needed for accuracy.
- This Skill's documentation is available in both languages: use `references/checklist.en.md` for the English checklist and `references/checklist.es.md` for the Spanish version.

## 2. Propósito / Purpose

### Español
Analizador-Web proporciona un flujo de trabajo repetible para inspeccionar sitios web renderizados mediante un navegador Chromium real, en lugar de depender únicamente del HTML sin procesar o de la extracción de texto. Utiliza Chromium a través de la biblioteca oficial Playwright para Python.

### English
Analizador-Web provides a repeatable workflow for inspecting rendered websites through a real Chromium browser instead of relying only on raw HTML or text extraction. It uses Chromium through the official Playwright for Python library.

## 3. Seguridad y autorización / Safety and authorization

### Español
- Alcance predeterminado: inspección pasiva de páginas HTTP(S) de acceso público.
- Inspecciona únicamente sitios que el usuario posea o para los que tenga autorización. En sitios de terceros, limita el trabajo a la observación ordinaria de páginas públicas.
- No intentes explotar vulnerabilidades, validar su explotación, evadir autenticación, escanear puertos, realizar fuerza bruta de directorios, enumerar APIs, acceder a bases de datos ni eludir protecciones anti-bot.
- No envíes formularios, crees cuentas, realices pedidos, publiques comentarios, cargues archivos ni modifiques el estado remoto durante una auditoría predeterminada.
- Nunca introduzcas credenciales, tokens, cookies ni datos personales en el sitio objetivo.
- No sigas enlaces hacia destinos de redes no públicas. Los scripts aplican controles de direcciones públicas, pero son defensa en profundidad, no un aislamiento de red reforzado.
- Detente si el sitio solicita autenticación, presenta un desafío o bloquea el acceso automatizado. Informa la limitación; no intentes eludirla.
- Obtén autorización explícita antes de usar el modo opcional de interacción. Incluso con autorización, evita acciones que envíen o modifiquen datos.

### English
- Default scope: passive inspection of publicly accessible HTTP(S) pages.
- Inspect only sites the user owns or is authorized to assess. For third-party sites, limit work to ordinary observation of public pages.
- Do not exploit or validate vulnerabilities, bypass authentication, scan ports, brute-force directories, enumerate APIs, access databases, or circumvent bot protections.
- Do not submit forms, create accounts, place orders, post comments, upload files, or change remote state during a default audit.
- Never enter credentials, tokens, cookies, or personal data into a target site.
- Do not follow links to non-public network destinations. The scripts apply public-address checks, but these are defense-in-depth controls, not a hardened network sandbox.
- Stop if the target requests authentication, presents a challenge, or blocks automated access. Report the limitation instead of attempting to bypass it.
- Obtain explicit authorization before using the optional interaction mode. Even then, avoid actions that submit or modify data.

## 4. Instalación / Setup

### Español
Desde la raíz del repositorio:

```bash
bash skills/analizador-web/scripts/setup.sh
```

Instalación manual:

```bash
python -m pip install -r skills/analizador-web/requirements.txt
python -m playwright install chromium
```

### English
From the repository root:

```bash
bash skills/analizador-web/scripts/setup.sh
```

Manual installation:

```bash
python -m pip install -r skills/analizador-web/requirements.txt
python -m playwright install chromium
```

## 5. Ejecutar una auditoría / Run an audit

```bash
python skills/analizador-web/scripts/analyze_site.py https://example.com --out ./website-audit
```

### Opciones / Options

- `--crawl N`: inspecciona hasta N páginas HTML adicionales del mismo host (predeterminado 0; máximo 20). / Inspect up to N additional same-host HTML pages (default 0; maximum 20).
- `--no-mobile`: omite la captura móvil. / Skip the mobile viewport screenshot.
- `--wait MS`: espera adicional después de cargar la página (predeterminado 1000). / Extra wait after page load (default 1000).
- `--timeout MS`: tiempo límite de navegación (predeterminado 30000). / Navigation timeout (default 30000).
- `--check-links N`: comprueba hasta N enlaces del mismo host usando únicamente HEAD (predeterminado 0; máximo 40). / Check up to N same-host links using HEAD only (default 0; maximum 40).
- `--include-text-excerpt`: incluye un fragmento breve del texto renderizado en el informe JSON; está desactivado de forma predeterminada. / Include a short rendered-text excerpt in the JSON report; disabled by default.

La salida incluye `report.json`, `summary.md` y capturas dentro de `screenshots/`. / Output includes `report.json`, `summary.md`, and screenshots under `screenshots/`.

## 6. Revisar la evidencia / Review the evidence

### Español
1. Lee `summary.md` y `report.json`.
2. Abre las capturas de escritorio y móvil. No infieras la calidad visual únicamente a partir de métricas.
3. Separa los hechos observados de las hipótesis. La detección de tecnologías es heurística.
4. Trata los tiempos del navegador como observaciones de una ejecución, no como un benchmark de laboratorio.
5. Indica expresamente las mediciones no disponibles. No presentes la auditoría como una prueba de penetración ni como una certificación formal de accesibilidad.
6. Utiliza la lista de verificación en el idioma del informe: `references/checklist.es.md` o `references/checklist.en.md`.

### English
1. Read `summary.md` and `report.json`.
2. Open desktop and mobile screenshots. Do not infer visual quality from metrics alone.
3. Separate observed facts from hypotheses. Technology detection is heuristic.
4. Treat browser timings as observations from a single run, not laboratory benchmarks.
5. Explicitly report unavailable measurements. Do not describe the audit as a penetration test or formal accessibility certification.
6. Use the checklist matching the report language: `references/checklist.en.md` or `references/checklist.es.md`.

## 7. Interacción controlada opcional / Optional controlled interaction

### Español
El script de interacción es de solo lectura de forma predeterminada. Admite navegación, esperas, desplazamiento, capturas y extracción de texto sin habilitar controles de la página.

```bash
python skills/analizador-web/scripts/interact.py https://example.com --steps ./steps.json --out ./website-audit
```

Las acciones opcionales `click`, `fill` y `press` requieren `--allow-interactions`. Esta opción no concede permiso para enviar formularios ni modificar datos de producción. Utilízala únicamente en un entorno de pruebas autorizado y con cuentas de prueba. No actives controles de compra, eliminación, publicación, pago o envío.

Ejemplo de pasos de solo lectura:

```json
[
  {"action": "wait", "ms": 1000},
  {"action": "scroll", "y": 700},
  {"action": "screenshot", "name": "below-fold", "full_page": true},
  {"action": "text", "selector": "main"}
]
```

### English
The interaction script is read-only by default. It supports navigation, waits, scrolling, screenshots, and text extraction without enabling page controls.

```bash
python skills/analizador-web/scripts/interact.py https://example.com --steps ./steps.json --out ./website-audit
```

The optional `click`, `fill`, and `press` actions require `--allow-interactions`. This flag does not grant permission to submit forms or change production data. Use it only in an authorized test environment with test accounts. Do not activate purchase, delete, publish, payment, or submission controls.

Example read-only steps:

```json
[
  {"action": "wait", "ms": 1000},
  {"action": "scroll", "y": 700},
  {"action": "screenshot", "name": "below-fold", "full_page": true},
  {"action": "text", "selector": "main"}
]
```

## 8. Formato del informe / Reporting format

### Español
Incluye:
1. Alcance, URL objetivo, fecha/hora y limitaciones.
2. Resumen ejecutivo con las observaciones de mayor impacto.
3. Revisión visual de las capturas de escritorio y móvil.
4. Observaciones de SEO técnico.
5. Indicadores de rendimiento y recursos.
6. Señales de accesibilidad que requieren revisión manual.
7. Observaciones sobre HTTPS y encabezados de respuesta.
8. Errores de consola, solicitudes fallidas y errores HTTP.
9. Recomendaciones priorizadas con evidencia y nivel de confianza.
10. Elementos no evaluados.

Nunca afirmes que existe una vulnerabilidad únicamente porque falte un encabezado. Describe los encabezados ausentes como observaciones de configuración y explica su contexto.

### English
Include:
1. Scope, target URL, date/time, and limitations.
2. Executive summary with the highest-impact observations.
3. Visual review of desktop and mobile screenshots.
4. Technical SEO observations.
5. Performance indicators and resource findings.
6. Accessibility signals requiring manual review.
7. HTTPS and response-header observations.
8. Console errors, failed requests, and HTTP errors.
9. Prioritized recommendations with evidence and confidence.
10. Items not tested.

Never claim a vulnerability solely because a header is absent. Describe missing headers as configuration observations and explain their context.
