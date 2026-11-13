# Analizador-Web

**Skill bilingüe de inspección y auditoría de sitios web / Bilingual Website Audit & Inspection Agent Skill**

Analizador-Web es una Agent Skill independiente y portable, mantenida por [@victorlpz3293](https://github.com/victorlpz3293). Permite que agentes de IA compatibles inspeccionen sitios web públicos mediante un navegador Chromium real, utilizando el framework oficial [Playwright para Python](https://playwright.dev/python/).

La Skill y su documentación están disponibles en español e inglés. El agente debe responder en el idioma del usuario y puede generar informes completos en cualquiera de los dos idiomas.

**English documentation:** see [README.en.md](README.en.md).

## Qué hace

- Renderiza sitios web con JavaScript en Chromium.
- Captura pantallas completas en escritorio y móvil.
- Recopila metadatos SEO técnicos y estructura de encabezados.
- Mide tiempos del navegador e indicadores de recursos transferidos.
- Identifica recursos potencialmente pesados y firmas tecnológicas (heurísticas).
- Reporta indicadores seleccionados de accesibilidad.
- Revisa HTTPS/TLS y encabezados de seguridad comunes.
- Registra errores de consola, solicitudes fallidas y respuestas HTTP de error.
- Comprueba una cantidad limitada de enlaces del mismo host usando únicamente solicitudes HEAD.
- Exporta evidencia en JSON y Markdown para revisión humana o por IA.

## Qué no hace

Está diseñada para la inspección pasiva de sitios web públicos. No realiza pruebas de penetración, explota vulnerabilidades, enumera puertos, sondea bases de datos o APIs, elude controles de acceso ni supera protecciones anti-bot. Tampoco envía formularios reales de forma predeterminada.

## Requisitos

- Python 3.10 o posterior.
- Playwright para Python.
- Chromium instalado mediante Playwright. Si se utiliza un binario Chromium administrado por el sistema, configura `PLAYWRIGHT_CHROMIUM_EXECUTABLE` con su ruta completa.
- Acceso a Internet durante la instalación inicial de dependencias/navegador y para acceder al sitio público objetivo.

## Inicio rápido

Desde la raíz del repositorio:

```bash
bash skills/analizador-web/scripts/setup.sh
.venv/bin/python skills/analizador-web/scripts/analyze_site.py https://example.com --out ./website-audit
```

Configuración en Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r skills/analizador-web/requirements.txt
python -m playwright install chromium
python skills/analizador-web/scripts/analyze_site.py https://example.com --out .\website-audit
```

Consulta [SKILL.md](skills/analizador-web/SKILL.md) para las instrucciones del agente, opciones y reglas de seguridad. Las listas de verificación están en [español](skills/analizador-web/references/checklist.es.md) e [inglés](skills/analizador-web/references/checklist.en.md). Ejecuta las pruebas de seguridad con `python -m unittest discover -s tests -v`.

## Instalar como Agent Skill

Este repositorio sigue la convención de carpetas abierta de Agent Skills. Instala o copia `skills/analizador-web/` en el directorio de Skills documentado por tu agente.

Ejemplos:

- Claude Code (ámbito de usuario): `~/.claude/skills/analizador-web/`
- Claude Code (ámbito de proyecto): `.claude/skills/analizador-web/`
- Otros clientes compatibles con Agent Skills: utiliza el directorio de Skills documentado por cada cliente.

Para Claude.ai, genera el ZIP con `python scripts/package_skill.py` (Windows: `py scripts/package_skill.py`). Sube `dist/analizador-web-1.1.0.zip` mediante **Settings / Customize → Skills** (la disponibilidad y los nombres de los menús pueden variar según el plan y la versión del cliente). El paquete coloca `SKILL.md` en la raíz del ZIP, según requiere el flujo de carga de Skills.

Las instrucciones pueden cargarse en clientes compatibles con Agent Skills. La ejecución de scripts depende además de que el entorno disponga de Python, Playwright, Chromium y acceso de red permitido.

## Modelo de seguridad

De forma predeterminada, los scripts:

- Aceptan únicamente URLs HTTP(S) en los puertos estándar 80 y 443.
- Rechazan hosts que resuelven a direcciones IP loopback, privadas, link-local, reservadas o no públicas.
- Aplican la validación de destino a solicitudes HTTP(S) del navegador, incluidas redirecciones y subrecursos.
- Bloquean métodos HTTP de escritura (`POST`, `PUT`, `PATCH`, `DELETE`, etc.).
- Mantienen deshabilitadas las acciones de interacción (`click`, `fill`, `press`) salvo habilitación explícita.
- No reintentan con GET los enlaces cuyo chequeo HEAD falla.
- Limitan el rastreo a 20 páginas en total.
- Omiten fragmentos del texto renderizado salvo solicitud explícita.

Estos controles a nivel de aplicación reducen riesgos, pero no constituyen un sandbox reforzado ni eliminan riesgos de DNS rebinding, navegador, dependencias o infraestructura. La interceptación de solicitudes del navegador también puede afectar los tiempos observados. Utiliza un entorno aislado y obtén autorización antes de evaluar un sitio.

## Privacidad

Los artefactos pueden contener títulos, metadatos, URLs, nombres de recursos, errores del navegador y capturas de pantalla. Los scripts redactan los valores de query strings en las URLs que escriben y desactivan por defecto los fragmentos de texto. Las capturas y metadatos aún pueden contener información sensible. Revisa los artefactos antes de publicarlos o compartirlos.

## Estructura del proyecto

```text
skills/analizador-web/
├── SKILL.md
├── references/
│   ├── checklist.md
│   ├── checklist.es.md
│   └── checklist.en.md
├── scripts/
│   ├── analyze_site.py
│   ├── interact.py
│   └── safety.py
└── requirements.txt
```

## Atribución e independencia

Analizador-Web es una Skill comunitaria independiente mantenida por **@victorlpz3293**. Utiliza el framework Playwright; Playwright es un proyecto de Microsoft distribuido bajo Apache License 2.0. Este repositorio no está afiliado, patrocinado ni respaldado por Microsoft o Anthropic. Los nombres de productos y empresas se utilizan únicamente para identificar software compatible.

## Licencia

El material original de este repositorio se publica bajo MIT License. Consulta [LICENSE](LICENSE). El software de terceros (incluidos Playwright y Chromium) conserva sus propias licencias.

## Contribuciones y seguridad

Las contribuciones son bienvenidas. Consulta [CONTRIBUTING.md](CONTRIBUTING.md) y [SECURITY.md](SECURITY.md), disponibles también en inglés mediante los archivos `.en.md`.
