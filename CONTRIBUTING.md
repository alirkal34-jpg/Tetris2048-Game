# Contributing to T2048 Nexus

Thanks for your interest in improving this project! 🎉

## How to Contribute

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/short-description
   ```
3. Make focused, reviewable commits.
4. Run checks before opening a PR:
   ```bash
   ruff check .
   python -m py_compile *.py
   ```
5. Open a Pull Request with a clear summary and testing notes.

## Code Style

- Follow existing project structure and naming.
- Keep game logic changes isolated and minimal.
- Ensure new/updated docs are clear and bilingual where relevant.

## Pull Request Checklist

- [ ] I tested my changes locally.
- [ ] I ran lint/syntax checks.
- [ ] I updated documentation if needed.
- [ ] My changes are backward compatible.
