from time import sleep

from tools.device import Device

PROFILES = {
    0: '(640x360)',
    1: '(848x480)',
    2: '(1280x720)',
    3: '(1920x1080)',
}


# def test_profile(device, profile_fixture):
#     device = device
#     (input, expected_output) = profile_fixture
#     device.set_profile(input)
#     assert device.show_stream_info() == expected_output


def test_probed(device):
    pass
    # assert info[1] == '1234567'

