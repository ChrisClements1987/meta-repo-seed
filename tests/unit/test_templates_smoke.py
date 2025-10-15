import pytest

from src.templates.generator import ProductTemplateRegistry


@pytest.mark.unit
def test_list_templates_non_empty():
    names = ProductTemplateRegistry.list_templates()
    assert isinstance(names, list)
    assert len(names) > 0


