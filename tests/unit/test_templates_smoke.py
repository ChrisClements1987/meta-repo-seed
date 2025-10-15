import pytest

from src.templates.generator import TemplateRegistry


@pytest.mark.unit
def test_list_templates_non_empty():
    names = TemplateRegistry.list_templates()
    assert isinstance(names, list)
    assert len(names) > 0


