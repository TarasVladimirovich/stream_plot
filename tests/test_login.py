import logging

from lib.auth_manager import AuthManager

logger = logging.getLogger(__name__)


def test_successful_login(mxserver, param_test_auth):
    (param, expected) = param_test_auth
    auth = AuthManager(mxserver, param[0], param[1])
    response = auth.get_response()
    logger.info(f'input: {param}, output: {response.status_code}, expected: {expected}')
    logger.info(response.text)
    assert response.status_code == expected
