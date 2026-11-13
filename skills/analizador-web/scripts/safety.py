"""Defensive URL validation for passive public-site inspection.

These checks reduce accidental access to private networks; they are not a
replacement for OS/container egress controls or a hardened browser sandbox.
"""
from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlsplit, urlunsplit


class UnsafeTarget(ValueError):
    pass


def validate_public_url(url: str) -> str:
    try:
        parts = urlsplit(url)
        port = parts.port
    except ValueError as exc:
        raise UnsafeTarget("Malformed URL or port") from exc

    if parts.scheme.lower() not in ("http", "https"):
        raise UnsafeTarget("Only HTTP and HTTPS URLs are allowed")
    if not parts.hostname:
        raise UnsafeTarget("URL must include a hostname")
    if parts.username is not None or parts.password is not None:
        raise UnsafeTarget("Credentials in URLs are not allowed")
    if port is not None and port not in (80, 443):
        raise UnsafeTarget("Only standard HTTP/HTTPS ports are allowed")

    host = parts.hostname.rstrip(".").lower()
    if host == "localhost" or host.endswith(".localhost") or host.endswith(".local"):
        raise UnsafeTarget("Local hostnames are not allowed")

    try:
        addresses = {ipaddress.ip_address(host)}
    except ValueError:
        try:
            answers = socket.getaddrinfo(host, port or (443 if parts.scheme == "https" else 80),
                                         type=socket.SOCK_STREAM)
        except OSError as exc:
            raise UnsafeTarget(f"DNS resolution failed: {exc}") from exc
        addresses = {ipaddress.ip_address(item[4][0].split("%")[0]) for item in answers}

    if not addresses:
        raise UnsafeTarget("Hostname did not resolve")
    for address in addresses:
        if not address.is_global:
            raise UnsafeTarget(f"Non-public destination blocked: {address}")

    # Remove fragments; preserve query for navigation but redact it in reports.
    return urlunsplit((parts.scheme.lower(), parts.netloc, parts.path or "/", parts.query, ""))


def redact_url(url: str) -> str:
    """Remove query and fragment values from URLs written to reports."""
    try:
        p = urlsplit(url)
        return urlunsplit((p.scheme, p.netloc, p.path, "", ""))
    except Exception:
        return "[invalid-url]"
