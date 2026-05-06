import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import type { GraphQLAgentEvent } from "../src";

const testDir = dirname(fileURLToPath(import.meta.url));
const fixturesDir = resolve(testDir, "fixtures");

export function readFixture(name: string): GraphQLAgentEvent[] {
  const content = readFileSync(resolve(fixturesDir, name), "utf-8");

  return content
    .split("\n")
    .filter(Boolean)
    .map((line) => JSON.parse(line) as GraphQLAgentEvent);
}
