import logging
import string
import random

import pytest

from api.upload_license import UploadLicense

logger = logging.getLogger(__name__)

constant = '8032BB24-1256-0F99-B1EC-E9AD786F3E5D'


def random_auth():
    code = "".join([random.choice(string.printable) for i in range(random.randrange(255))])
    return [code, 401]


test_data = [random_auth() for _ in range(10)]
test_data.extend(constant)


# @pytest.mark.parametrize('test_input, expected', test_data, ids=[f'Test {i + 1}' for i in range(len(test_data))])
def test_upload_license(mxserver, app):
    flex_protect = ''
    expected = 400
    lic = UploadLicense(mxserver)
    response = lic.register_mx(flex_protect, app)
    logger.info(f'input_flex_protect: {flex_protect}\n')
    logger.info(response.text)
    assert response.status_code == expected
