import asyncio

import pytest

from src.blueprints.orchestrator import GitHubProvider


@pytest.mark.unit
def test_github_provider_dry_run_repository_creation():
    provider = GitHubProvider(dry_run=True)

    class DummyRepo:
        name = "example"
        visibility = "private"
        features = ["issues", "projects"]
        protection = {"enabled": True}

    async def run():
        return await provider.create_repository("acme", DummyRepo)

    result = asyncio.get_event_loop().run_until_complete(run())
    assert result is True


