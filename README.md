# 🌳 Yggdrasil Labs Engineering

# 🛡 OVERWATCH Sentinel

## Rapid API Operational Readiness

> **Operational Readiness Verification. Immediate Engineering Confidence.**

![Sentinel](assets/sentinel-hero-banner.png)

Sentinel is a lightweight desktop API smoke-testing utility. Give it a target API, run a small readiness suite, and get clear PASS / FAIL results with useful failure information.

Sentinel is designed for the fast development and QA feedback loop:

```text
Make a change
    |
    v
Run Sentinel
    |
    v
Review results
    |
    v
Make another change
    |
    v
Run again and compare
```

> **Philosophy:** Observe. Validate. Report.

---

## v0.1.0 MVP

The Sentinel MVP demonstrates one workflow well:

```text
API Target
   |
   v
Validate Configuration
   |
   v
Connectivity Check
   |
   +--> Optional Authentication Check
   |
   v
Endpoint Check
   |
   v
PASS / FAIL Results
   |
   v
Immediate Operational Confidence
```

### Implemented

- PySide6 desktop GUI
- Target/base URL input
- Configurable endpoint path
- Connectivity validation against the target base URL
- Optional username/password authentication through `/login`
- Bearer-token endpoint request when authentication returns a token
- Endpoint availability/status check
- PASS / FAIL status cards
- Human-readable execution results and response timing
- Graceful handling of unreachable or malformed targets
- Early stop after critical connectivity or authentication failure
- Timestamped in-session run history
- Previous results remain visible for quick comparison between runs
- Clear Results control for starting a fresh visible session
- Results panel automatically scrolls to the newest output
- Wrapped results output without unnecessary horizontal scrolling
- Repeatable automated tests using a local HTTP fixture
- Positive and negative demo paths

### Not implemented in v0.1.0

These remain future enhancements and should not be interpreted as current capabilities:

- Persistent run history across application restarts
- Saved test sessions
- Run-to-run diff analysis
- JSON payload/schema validation
- Configurable endpoint suites
- Configurable authentication profiles or OAuth
- HTML report export
- Console report export
- CI exit codes
- API contract validation
- Security-oriented checks
- HELHEIM Proving Grounds integration
- YLE agent integration

---

## Architecture

Sentinel keeps desktop presentation separate from smoke-test behavior:

```text
PySide6 GUI
    |
    v
Configuration
    |
    v
SmokeEngine
    |
    +--> ConnectivityCheck
    +--> AuthenticationCheck (optional)
    +--> EndpointCheck
    |
    v
CheckResult / SmokeResult
    |
    v
Results Presentation
```

The GUI coordinates user interaction and presentation. It does not implement the HTTP smoke-test business logic.

Session history is also presentation-only. Timestamping, retaining visible run output, scrolling, and clearing results do not alter `SmokeEngine` behavior.

---

## Requirements

- Python 3.12+
- PySide6
- requests
- PyYAML
- Jinja2

For development/testing:

- pytest

---

## Install

From the repository root:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest
```

---

## Run Sentinel

From the repository root:

```powershell
python main.py
```

or:

```powershell
python -m sentinel.app
```

The application accepts:

- **Target URL** — API base URL, such as `http://127.0.0.1:8765`
- **Endpoint Path** — endpoint to validate, such as `/users`
- **Username / Password** — optional; leave both blank to skip authentication

If credentials are supplied, Sentinel currently authenticates with `POST /login` using:

```json
{
  "username": "...",
  "password": "..."
}
```

A successful authentication response may return a JSON `token`, which Sentinel sends to the endpoint check as a Bearer token.

---

## Session History

Sentinel preserves smoke-test output for the current application session so a developer or QA engineer can compare successive runs while making changes.

Each run receives a local system timestamp:

```text
Run Executed: 2026-09-20 09:08:56 AM
PASS

Run Executed: 2026-09-20 09:09:10 AM
FAIL - HTTP 404

Run Executed: 2026-09-20 09:09:23 AM
PASS
```

This supports a lightweight feedback workflow:

```text
Change API
   |
   v
Run smoke test
   |
   v
Inspect result
   |
   v
Change API
   |
   v
Run again
   |
   v
Compare with previous run
```

The **Clear Results** button clears only the visible session history. It does not change Sentinel configuration or engine behavior.

Run history is currently in-memory only and is not preserved after Sentinel exits.

---

## Repeatable Local Demonstration

Sentinel includes a small local API specifically so the MVP can be demonstrated without depending on a public service or internet access.

### 1. Start the demo API

Open one terminal from the repository root:

```powershell
python demo\demo_api.py
```

The demo target runs at:

```text
http://127.0.0.1:8765
```

Keep this terminal running while demonstrating Sentinel.

### 2. Start Sentinel

Open a second terminal:

```powershell
python main.py
```

### Positive demo — no authentication

Enter:

```text
Target URL:    http://127.0.0.1:8765
Endpoint Path: /users
Username:      [blank]
Password:      [blank]
```

Expected outcome:

- Connectivity: PASS
- Authentication: Not Configured
- Endpoint: PASS
- Overall: PASS

### Positive demo — authentication configured

Enter:

```text
Target URL:    http://127.0.0.1:8765
Endpoint Path: /users
Username:      demo
Password:      sentinel
```

Expected outcome:

- Connectivity: PASS
- Authentication: PASS
- Endpoint: PASS
- Overall: PASS

### Negative demo — missing endpoint

Enter:

```text
Target URL:    http://127.0.0.1:8765
Endpoint Path: /missing
Username:      [blank]
Password:      [blank]
```

Expected outcome:

- Connectivity: PASS
- Authentication: Not Configured
- Endpoint: FAIL
- HTTP status: 404
- Overall: FAIL
- Sentinel remains running

### Negative demo — failed authentication

Enter:

```text
Target URL:    http://127.0.0.1:8765
Endpoint Path: /users
Username:      demo
Password:      wrong
```

Expected outcome:

- Connectivity: PASS
- Authentication: FAIL
- HTTP status: 401
- Endpoint check is not executed
- Overall: FAIL

### Negative demo — target unavailable

Stop the local demo API, then execute Sentinel against:

```text
http://127.0.0.1:8765
```

Expected outcome:

- Connectivity: FAIL
- Useful connection-refused message
- Remaining dependent checks are not executed
- Overall: FAIL
- Sentinel remains running

---

## Suggested Demonstration Sequence

For a short portfolio or interview demonstration:

```text
1. /users with no credentials          -> PASS
2. /missing                            -> FAIL (404)
3. /users                              -> PASS
4. demo / wrong password               -> FAIL (401)
5. demo / sentinel                     -> PASS
```

Because Sentinel retains timestamped results, the sequence remains visible in the Results panel and demonstrates both positive and negative QA thinking in one session.

---

## Automated Tests

Run from the repository root:

```powershell
python -m pytest
```

Using `python -m pytest` is recommended on Windows because it ensures pytest runs with the same Python interpreter/environment being used by Sentinel.

The current MVP test suite contains **11 automated tests** covering:

- reachable target
- malformed target
- successful endpoint request
- missing endpoint
- successful authentication
- failed authentication
- optional authentication
- incomplete authentication configuration
- connectivity short-circuit behavior
- successful complete smoke execution
- failed complete smoke execution

Verified MVP baseline:

```text
11 passed
```

---

## Verified v0.1.0 Behavior

The MVP has been manually exercised on Windows with the bundled local demo API.

Verified paths:

```text
Successful unauthenticated run   PASS
Successful authenticated run     PASS
Unreachable target               PASS (expected failure handled cleanly)
Missing endpoint / HTTP 404       PASS (expected failure handled cleanly)
Invalid credentials / HTTP 401    PASS (expected failure handled cleanly)
Timestamped session history       PASS
Clear Results                     PASS
Automated test suite              11/11 PASS
```

Here, `PASS (expected failure handled cleanly)` means Sentinel correctly detected and reported the negative condition without crashing.

---

## Repository Structure

```text
overwatch-sentinel/
├── assets/
├── demo/
│   └── demo_api.py
├── docs/
├── src/
│   └── sentinel/
│       ├── checks/
│       ├── engine/
│       ├── gui/
│       ├── models/
│       └── widgets/
├── tests/
├── main.py
├── README.md
├── PRODUCT.md
├── CHANGELOG.md
└── pyproject.toml
```

---

## Windows Packaging

Windows packaging intentionally comes after core MVP verification.

The intended deliverable is:

```text
Sentinel.exe
    |
    v
Existing PySide6 GUI
    |
    v
Existing SmokeEngine
```

Packaging must remain a thin deployment layer. Smoke-test behavior will not be duplicated inside packaging-specific code.

A PyInstaller build is the planned next deployment step now that:

- core behavior is working
- positive and negative GUI paths are verified
- session-history behavior is verified
- the automated test suite is green

---

## Future Direction

Sentinel may later grow into a richer API operational-readiness utility while preserving the same small-core architecture.

Potential future capabilities include:

- persistent test sessions
- exportable run history
- run-to-run comparison
- JSON payload validation
- configurable endpoint suites
- authentication profiles
- HTML reports
- console reports
- CI exit codes
- API contract checks
- security-oriented validation
- HELHEIM Proving Grounds integration
- future YLE agent integration

These are roadmap concepts, not v0.1.0 capabilities.

---

## Engineering Standard

Sentinel follows the Yggdrasil Labs Engineering principle:

> **Wisdom Before Action.**

And the product standard:

> **“This made my job easier.”**

Sentinel is not intended to replace a full API testing framework or regression suite. Its job is to answer a smaller question quickly and clearly:

> **Is this API operationally ready for deeper testing?**

---

## License

MIT License. See [LICENSE](LICENSE).
