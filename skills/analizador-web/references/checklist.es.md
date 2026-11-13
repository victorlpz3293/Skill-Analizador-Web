# Lista de verificación de auditoría — Analizador-Web

Utiliza esta lista para interpretar el informe JSON y las capturas. Es una ayuda de inspección, no una certificación formal.

## Alcance y evidencia
- [ ] Confirma la autorización y el alcance objetivo.
- [ ] Registra la URL exacta, fecha/hora, viewport, límite de rastreo y versión de la herramienta.
- [ ] Distingue hechos observados, detecciones heurísticas y suposiciones.
- [ ] Registra páginas bloqueadas, tiempos de espera agotados, desafíos anti-bot y otras limitaciones.

## Calidad visual y experiencia de usuario
- [ ] ¿Se entiende el propósito del sitio en pocos segundos?
- [ ] ¿La llamada a la acción principal es visible y clara?
- [ ] ¿La jerarquía visual es coherente?
- [ ] ¿El tamaño del texto, longitud de línea, espaciado y contraste son cómodos?
- [ ] ¿Hay elementos superpuestos, imágenes rotas, banners intrusivos o saltos de diseño?
- [ ] En móvil, ¿el texto es legible sin ampliar?
- [ ] ¿Los objetivos interactivos tienen tamaño y separación suficientes?
- [ ] ¿Existe desbordamiento horizontal?
- [ ] ¿La navegación y el contenido clave funcionan en anchos reducidos?

## SEO técnico
- [ ] El título existe, es descriptivo y razonablemente único.
- [ ] Existe una meta description que describe la página.
- [ ] La jerarquía de encabezados tiene sentido; revisa H1 ausentes o excesivos.
- [ ] El idioma del documento está declarado.
- [ ] Existe metadato viewport.
- [ ] La URL canonical existe y parece correcta.
- [ ] Los metadatos Open Graph están disponibles cuando compartir es relevante.
- [ ] Las directivas robots no bloquean la indexación accidentalmente.
- [ ] El contenido importante está renderizado y puede descubrirse.

## Indicadores de rendimiento
- [ ] Revisa navigation timing, DOMContentLoaded, load y paint cuando estén disponibles.
- [ ] Revisa indicadores de tamaño transferido y cantidad de recursos.
- [ ] Identifica recursos inusualmente grandes y scripts de terceros.
- [ ] Considera formatos de imagen, imágenes responsivas, lazy loading, caché y CDN.
- [ ] Trata las mediciones como una única ejecución de navegador afectada por red, caché, ubicación e interceptación de solicitudes.
- [ ] Utiliza Lighthouse o PageSpeed Insights por separado para una evaluación más completa.

## Señales de accesibilidad
- [ ] Las imágenes tienen texto alternativo apropiado (las decorativas pueden usar alt vacío).
- [ ] Los controles de formulario tienen etiquetas programáticas.
- [ ] Los enlaces y botones tienen nombres accesibles.
- [ ] El idioma de la página está declarado.
- [ ] El foco de teclado es visible y la navegación es posible.
- [ ] El contraste se revisa con una herramienta dedicada.
- [ ] El orden de encabezados y landmarks tiene sentido.
- [ ] No declares conformidad WCAG basándote únicamente en esta lista.

## Observaciones de configuración de seguridad
- [ ] Se utiliza HTTPS.
- [ ] La validación del certificado funciona en un contexto normal de navegador.
- [ ] Revisa HSTS, CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy y protecciones de framing.
- [ ] Trata los encabezados que identifican el servidor como exposición informativa, no automáticamente como vulnerabilidad.
- [ ] No infieras la seguridad de la aplicación únicamente a partir de encabezados públicos.
- [ ] No explotes, sondees endpoints ocultos ni pruebes autenticación.

## Fiabilidad
- [ ] Revisa errores de consola JavaScript.
- [ ] Revisa solicitudes de red fallidas.
- [ ] Revisa respuestas HTTP con estado 4xx/5xx.
- [ ] Comprueba enlaces del mismo host únicamente cuando se solicite explícitamente.
- [ ] Considera incompletos los chequeos HEAD: algunos servidores rechazan HEAD.

## Priorización
- **Alta:** página principal no disponible, navegación primaria rota, fallo grave de diseño móvil, errores generalizados de aplicación o contenido importante inaccesible.
- **Media:** metadatos esenciales ausentes, recursos pesados, errores de consola recurrentes o encabezados defensivos ausentes cuando sean apropiados.
- **Baja:** inconsistencias visuales menores, metadatos no críticos u optimizaciones opcionales.

Cada hallazgo debe incluir evidencia, impacto, confianza y una acción concreta.
