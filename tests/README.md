# Pruebas / Tests

## Español
Ejecuta las pruebas unitarias de seguridad desde la raíz del repositorio:

```bash
python -m unittest discover -s tests -v
```

Las pruebas cubren el esquema de URL, credenciales, puertos, localhost, rechazo de direcciones privadas obtenidas por DNS, aceptación de direcciones públicas y redacción de URLs. No sustituyen las pruebas end-to-end del navegador ni las restricciones de salida de red a nivel del sistema operativo.

## English
Run the safety unit tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

The tests cover URL scheme, credentials, ports, localhost, DNS-to-private-address rejection, public-address acceptance, and URL redaction. They do not replace end-to-end browser tests or OS-level egress restrictions.
