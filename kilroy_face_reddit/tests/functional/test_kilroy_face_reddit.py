"""

Notice we don't follow the same test structure as in unit tests.
That's because functional tests should test the code from "outside".
So we don't need to follow any hierarchy.

"""

import pytest
from kilroy_face_reddit.__main__ import cli
from typer.testing import CliRunner


class TestKilroyFaceReddit:

    # pytest fixture, passed to all methods by argument
    @pytest.fixture(autouse=True, scope="class")
    def runner(self):
        return CliRunner()

    def test_kilroy_face_reddit_prints_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert "Usage" in result.output
