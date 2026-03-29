"""Governance tests for baseline FredOS agent profiles."""

from __future__ import annotations

from pathlib import Path


CONFIG_DIR = Path(__file__).resolve().parents[1] / "app" / "agents" / "config"


def _load_text(name: str) -> str:
    return (CONFIG_DIR / name).read_text(encoding="utf-8")


def _tool_names(config_text: str) -> list[str]:
    names: list[str] = []
    for line in config_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- name:"):
            names.append(stripped.split(":", 1)[1].strip())
    return names


def test_all_baseline_profiles_exist():
    expected = {
        "router_config.yaml",
        "research_config.yaml",
        "operator_config.yaml",
        "memory_manager_config.yaml",
        "executor_config.yaml",
        "reviewer_config.yaml",
    }
    existing = {path.name for path in CONFIG_DIR.glob("*_config.yaml")}
    assert expected.issubset(existing)


def test_only_executor_has_exec():
    profiles_with_exec = []
    for path in CONFIG_DIR.glob("*_config.yaml"):
        tools = _tool_names(path.read_text(encoding="utf-8"))
        if "exec" in tools:
            profiles_with_exec.append(path.name)
    assert profiles_with_exec == ["executor_config.yaml"]


def test_read_only_roles_have_no_write_tools():
    read_only_profiles = {
        "router_config.yaml",
        "research_config.yaml",
        "reviewer_config.yaml",
    }
    forbidden_fragments = ("create_", "update_", "consolidate_", "add_session_summary")

    for name in read_only_profiles:
        tools = _tool_names(_load_text(name))
        assert not any(
            any(fragment in tool_name for fragment in forbidden_fragments)
            for tool_name in tools
        ), name


def test_write_capable_roles_require_retrieval_first_flag():
    write_capable_profiles = {
        "operator_config.yaml",
        "memory_manager_config.yaml",
    }
    for name in write_capable_profiles:
        text = _load_text(name)
        assert "requires_retrieval_before_reasoning: true" in text
        assert "can_write_fredos: true" in text


def test_all_profiles_use_openclaw_aligned_runtime_sections():
    required_sections = [
        "runtime:",
        "retrieval_policy:",
        "output_contract:",
        "escalation:",
    ]
    for path in CONFIG_DIR.glob("*_config.yaml"):
        if path.name in {"chief_of_staff_config.yaml", "memory_curator_config.yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        for section in required_sections:
            assert section in text, f"{path.name} missing {section}"


def test_runtime_role_specific_constraints():
    router = _load_text("router_config.yaml")
    executor = _load_text("executor_config.yaml")
    operator = _load_text("operator_config.yaml")

    assert "session_profile: controller-session" in router
    assert "can_coordinate_sessions: true" in router

    assert "session_profile: exec-enabled-session" in executor
    assert "can_use_exec: true" in executor
    assert "requires_review_before_exec: false" in executor

    assert "fredos_write_structured" in operator
    assert "fredos_update_task" in operator
