import pytest

from sa_konsepy.concepts.suicide_attempt import SuicideAttempt, RUN_REGEXES_FUNC


@pytest.mark.parametrize('text', [
    'attempt to leap into traffic',
    'attempted to leap into traffic',
    'after a suicide attempt',
    'suicide attempt was unsuccessful',
    'jumped off a bridge',
    'used a knife to kill herself',
    'shot himself',
    'attempted to commit suicide',
    'attempt to leap into traffic',
    'attempted to leap into traffic',
    'after a suicide attempt',
    'suicide attempt was unsuccessful',
    'suicide attempt not successful',
    'suicidal behavior due to stress',
    'suicidal behaviour due to stress',
    'trying to kill herself',
    'tried to kill himself',
    'attempt to kill herself',
    'attempted to kill himself',
    'attempt to commit suicide',
    'attempted suicide',
    'failed to hang herself',
    'jumped off a bridge',
    'jumping from a building',
    'used a knife to kill herself',
    'took a gun and shot himself',
    'shot herself',
    'stabbed himself',
    'ran into traffic',
    'walked into a moving car',
])
def test_run_regexes_yes(text):
    results = set(RUN_REGEXES_FUNC(text))
    assert SuicideAttempt.YES in results


@pytest.mark.parametrize('text', [
    'denies suicide attempt in teens',
    'denied suicide attempts in college',
    'no history of suicide attempt',
    'not hx of suicide attempt',
    'nor previous suicide attempt',
    'or past suicide attempt',
    'denies hx of suicide attempt: no',
    'denies prior suicide attempt during childhood',
    'denies past self harm behaviour in high school',
    'denied deliberate self harm in the past',
    'no suicide attempt',
    'suicide attempt: never',
])
def test_run_regexes_no(text):
    results = set(RUN_REGEXES_FUNC(text))
    assert SuicideAttempt.NO in results


@pytest.mark.parametrize('text', [
    'family history of suicide attempt',
    'family hx of suicide attempts',
    'family past suicide attempt',
    'brother self harm behaviour',
    'family history of attempted suicide',
    'family history: suicide attempt',
    'family hx of deliberate self harm',
    'mother prior attempted to kill herself',
    'aunt has history of suicide attempt in teens',
    'son attempted to commit suicide during college',
    'uncle attempted to commit suicide',
],
                         )
def test_run_regexes_family(text):
    results = set(RUN_REGEXES_FUNC(text))
    assert SuicideAttempt.FAMILY in results


@pytest.mark.parametrize('text', [
    'suicide attempt in teens',
    'suicide attempt in college',
    'suicide attempts in childhood',
    'suicide attempt on 3/2019',
    'suicide attempt during the past year',
    'self harm behaviour in middle school',
    'attempted suicide at age 17',
    'attempted to kill herself as a junior in high school',
    'history of suicide attempt: yes',
    'hx of self harm: 2 times',
    'past suicide attempt during high school',
    'attempted suicide in college',
])
def test_run_regexes_history(text):
    results = set(RUN_REGEXES_FUNC(text))
    assert SuicideAttempt.HISTORY in results


@pytest.mark.parametrize('text', [
    'problem list: hx of suicide attempt',
    'problem list hx of suicide attempt',
    'problem list: prior suicide attempts',
    'PMH: hx of deliberate self harm',
    'Medical History: deliberate self harm',
])
def test_run_regexes_problem_list(text):
    results = set(RUN_REGEXES_FUNC(text))
    assert SuicideAttempt.PROBLEM_LIST in results


@pytest.mark.parametrize('text', [
    'no suicide attempt',
    'suicide attempt: never',
])
def test_suppress_overlaps_is_working(text):
    results = list(RUN_REGEXES_FUNC(text))
    assert len(results) == 1
    assert results[0] == SuicideAttempt.NO
