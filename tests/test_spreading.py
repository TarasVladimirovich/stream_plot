


def set_profile(client):
    client.execute_commands(['/ring/bin/rp set stream.probed_bitrate 1234567', 'systemctl restart stream',
                             ])


def test_profile(client_setup):
    print("test")


def test_probed(client_setup):
    result = client_setup.execute_command('/ring/bin/rp list | grep stream.probed_bitrate')
    info = result.split(':')
    # assert info[1] == '1234567'

