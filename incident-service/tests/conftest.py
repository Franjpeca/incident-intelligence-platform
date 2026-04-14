import os
import pytest

# Este "hook" se ejecuta antes de cargar cualquier test
def pytest_configure(config):
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["ENV"] = "testing"