from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.config.settings import get_settings
from src.core.logging.config import get_logger


class ModelRegistryError(RuntimeError):
    pass


class ModelRegistry:
    """Loads lightweight manifest metadata for demo models."""

    def __init__(self, base_path: str | None = None) -> None:
        settings = get_settings()
        self.base_path = Path(base_path or settings.model_registry_path).resolve()
        self._cache: dict[str, dict[str, Any]] = {}
        self._logger = get_logger(__name__)

    def _manifest_path(self, model_name: str, version: str) -> Path:
        return self.base_path / model_name / version / "manifest.json"

    def get_manifest(
        self,
        model_name: str,
        version: str = "1.0.0",
        default: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        cache_key = f"{model_name}:{version}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        manifest_path = self._manifest_path(model_name, version)
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self._cache[cache_key] = manifest
            self._logger.info(
                "model_registry.loaded",
                model=model_name,
                version=version,
                path=str(manifest_path),
            )
            return manifest

        if default is None:
            raise ModelRegistryError(
                f"Manifest for {model_name}:{version} not found at {manifest_path}"
            )

        self._logger.warning(
            "model_registry.default_manifest",
            model=model_name,
            version=version,
            path=str(manifest_path),
        )
        self._cache[cache_key] = default
        return default


registry = ModelRegistry()
