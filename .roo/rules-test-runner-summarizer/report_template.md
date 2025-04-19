# Grouped Issue Report Template

Group all results by unique issue (error/warning/assertion message or error code + message). For each issue, list all affected tests, functions/methods, and files.

---

**If issues are found:**

```
[<error code or type>] <short message or assertion>
  Tests: <test_name_1>, <test_name_2>, ...
  Functions/Methods: <func_1>, <func_2>, ...
  Locations:
    <filename_1>:<line>[:<col>]
    <filename_2>:<line>[:<col>]
    ...
```
- Omit any section (Tests, Functions/Methods) if not applicable.
- Only include unique, actionable issues.
- If more than 10 unique issues, show the 10 most relevant and add: "...and N more."

---

**If no issues are found, output exactly:**
```
No issues found.