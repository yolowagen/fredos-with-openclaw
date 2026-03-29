import type { SessionSkillSnapshot } from "../config/sessions/types.js";
import { matchesSkillFilter } from "./skills/filter.js";

export function shouldRefreshSkillsSnapshot(params: {
  isNewSession: boolean;
  snapshot?: SessionSkillSnapshot;
  currentVersion: number;
  skillFilter?: string[];
}): boolean {
  if (params.isNewSession || !params.snapshot) {
    return true;
  }
  if (params.snapshot.version !== params.currentVersion) {
    return true;
  }
  if (!matchesSkillFilter(params.snapshot.skillFilter, params.skillFilter)) {
    return true;
  }
  return false;
}
