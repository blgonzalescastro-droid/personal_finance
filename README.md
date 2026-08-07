# Pytest

## Instalación

```bash
pip install pytest pytest-django pytest-cov faker
```

## Configuración `pytest.ini`

```ini
[pytest]
DJANGO_SETTINGS_MODULE=personal_finance.settings
python_files=tests.py test_*.py *_tests.py
filterwarnings=ignore::DeprecationWarning
```

## Ejecución

```bash -v
```