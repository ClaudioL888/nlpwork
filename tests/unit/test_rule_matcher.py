from src.core.nlp.rule_matcher import RuleMatcher


def test_rule_matcher_detects_crisis():
    matcher = RuleMatcher()
    matches = matcher.match("This person said they will kill myself immediately")
    ids = {match.rule_id for match in matches}
    assert "CRISIS_LANGUAGE" in ids
    assert any("kill myself" in ev for match in matches for ev in match.evidence)


def test_rule_matcher_hot_reload(tmp_path):
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    rule_file = rules_dir / "rules.yaml"
    rule_file.write_text(
        """
rules:
  - id: TEST_RULE
    description: temp
    action: review
    severity: low
    tags: [demo]
    patterns:
      - type: contains
        value: foo
""",
        encoding="utf-8",
    )

    matcher = RuleMatcher(rules_path=str(rules_dir))
    assert matcher.match("foo bar")

    # modify file to trigger reload
    rule_file.write_text(
        """
rules:
  - id: TEST_RULE
    description: temp
    action: review
    severity: low
    tags: [demo]
    patterns:
      - type: contains
        value: bar
""",
        encoding="utf-8",
    )
    matches = matcher.match("something bar here")
    assert matches
