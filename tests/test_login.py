Íimport logging
import string
import random

import pytest

from api.auth_manager import AuthManager
from configs.env_variable import STANDARD_USER, STANDARD_PASS

logger = logging.getLogger(__name__)

constant = [
    [(STANDARD_USER, STANDARD_PASS), 200],
    [(STANDARD_PASS, STANDARD_USER), 401],
    [(STANDARD_USER, STANDARD_USER), 401],
    [(STANDARD_PASS, STANDARD_PASS), 401],
    [('', ''), 401],
    [(' ', ' '), 401],
    [('', STANDARD_PASS), 401],
    [(STANDARD_USER, ''), 401],
]


def random_auth():
    user = "".join([random.choice(string.printable) for i in range(random.randrange(255))])
    password = "".join([random.choice(string.printable) for i in range(random.randrange(255))])
    return [(user, password), 401]


test_data = [random_auth() for _ in range(10)]
test_data.extend(constant)


@pytest.mark.parametrize('test_input, expected', test_data, ids=[f'Test {i + 1}' for i in range(len(test_data))])
def test_login(mxserver, test_input, expected):
    auth = AuthManager(mxserver)
    response = auth.get_response(test_input[0], test_input[1])
    logger.info(f'input_user: {test_input[0]}\n'
                f'input_pass: {test_input[1]}\n'
                f'status_code: {response.status_code}\n'
                f'status_code_expected: {expected}\n')
    logger.info(response.text)
    assert response.status_code == expected
