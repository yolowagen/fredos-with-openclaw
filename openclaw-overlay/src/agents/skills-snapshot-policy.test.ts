import { describe, expect, it } from "vitest";
import { shouldRefreshSkillsSnapshot } from "./skills-snapshot-policy.js";

describe("shouldRefreshSkillsSnapshot", () => {
  it("refreshes when creating a new session", () => {
    expect(
      shouldRefreshSkillsSnapshot({
        isNewSession: true,
        currentVersion: 10,
      }),
    ).toBe(true);
  });

  it("refreshes when the snapshot is missing", () => {
    expect(
      shouldRefreshSkillsSnapshot({
        isNewSession: false,
        currentVersion: 10,
      }),
    ).toBe(true);
  });

  it("refreshes when the snapshot version changes", () => {
    expect(
      shouldRefreshSkillsSnapshot({
        isNewSession: false,
        currentVersion: 10,
        snapshot: {
          prompt: "cached",
          skills: [],
          version: 9,
        },
      }),
    ).toBe(true);
  });

  it("refreshes when the skill filter changes", () => {
    expect(
      shouldRefreshSkillsSnapshot({
        isNewSession: false,
        currentVersion: 10,
        skillFilter: ["fredos", "router"],
        snapshot: {
          prompt: "cached",
          skills: [],
          version: 10,
          skillFilter: ["fredos"],
        },
      }),
    ).toBe(true);
  });

  it("does not refresh when version and filter still match", () => {
    expect(
      shouldRefreshSkillsSnapshot({
        isNewSession: false,
        currentVersion: 10,
        skillFilter: ["router", "fredos"],
        snapshot: {
          prompt: "cached",
          skills: [],
          version: 10,
          skillFilter: ["fredos", "router"],
        },
      }),
    ).toBe(false);
  });
});
