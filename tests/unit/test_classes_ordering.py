from __future__ import annotations

from click.testing import CliRunner
from pydantic_settings import BaseSettings
from pytest_mock import MockerFixture

from tests.fixtures.valid_settings import EmptySettings, MultipleSettings, PossibleValuesSettings
from tests.helpers import run_app_with_settings

_TEMPLATE = """
{% for cls, fields in classes.items() %}
{{ cls.__name__ }}
{%- endfor %}
""".strip()


class TestClassesOrdering:
    @staticmethod
    def should_be_stable(runner: CliRunner, mocker: MockerFixture):
        classes: list[type[BaseSettings]] = [EmptySettings, MultipleSettings, PossibleValuesSettings]
        expected_cls_names = [_.__name__.lower() for _ in classes]

        for i in range(1, 11):
            result = run_app_with_settings(mocker, runner, classes, template=_TEMPLATE)
            assert result.strip().split("\n") == expected_cls_names, f"Unstable ordering observed at iteration {i}/10"
