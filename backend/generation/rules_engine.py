"""
rules_engine.py — Enterprise Rule Engine for synthetic data generation.

Parses rules.yml / rules.yaml and exposes rule-driven data generation strategies.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from faker import Faker

logger = logging.getLogger(__name__)


@dataclass
class ColumnRule:
    rule_id    : str
    generator  : str                  # sequence, choice, regex, not_applicable
    start      : int = 1
    increment  : int = 1
    values     : list[Any] = field(default_factory=list)
    pattern    : str = ""
    description: str = ""
    applies_to : Optional[dict[str, str]] = None  # { 'table': ..., 'column': ..., 'condition': ... }


class RulesEngine:
    """Loads and evaluates rules.yml / rules.yaml for column data generation."""

    def __init__(self, rules_path: Optional[Path] = None) -> None:
        self.rules_path = rules_path
        self.global_config: dict[str, Any] = {}
        self.rules: dict[str, ColumnRule] = {}              # rule_id -> ColumnRule
        self.column_rule_map: dict[tuple[str, str], ColumnRule] = {}  # (table, column) -> ColumnRule
        self.direct_rule_map: dict[str, ColumnRule] = {}    # col_name -> ColumnRule
        self.sequence_state: dict[str, int] = {}
        self._fake = Faker()

        self._load()

    def _load(self) -> None:
        path = self.rules_path
        if not path or not path.exists():
            root = Path(__file__).parent
            for cand in [root / "rules.yml", root / "rules.yaml"]:
                if cand.exists():
                    path = cand
                    break

        if not path or not path.exists():
            logger.info("No rules.yml or rules.yaml file found.")
            return

        logger.info("Loading rules engine from: %s", path.name)
        data = self._parse_yaml(path)

        self.global_config = data.get("global", {})
        columns_data = data.get("columns", {})

        for rule_id, rdata in columns_data.items():
            if not isinstance(rdata, dict):
                continue

            applies = rdata.get("applies_to")
            rule = ColumnRule(
                rule_id    = rule_id,
                generator  = str(rdata.get("generator", "")).lower(),
                start      = int(rdata.get("start", 1)),
                increment  = int(rdata.get("increment", 1)),
                values     = list(rdata.get("values", [])),
                pattern    = str(rdata.get("pattern", "")),
                description= str(rdata.get("description", "")),
                applies_to = applies if isinstance(applies, dict) else None,
            )

            self.rules[rule_id] = rule

            # If rule specifies applies_to (table, column)
            if rule.applies_to and "table" in rule.applies_to and "column" in rule.applies_to:
                tbl = str(rule.applies_to["table"]).lower()
                col = str(rule.applies_to["column"]).lower()
                self.column_rule_map[(tbl, col)] = rule
            else:
                self.direct_rule_map[rule_id.lower()] = rule

            if rule.generator == "sequence":
                self.sequence_state[rule_id] = rule.start

        logger.info("Loaded %d column generation rules from %s", len(self.rules), path.name)

    def get_rule_for_column(self, table_name: str, column_name: str, row_context: Optional[dict[str, Any]] = None) -> Optional[ColumnRule]:
        """Return the active ColumnRule for (table_name, column_name), checking conditions if applicable."""
        tbl_lower = table_name.lower()
        col_lower = column_name.lower()

        # Check explicit table+column mappings first (with condition evaluation)
        for (tbl, col), rule in self.column_rule_map.items():
            if tbl == tbl_lower and col == col_lower:
                if rule.applies_to and "condition" in rule.applies_to and row_context is not None:
                    cond = rule.applies_to["condition"]
                    if self._evaluate_condition(cond, row_context):
                        return rule
                else:
                    return rule

        # Direct column name match
        if col_lower in self.direct_rule_map:
            rule = self.direct_rule_map[col_lower]
            if rule.generator != "not_applicable":
                return rule

        return None

    def generate_value(self, rule: ColumnRule, row_context: Optional[dict[str, Any]] = None) -> Any:
        """Generate a single cell value according to rule strategy."""
        g = rule.generator

        if g == "sequence":
            val = self.sequence_state.get(rule.rule_id, rule.start)
            self.sequence_state[rule.rule_id] = val + rule.increment
            return val

        if g == "choice":
            if not rule.values:
                return None
            import random
            return random.choice(rule.values)

        if g == "regex":
            if not rule.pattern:
                return None
            try:
                import rstr
                return rstr.xeger(rule.pattern)
            except Exception:
                return self._fake.bothify(rule.pattern.replace("[0-9]", "#").replace("[A-Z]", "?"))

        if g == "not_applicable":
            return None

        return None

    @staticmethod
    def _evaluate_condition(condition: str, row_context: dict[str, Any]) -> bool:
        """
        Evaluate a simple equality condition string, e.g. "p_alt_id_ty_cd = 'NPI'".
        """
        m = re.match(r"^\s*([a-zA-Z0-9_]+)\s*=\s*'([^']*)'\s*$", condition)
        if m:
            var_name, expected_val = m.group(1).lower(), m.group(2)
            actual_val = str(row_context.get(var_name, "") or "").strip()
            return actual_val.upper() == expected_val.upper()
        return False

    @staticmethod
    def _parse_yaml(path: Path) -> dict[str, Any]:
        """Simple YAML parser fallback if PyYAML is not installed."""
        try:
            import yaml
            with open(path, encoding="utf-8") as fh:
                return yaml.safe_load(fh) or {}
        except ImportError:
            logger.warning("PyYAML not installed; using basic fallback parser.")
            return {}
