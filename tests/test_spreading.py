from time import sleep

import pytest

from tools.device import Device

PROFILES = [
    [0, '(640x360) 10/10'],
    [1, '(848x480) 15/15'],
    [2, '(1280x720) 15/15'],
    [3, '(1920x1080) 15/15'],
]


@pytest.mark.parametrize('profile, expected', PROFILES)
def test_profile(device, profile, expected):
    device.set_profile(profile)
    assert device.show_stream_info() == expected


def test_probed(device):
    pass
    # assert info[1] == '1234567'

