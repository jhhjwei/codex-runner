#!/usr/bin/env python3
"""Small, polite crawler for public password-free webpages."""

from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class PageParser(HTMLParser):
    SKIP_TAGS = {"script", "style", "noscript", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.links: list[str] = []
        self._skip_depth = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        cleaned = " ".join(data.split())
        if not cleaned:
            return
        self.text_parts.append(cleaned)
        if self._in_title:
            self.title_parts.append(cleaned)

    def result(self) -> tuple[str, str, list[str]]:
        title = " ".join(self.title_parts).strip()
        text = " ".join(self.text_parts).strip()
        return title, text, self.links


def load_config(path: Path) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    urls = config.get("start_urls")
    if not isinstance(urls, list) or not urls:
        raise ValueError("config.start_urls must be a non-empty list")

    normalized_urls = []
    for value in urls:
        url = str(value).strip()
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"invalid start URL: {url}")
        normalized_urls.append(url)

    return {
        "start_urls": normalized_urls,
        "same_domain_only": bool(config.get("same_domain_only", True)),
        "max_pages": max(1, int(config.get("max_pages", 10))),
        "delay_seconds": max(0.0, float(config.get("delay_seconds", 1.0))),
        "timeout_seconds": max(1.0, float(config.get("timeout_seconds", 20))),
        "user_agent": str(
            config.get(
                "user_agent",
                "PublicTextScraper/1.0 (+https://github.com/jhhjwei/codex-runner)",
            )
        ),
    }


def canonicalize(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit(
        (parsed.scheme.lower(), parsed.netloc.lower(), parsed.path or "/", parsed.query, "")
    )


def allowed_link(url: str, root_domain: str, same_domain_only: bool) -> bool:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    if same_domain_only and parsed.netloc.lower() != root_domain.lower():
        return False
    return True


def robots_for(url: str, user_agent: str) -> urllib.robotparser.RobotFileParser:
    parsed = urllib.parse.urlparse(url)
    robots_url = urllib.parse.urlunparse(
        (parsed.scheme, parsed.netloc, "/robots.txt", "", "", "")
    )
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(robots_url)
    try:
        parser.read()
    except (OSError, urllib.error.URLError):
        parser.parse([])
    return parser


def fetch_page(url: str, user_agent: str, timeout: float) -> tuple[str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get_content_type()
        if content_type not in {"text/html", "application/xhtml+xml"}:
            raise ValueError(f"unsupported content type: {content_type}")
        charset = response.headers.get_content_charset() or "utf-8"
        body = response.read().decode(charset, errors="replace")
        return response.geturl(), body


def crawl(config: dict[str, Any]) -> list[dict[str, Any]]:
    queue: deque[tuple[str, str]] = deque()
    for start_url in config["start_urls"]:
        queue.append((start_url, urllib.parse.urlparse(start_url).netloc))

    visited: set[str] = set()
    robots_cache: dict[str, urllib.robotparser.RobotFileParser] = {}
    records: list[dict[str, Any]] = []

    while queue and len(records) < config["max_pages"]:
        requested_url, root_domain = queue.popleft()
        normalized = canonicalize(requested_url)
        if normalized in visited:
            continue
        visited.add(normalized)

        parsed = urllib.parse.urlparse(requested_url)
        robots = robots_cache.setdefault(
            parsed.netloc,
            robots_for(requested_url, config["user_agent"]),
        )
        if not robots.can_fetch(config["user_agent"], requested_url):
            records.append({
                "url": requested_url,
                "title": "",
                "text": "",
                "status": "blocked_by_robots",
                "error": "",
            })
            continue

        try:
            final_url, html = fetch_page(
                requested_url,
                config["user_agent"],
                config["timeout_seconds"],
            )
            parser = PageParser()
            parser.feed(html)
            title, text, links = parser.result()
            records.append({
                "url": final_url,
                "title": title,
                "text": text,
                "status": "ok",
                "error": "",
            })

            for href in links:
                child = canonicalize(urllib.parse.urljoin(final_url, href))
                if allowed_link(child, root_domain, config["same_domain_only"]):
                    queue.append((child, root_domain))
        except (OSError, ValueError, urllib.error.URLError) as exc:
            records.append({
                "url": requested_url,
                "title": "",
                "text": "",
                "status": "error",
                "error": str(exc),
            })

        if queue and config["delay_seconds"]:
            time.sleep(config["delay_seconds"])

    return records


def write_output(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".json":
        path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return
    if path.suffix.lower() == ".csv":
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["url", "title", "text", "status", "error"],
            )
            writer.writeheader()
            writer.writerows(records)
        return
    raise ValueError("output must end in .csv or .json")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        records = crawl(config)
        write_output(args.output, records)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    ok_count = sum(record["status"] == "ok" for record in records)
    print(f"pages={len(records)} ok={ok_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
