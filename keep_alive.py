#!/usr/bin/env python3
"""Ping configured HTTP(S) endpoints and report response status."""
import concurrent.futures
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

TIMEOUT_SECONDS = 45
MAX_WORKERS = 10
USER_AGENT = "KeepAlive-Monitor/1.0"


def load_urls():
    # Recommended: set KEEPALIVE_URLS as a GitHub Actions repository secret,
    # with one full https:// URL per line. targets.txt is a convenient fallback.
    secret_value = os.getenv("KEEPALIVE_URLS", "").strip()
    if secret_value:
        raw_lines = secret_value.splitlines()
    else:
        config = Path("targets.txt")
        raw_lines = config.read_text(encoding="utf-8").splitlines() if config.exists() else []

    urls = []
    for line in raw_lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if not (line.startswith("https://") or line.startswith("http://")):
            print(f"IGNORADO | URL inválida (use http:// ou https://): {line}")
            continue
        urls.append(line)

    # Avoid accidentally pinging the same URL multiple times.
    return list(dict.fromkeys(urls))


def ping(url):
    started = time.monotonic()
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            status = response.status
            elapsed = time.monotonic() - started
            ok = 200 <= status < 400
            label = "OK" if ok else "FALHA"
            print(f"{label} | HTTP {status} | {elapsed:.2f}s | {url}")
            return ok
    except urllib.error.HTTPError as exc:
        elapsed = time.monotonic() - started
        print(f"FALHA | HTTP {exc.code} | {elapsed:.2f}s | {url}")
        return False
    except Exception as exc:
        elapsed = time.monotonic() - started
        print(f"FALHA | {type(exc).__name__}: {exc} | {elapsed:.2f}s | {url}")
        return False


def main():
    urls = load_urls()
    if not urls:
        raise SystemExit(
            "Nenhuma URL configurada. Defina o segredo KEEPALIVE_URLS "
            "ou adicione URLs em targets.txt."
        )

    print(f"Keep Alive iniciado: {len(urls)} URL(s). Timeout por URL: {TIMEOUT_SECONDS}s.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(urls))) as pool:
        results = list(pool.map(ping, urls))

    passed = sum(results)
    failed = len(results) - passed
    print(f"Resumo: {passed} OK | {failed} falha(s) | total {len(results)}.")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
