---
number: 78
title: "Implement RedactingFormatter with integrated redaction logic"
state: OPEN
author: Leikaab
created_at: 2025-04-20T02:51:17Z
updated_at: 2025-04-20T02:51:17Z
closed_at: null
url: https://github.com/Leikaab/apiconfig/issues/78
---

# Implement RedactingFormatter with integrated redaction logic

## Module
`apiconfig/utils/logging/formatters.py`

## Category
Feature/Enhancement

## Problem
The `RedactingFormatter` class is currently a placeholder and does not perform any redaction. This means that if it is used as the default formatter, sensitive data (such as secrets, tokens, or PII) may be exposed in logs.

## Impact
- Potential leakage of secrets or PII in logs.
- Users may assume logs are safe when using RedactingFormatter, but they are not.

## Scenario
- Using `RedactingFormatter` as a default formatter does not guarantee redaction of sensitive information.
- Redaction logic exists in `apiconfig/utils/redaction/` (body.py, headers.py), but is not integrated with the formatter.

## Notes
- Implement `RedactingFormatter` to integrate with the redaction utilities in `apiconfig/utils/redaction/`.
- Ensure all log output is properly redacted before being emitted.
- Add unit and integration tests to verify redaction is applied.
- Update documentation to clarify the formatter's guarantees and usage.
---

## Implementation Plan

**Design Principles:**
- **SRP:** The formatter will only handle formatting and redaction, not filtering or log context injection.
- **DRY:** All redaction logic will delegate to the existing utilities in `apiconfig/utils/redaction/body.py` and `apiconfig/utils/redaction/headers.py`. No regex or redaction logic will be duplicated.
- **Consistency:** The formatter will use the `REDACTED_VALUE` constant for all redacted output.

**Steps:**
1. **Formatter Implementation:**
   - Implement `RedactingFormatter.format(self, record)` to:
     - Apply redaction to the log message using `redact_body` for structured data (JSON, dict, form-encoded).
     - If the log record contains HTTP headers (as a dict), use `redact_headers` to redact them before formatting.
     - Allow configuration of sensitive key/value patterns via the formatter's constructor, defaulting to the project's standard patterns.
     - Ensure that if the message is a plain string, only obvious secrets (e.g., matching the sensitive value pattern) are redacted.
   - Do not duplicate any redaction logic—always call the utility functions.

2. **Testing:**
   - Add unit tests for `RedactingFormatter` covering:
     - JSON, dict, and form-encoded messages with secrets.
     - Log records with HTTP headers containing secrets.
     - Plain string messages with embedded secrets.
     - Edge cases: binary data, unparsable input, empty messages.
   - Add integration tests to verify that when used in a real logger, all output is redacted as expected.

3. **Documentation:**
   - Update the formatter's docstring to clearly state its guarantees and limitations.
   - Update user documentation to explain how to use the formatter, what is and isn't redacted, and how to configure patterns.

4. **Quality:**
   - Ensure 100% test coverage for the new code.
   - Follow project code style and type hinting conventions.
   - Use the `REDACTED_VALUE` constant for all redacted output.

---