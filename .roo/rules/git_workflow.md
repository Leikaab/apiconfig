### Git Workflow

This project follows the Gitflow branching model:

*   **`main`**: Contains stable, production-ready code. Direct commits are prohibited.
*   **`develop`**: The primary integration branch for ongoing development. All feature branches are merged into `develop`.
*   **`feature/*`**: Branches created from `develop` for specific features or tasks.

**Pull Requests (PRs):**

*   All work must be submitted via Pull Requests.
*   PRs should target the `develop` branch.

**Commit Messages:**

*   Commit messages **must** follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format (e.g., `feat: add new login endpoint`, `fix: resolve issue with config loading`, `docs: update README`).

**Commit Verification:**

*   Using `git commit --no-verify` to bypass pre-commit hooks is **strictly prohibited**. All checks must pass before committing.