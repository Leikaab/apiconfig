# Building the documentation

The documentation is generated with [Sphinx](https://www.sphinx-doc.org/).
Ensure development dependencies are installed with Poetry and then run:

```bash
poetry install --with dev
cd docs
make html
```

The HTML output will be available under `docs/build/html/index.html`.
