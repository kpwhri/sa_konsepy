"""
This file should not be edited. It is just a template for creating additional templates.

Steps for creating a new category:
1. Copy-paste this file to $PROJECT_PATH/src/$PROJECT_NAME/concepts
2. Name new file something like `concept.py`
3. Fix statements on the relevant lines marked # TODO
4. Copy-paste `test_concept_template` file in tests directory
5. Name new file to something like `test_concept.py`
6. Fix statements on relevant lines marked # TODO
7. Add `ConceptCategory` and `RUN_REGEXES_FUNC` to `run_all.py`
8. (Less important) Add the `run_file_on_concept` function to the `tests/test_run_regex_and_output` file.
"""
import enum
import re

from konsepy.context.negation import check_if_negated, has_prenegation
from konsepy.context.other_subject import check_if_other_subject as _check_if_other_subject
from konsepy.rxsearch import search_all_regex, SKIP


class SuicideAttempt(enum.Enum):
    NO = 0
    YES = 1
    HISTORY = 2
    FAMILY = 3
    CODE = 4
    PROBLEM_LIST = 5  # YES, in problem list
    # SELF_HARM = 6
    YES_ACTION = 2  # YES, but related to an action performed


# account for variables ways to describe HISTORY suicide attempt
suicide_attempt = '(?:{})'.format('|'.join([
    r'suicid\w+\W+attempts?',
    r'deliberate\W*self\W*harm',
    r'self\W*harm\W*behaviou?r',
    r'attempted\W*(?:to\W*commit\W*)?suicide',
    r'attempted\W*(?:\w+\W+){,2}to\W*take\W*(?:his|her)\W*(?:own\W*)?life',
    r'attempted\W*to\W*kill\W*(?:him|her)self',
    r'suicid\w+\W*behaviou?r',
]))

day = r'(?:\d{1,2}\W*)'
year = r'(?:\d{2,4})'
in_period = r'(?:in|on|during)\W*(?:\w+\W+)?(?:{})'.format('|'.join([
    'college', 'university', 'childhood', r'(?:high|middle)\W*school', r'jr\W*high',
    'teens', 'twenties', 'thirties', r'\d0s',
    rf'{day}?January\W*{year}?', rf'{day}?February\W*{year}?', rf'{day}?March\W*{year}?',
    rf'{day}?April\W*{year}?', rf'{day}?May\W*{year}?', rf'{day}?June\W*{year}?',
    rf'{day}?July\W*{year}?', rf'{day}?August\W*{year}?', rf'{day}?September\W*{year}?',
    rf'{day}?October\W*{year}?', rf'{day}?November\W*{year}?', rf'{day}?December\W*{year}?',
    r'(?:20|19)\d{2}', r'\d{1,2}/\d{1,4}(?:\d{2,4})?', 'the past',
]))

approximately = rf'(?:about|approximately|almost|close\W*to|nearly|just\W*about)'
more_than = fr'(?:(?:over|(?:more|less)\s*than|{approximately})\W*)?'
period_ago = rf'{more_than}(?:\d+|(?:a\W*)?few|one|two|three|a|several)\W*(?:month|week|year|day)s?\W*ago'
as_a = r'(?:as a|when a)'
role_label = r'(?:teen(?:ager)?|freshman|jr|junior|senior|sr|sophomore|student)'
role_descript = r'(?:college|(?:high|middle) school)'
role = rf'{role_label}\W*(?:in|at|during)\W*{role_descript}'
role_rev = fr'(?:{role_descript}\W*)?{role_label}'
as_a_role = rf'(?:{as_a}\W*(?:{role}|{role_rev}))'

hx_of = r'(?:past|(?:history|hx)\W*of|previous|prior)'

deny = r'(?:den(?:y|ies|ied))'
family_hx = r'(?:family)'
no = r'(?:no|or|nor|not|never)'
yes = r'(?:yes|briefly|previously)'
number = r'(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen)'
times = rf'(?:{number}\s*(?:x|times?))'
more_than_times = rf'{more_than}{times}'
age = rf'(?:at\W*)?age\W*{number}'
sa_hx_pred = rf'(?:{approximately}\W*)?(?:{in_period}|{period_ago}|{more_than_times}|{as_a_role}|{age})'
the = r'\b(?:an?|the|his|her|their)\b'

# current suicide attempts building on Fernandes et al (2018)
own_life = r'(?:(?:his|her|their)\W*)(?:own\W*)?life'
self = (r'(?:'
        r'(?:(?:him|her|them|their)?\W*)sel(?:f|ves)'
        rf'|{own_life}'
        r')')
attempt = r'(?:attempt|fail|tr[yi])\w*(?:\W*to)?'
in_front_subj = r'\b(?:leap|jump|walk|ran|run)\w{0,4}\b'
in_front_of = r'(?:in\W*front\W*of|out\W*into|into)'
in_front_pred = r'(?:\w+\W+){0,2}(?:motor|bus|train|traffic|car|truck|vehicle)\b\w*'
from_a_bridge = r'(?:(?:off|from)?\W*(?:\w+\W*){0,2}(?:bridge|building))'
weapon = r'(?:gun|firearm|handgun|knife|rifle|weapon)'
suicide_action = r'(?:drown|end|hang|kill|shoot|stab)'
# new type of suicide action
take = r'(?:take)'
commit_suicide = r'(?:commit\W*suicide|(?:deliberate\W*)?self\W*harm|(?:death|died)\W*by\W*suicid)'
used = r'\b(?:used|took)\b'
harmed = r'\b(?:shot|stabbed)\b'

any_sa = rf'(?:{commit_suicide}|{suicide_attempt})'

SA_PAT = re.compile(
    rf'(?:'
    rf'after\W*a\W*suicide\W*attempt'
    rf'|{suicide_attempt}'
    rf'|suicid\w+\W*(?:attempt\W*)?(?:was\W*)?(?:unsuccessful|not\W*successful|due\W*to)'
    rf'|{attempt}\W*{commit_suicide}'
    rf'|{attempt}\W*{suicide_action}\W*{self}'
    rf'|{attempt}\W*{take}\W*{own_life}'
    rf')',
    re.I,
)

vehicle = r'(?:traffic|a\W*(?:moving\W*)?(?:car|truck|train|bus|vehicle))'
intentional = r'(?:intentional(?:ly)?)'
SA_ACTION_PAT = re.compile(
    rf'(?:'
    rf'{in_front_subj}\W*{in_front_of}\W*{in_front_pred}\W*{intentional}'
    rf'|{attempt}\W*{in_front_subj}\W*{in_front_of}\W*{in_front_pred}'
    rf'|(?:ran|jumped|leaped|walked)\W*(?:out\W*)?into\W*traffic'
    rf'|(?:ran|jumped|leaped|walked)\W*in\W*front\W*of\W*{vehicle}'
    rf'|{attempt}\W*(?:r[au]n|jump|leap|walk)\w*\W*in\W*front\W*of\W*{vehicle}'
    rf'|jump\w*\W*{from_a_bridge}'
    rf'|{used}\W*(?:{the}\W*)?{weapon}\W*(?:\w+\W*){{0,3}}{self}'
    rf'|{harmed}\W*{self}'
    rf')',
    re.I,
)


def check_if_other_subject(m, precontext, postcontext, text, window, **kwargs):
    if _check_if_other_subject(m, precontext, postcontext, text, window):
        return SuicideAttempt.FAMILY
    if has_prenegation(precontext, re.compile('animal|deer|cat|dog|bunny|rabbit|bird', re.I)):
        return SKIP


def check_if_colon_before(m, precontext, **kwargs):
    if precontext.strip().endswith(':'):
        return SKIP


def check_if_in_problem_list(m, text, **kwargs):
    prev_match = None
    for problist_match in re.finditer(r'(?:(?:PMH|Medical History):|problem list:?)', text, re.I):
        if problist_match.start() > m.end():  # occurs after current match
            break
        prev_match = problist_match
    if prev_match:
        target_text = text[prev_match.end():m.start()].lower()
        for skipper in [':', 'medications']:
            if skipper in target_text:  # found section in between
                return None
        return SuicideAttempt.PROBLEM_LIST
    else:
        return None


REGEXES = [
    (re.compile(rf'\b{deny}\W*{any_sa}\W*{sa_hx_pred}\b', re.I),
     SuicideAttempt.NO),
    # must be above SA SA_pred due to 'denies hx of SA in teens'
    (re.compile(rf'\b(?:{deny}|{no})\W*(?:\w+\W*)?{hx_of}\W*{any_sa}\b', re.I),
     SuicideAttempt.NO, [check_if_colon_before]),
    (re.compile(rf'\b(?:{family_hx})\W*(?:\w+\W*)?{hx_of}\W*{any_sa}\b', re.I),
     SuicideAttempt.FAMILY, [check_if_colon_before]),
    (re.compile(rf'\b{any_sa}\W*{sa_hx_pred}\b', re.I),
     SuicideAttempt.HISTORY, [check_if_other_subject]),
    (re.compile(rf'\b{hx_of}\W*{any_sa}\s*:\s*(?:{deny}|{no})\b', re.I),
     SuicideAttempt.NO),
    # specific (optional <- these get caught by next regex; can't move up otherwise 'denied hx of sa in teens')
    (re.compile(
        rf'\b{hx_of}\W*{any_sa}\s*:\s*(?:{yes}|{number}|{sa_hx_pred})\b', re.I),
     SuicideAttempt.HISTORY),
    # more generic
    (re.compile(rf'\b{hx_of}\W*{any_sa}\b', re.I),
     SuicideAttempt.HISTORY, [check_if_other_subject, check_if_in_problem_list]),
    (re.compile(rf'\b(?:Z91.51|Z91.52|R45.88|R45.851|E958.9|V62.84)\b'),
     SuicideAttempt.CODE),
    # current suicide attempt
    (SA_PAT, SuicideAttempt.YES, [
        check_if_other_subject,
        check_if_in_problem_list,
        lambda *x, **kw: check_if_negated(*x, **kw, neg_concept=SuicideAttempt.NO),
    ]),
    (SA_ACTION_PAT, SuicideAttempt.YES_ACTION, [
        check_if_other_subject,
        lambda *x, **kw: check_if_negated(*x, **kw, neg_concept=SuicideAttempt.NO),
    ])
]

# find all occurrences of all non-overalpping regexes
RUN_REGEXES_FUNC = search_all_regex(REGEXES, suppress_overlaps=True)
