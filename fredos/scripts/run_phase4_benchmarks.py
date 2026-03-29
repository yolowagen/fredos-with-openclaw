"""Run Phase 4 reliability benchmarks for FredOS wrappers and retrieval paths."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.base import Base, get_db
from app.main import app


TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(bind=TEST_ENGINE)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


def benchmark() -> dict:
    importlib.import_module("app.models")

    Base.metadata.create_all(bind=TEST_ENGINE)
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    results = {
        "retrieval_checks": [],
        "wrapper_checks": [],
        "metrics": {},
    }

    project = client.post("/api/projects", json={"name": "Benchmark Project"}).json()
    task = client.post(
        "/api/tasks",
        json={"project_id": project["id"], "title": "Benchmark Task"},
    ).json()

    retrieval_cases = [
        ("mode_a_project_overview", f"/api/retrieve/project-overview/{project['id']}", "A"),
        ("mode_b_task_support", f"/api/retrieve/task-support/{task['id']}", "B"),
        ("mode_c_research", f"/api/retrieve/research/{project['id']}", "C"),
        ("mode_d_personal_strategy", "/api/retrieve/personal-strategy", "D"),
    ]

    for name, url, expected_mode in retrieval_cases:
        response = client.get(url)
        passed = response.status_code == 200 and response.json()["mode"] == expected_mode
        results["retrieval_checks"].append(
            {"name": name, "url": url, "passed": passed, "status_code": response.status_code}
        )

    wrapper_cases = [
        (
            "write_structured",
            client.post,
            "/api/fredos/write-structured",
            {
                "record_type": "knowledge",
                "project_id": project["id"],
                "title": "Benchmark Knowledge",
                "author_agent": "operator-agent",
                "rationale": "Benchmarking structured writes",
                "summary": "Structured write benchmark passed.",
            },
        ),
        (
            "update_task",
            client.patch,
            f"/api/fredos/tasks/{task['id']}",
            {
                "author_agent": "operator-agent",
                "rationale": "Benchmarking task updates",
                "status": "in_progress",
            },
        ),
    ]

    left_memory = client.post(
        "/api/memory/items",
        json={"memory_level": "L2", "project_id": project["id"], "content": "left"},
    ).json()
    right_memory = client.post(
        "/api/memory/items",
        json={"memory_level": "L2", "project_id": project["id"], "content": "right"},
    ).json()
    wrapper_cases.append(
        (
            "link_entities",
            client.post,
            "/api/fredos/link-entities",
            {
                "author_agent": "memory-manager-agent",
                "relation_type": "related",
                "from_memory_id": left_memory["id"],
                "to_memory_id": right_memory["id"],
                "project_id": project["id"],
                "rationale": "Benchmarking entity links",
            },
        )
    )

    for name, method, url, payload in wrapper_cases:
        response = method(url, json=payload)
        passed = response.status_code == 200
        results["wrapper_checks"].append(
            {"name": name, "url": url, "passed": passed, "status_code": response.status_code}
        )

    retrieval_passes = sum(check["passed"] for check in results["retrieval_checks"])
    wrapper_passes = sum(check["passed"] for check in results["wrapper_checks"])
    total_checks = len(results["retrieval_checks"]) + len(results["wrapper_checks"])

    results["metrics"] = {
        "retrieval_success_rate": retrieval_passes / len(results["retrieval_checks"]),
        "wrapper_success_rate": wrapper_passes / len(results["wrapper_checks"]),
        "overall_success_rate": (retrieval_passes + wrapper_passes) / total_checks,
    }

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=TEST_ENGINE)
    return results


def main() -> None:
    output = benchmark()
    out_path = Path(__file__).resolve().parents[1] / "fredos_data" / "exports" / "phase4_benchmark_results.json"
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))
    print(f"saved={out_path}")


if __name__ == "__main__":
    main()
