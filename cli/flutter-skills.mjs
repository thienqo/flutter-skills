#!/usr/bin/env node

import { run } from "../lib/cli.mjs";

process.exitCode = run(process.argv.slice(2));
