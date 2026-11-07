# Specialist coordination

Select specialists by the behavior the slice reaches, using their descriptions and boundaries. Load only the relevant guidance. Extracting a reusable package brings in package development even without native code; reusing an existing dependency does not. The same agent can apply several specialists sequentially.

## Establish shared ownership

Keep one implementation owner for each shared contract and state transition, following the existing architecture. For example, the repository can own wire-to-domain mapping, the state owner submission and recovery, and the UI localized presentation. Do not let independent proposals redefine the same field or duplicate a state owner.

Before a dependent edit, carry a compact handoff in the current task context:

- Inputs: inspected contract fields, types, units, nullability, lifecycle, and existing package/SDK constraints. Identify exact missing inspection instead of inventing signatures or server behavior.
- Scope: the owning code path, shared consumers, authorized changes, and outputs that must remain compatible.
- Outputs: the agreed interface and success, pending, error, retry, and cancellation outcomes that the next owner consumes, where relevant.
- Acceptance: concrete assertions for those outputs, the checks already run, and the checks still needed at the receiving boundary.

This can be a short note; do not create a separate document or ceremony for every specialist. Establish shared contracts before dependent implementation. Independent test preparation or inspection can proceed in parallel with resolving a contract.

## Resolve proposals and blockers

Resolve conflicting proposals against the user's scope and inspected project contracts before applying them. A display requirement does not authorize changing a shared wire/domain type, and a specialist's preferred library does not authorize migration. Keep integer monetary units in their existing contract and format at the display boundary when that is the established design. When a material product decision remains genuinely unresolved, use the preflight understanding gate.

Separate unavailable external verification from implementation dependencies. Missing staging credentials or a device need not stop local implementation and fake-transport/unit/widget checks when contracts are established. Continue that independent work and record the exact live-backend and target-runtime boundaries as blocked. If an unavailable contract affects correctness, defer only the dependent edits rather than guessing.

Carry the resulting contracts and acceptance checks into the bounded implementation review. Report local, fixture-backed evidence separately from blocked runtime checks; do not call the feature fully verified while required evidence is missing.
