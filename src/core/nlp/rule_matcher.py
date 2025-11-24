from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

import yaml

from src.config.settings import get_settings
from src.core.logging.config import get_logger
from src.core.nlp.types import RuleMatch


class RuleMatcher:
    """Loads YAML/JSON rules and performs keyword or regex matching."""

    def __init__(self, rules_path: str | None = None) -> None:
        settings = get_settings()
        self.rules_path = Path(rules_path or settings.rules_path).resolve()
        self._rules: list[dict[str, Any]] = []
        self._last_loaded_at: float = 0.0
        self._fingerprint: dict[str, float] = {}
        self.logger = get_logger(__name__)
        self.reload()

    def reload(self) -> None:
        self._rules = []
        self._fingerprint = {}
        if not self.rules_path.exists():
            self.logger.warning("rule_matcher.no_rules_path", path=str(self.rules_path))
            return

        for file in self.rules_path.glob("**/*"):
            if file.suffix.lower() not in {".json", ".yaml", ".yml"}:
                continue
            with file.open("r", encoding="utf-8") as fh:
                data = json.load(fh) if file.suffix.lower() == ".json" else yaml.safe_load(fh)
            for rule in data.get("rules", []):
                rule["source_file"] = str(file)
                self._rules.append(rule)
            self._fingerprint[str(file)] = file.stat().st_mtime

        self._last_loaded_at = time.time()
        self.logger.info(
            "rule_matcher.loaded",
            count=len(self._rules),
            path=str(self.rules_path),
        )

    def reload_if_changed(self) -> None:
        if not self.rules_path.exists():
            return
        for file in self.rules_path.glob("**/*"):
            if file.suffix.lower() not in {".json", ".yaml", ".yml"}:
                continue
            mtime = file.stat().st_mtime
            if self._fingerprint.get(str(file)) != mtime:
                self.reload()
                break

    def match(self, text: str, metadata: dict[str, Any] | None = None) -> list[RuleMatch]:
        self.reload_if_changed()
        metadata = metadata or {}
        matches: list[RuleMatch] = []
        for rule in self._rules:
            evidence: list[str] = []
            for pattern in rule.get("patterns", []):
                ptype = pattern.get("type", "contains")
                value = pattern.get("value", "")
                if not value:
                    continue
                if ptype == "contains" and value.lower() in text.lower():
                    evidence.append(value)
                elif ptype == "regex" and re.search(value, text, flags=re.IGNORECASE):
                    evidence.append(value)
            if evidence:
                matches.append(
                    RuleMatch(
                        rule_id=rule["id"],
                        description=rule.get("description", ""),
                        action=rule.get("action", "review"),
                        severity=rule.get("severity", "medium"),
                        tags=rule.get("tags", []),
                        evidence=evidence,
                        metadata={**metadata, "source_file": rule.get("source_file")},
                    )
                )
        return matches
