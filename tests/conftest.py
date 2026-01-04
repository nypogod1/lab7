import pytest


def pytest_configure(config):
    """Настройка pytest"""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test"
    )


def pytest_collection_modifyitems(items):
    """Модификация собранных тестов"""
    for item in items:
        if "test_integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
