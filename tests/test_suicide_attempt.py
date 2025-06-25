import pytest

from sa_konsepy.concepts.suicide_attempt import SuicideAttempt, RUN_REGEXES_FUNC


@pytest.mark.parametrize('text, exp', [
    ('attempt to leap into traffic', SuicideAttempt.YES),  # TODO: put tests here
])
def test_run_regexes(text, exp):
    results = set(RUN_REGEXES_FUNC(text))
    assert exp in results
