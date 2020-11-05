import logging
import string
import random

import pytest

from lib.auth_manager import AuthManager

logger = logging.getLogger(__name__)

SUCCESSFUL_CRED = [('admin', 'Barbapapa12#'), 200]
TWO_USER = [('admin', 'admin'), 401]
TWO_PASS = [('Barbapapa12#', 'Barbapapa12#'), 401]
EMPTY = [('', ''), 401]
SPACES = [(' ', ' '), 401]
ONLY_PASS = [('', 'Barbapapa12#'), 401]
ONLY_USER = [('admin', ''), 401]


def random_auth():
    user = "".join([random.choice(string.printable) for i in range(random.randrange(255))])
    password = "".join([random.choice(string.printable) for i in range(random.randrange(255))])
    return [(user, password), 401]


test_data = [random_auth() for _ in range(10)]
test_data.extend([SUCCESSFUL_CRED, TWO_USER, TWO_PASS, EMPTY, SPACES, ONLY_PASS, ONLY_USER])


@pytest.mark.parametrize('test_input, expected', test_data, ids=[f'Test {i+1}' for i in range(len(test_data))])
def test_successful_login(mxserver, test_input, expected):
    auth = AuthManager(mxserver, test_input[0], test_input[1])
    response = auth.get_response()
    logger.info(f'input_user: {test_input[0]}\n'
                f'input_pass: {test_input[1]}\n'
                f'status_code: {response.status_code}\n'
                f'status_code_expected: {expected}\n')
    logger.info(response.text)
    assert response.status_code == expected
