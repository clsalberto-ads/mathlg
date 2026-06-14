"""Testes dos exportadores CSV e JSON."""

from __future__ import annotations

import csv
import json
import os
import tempfile
import pytest

from mathlg.export.csv_exporter import export_csv
from mathlg.export.json_exporter import export_json


class TestCsvExporter:
    """Testes do exportador CSV."""

    def test_export_basic(self) -> None:
        data = [
            {"expression": "2 + 2", "result": "4", "lang": "pt-BR"},
            {"expression": "sqrt 144", "result": "12.0", "lang": "pt-BR"},
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.close()  # Fecha para poder reabrir
            try:
                export_csv(data, f.name)

                with open(f.name, newline="", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)
                    rows = list(reader)
                    assert len(rows) == 2
                    assert rows[0]["expression"] == "2 + 2"
                    assert rows[0]["result"] == "4"
                    assert rows[1]["expression"] == "sqrt 144"
            finally:
                os.unlink(f.name)

    def test_export_empty(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.close()
            try:
                export_csv([], f.name)
                with open(f.name, "r", encoding="utf-8") as result:
                    content = result.read()
                assert content == ""  # CSV vazio
            finally:
                os.unlink(f.name)


class TestJsonExporter:
    """Testes do exportador JSON."""

    def test_export_basic(self) -> None:
        data = [
            {"expression": "2 + 2", "result": "4", "lang": "pt-BR"},
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.close()
            try:
                export_json(data, f.name)

                with open(f.name, "r", encoding="utf-8") as jsonfile:
                    content = json.load(jsonfile)
                    assert "metadata" in content
                    assert "results" in content
                    assert content["metadata"]["count"] == 1
                    assert content["results"][0]["expression"] == "2 + 2"
                    assert "timestamp" in content["metadata"]
            finally:
                os.unlink(f.name)

    def test_export_empty(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.close()
            try:
                export_json([], f.name)
                with open(f.name, "r", encoding="utf-8") as result:
                    content = json.load(result)
                    assert content["metadata"]["count"] == 0
                    assert content["results"] == []
            finally:
                os.unlink(f.name)
