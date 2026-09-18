# Architectural Decision Record

## 1. State Contention

ParaBank is a shared, stateful public sandbox. Unique usernames prevent user-data collisions,
but they do not protect against global operations such as `cleanDB`.

Decision:
- Generate unique users/resources for every run.
- Keep global reset tests serial.
- Use a CI concurrency group for reset-bearing jobs.
- Prefer an isolated ParaBank instance if true parallel execution is required.
- Do not claim a public shared sandbox can be safely isolated from another team's global reset.

## 2. Currency Handling

Python's binary floating-point values are not used for financial assertions.
Currency strings are parsed with `Decimal`, normalized to two decimal places, and converted
to integer cents before aggregation and equality assertions.

## 3. API vs UI Boundary

API:
- Environment/setup operations.
- Database/admin setup.
- Fast server-side validation.
- Pure API parity test.

UI:
- User-visible business journeys required by the assignment.
- Registration, account creation, transfers, transaction search, loan request, and visible assertions.

The goal is to keep UI tests focused on user behavior while using APIs for deterministic setup
and server-side verification.
