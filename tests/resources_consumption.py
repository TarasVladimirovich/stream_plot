import time


COMMANDS_PREPARE = ['mount -o remount,rw /', 'mkdir /usr/share/terminfo/d',
                    'cp /usr/share/terminfo/v/vt100 /usr/share/terminfo/d/dumb',
                    '/ring/bin/rp set test.profile_id 3', '/ring/bin/rp set test.bitrate 2500000',
                    'systemctl restart stream']

COMMANDS_CLEAN = ['rm -rf /usr/share/terminfo/d',
                  '/ring/bin/rp unset test.profile_id 3', '/ring/bin/rp unset test.bitrate 2500000',
                  'systemctl restart stream', 'mount -o remount,ro /']


def __prepare_setup(client):
    print(*COMMANDS_PREPARE, sep=' ; ')
    client.execute_commands(COMMANDS_PREPARE)


def test_5_min(client, file_name='results.txt', time_out=300):
    artifacts = dict()
    print("Prepare setup")
    __prepare_setup(client)
    pid = client.get_info_from_remote_host("systemctl status stream | grep 'Main PID' | awk \{'print $3'\}")
    time.sleep(3)
    part1 = f"timeout -t {time_out} top -b -d 0.2 -p {pid} "
    part2 = "| awk '/%Cpu/{idle=$8} /KiB Mem/{total=$4} /avail Mem/{avail=$9} /[0-9]+ root/{print idle,$9,$10}' "
    part3 = f">> /tmp/{file_name} & "
    command = part1 + part2 + part3
    print('Start test')
    client.execute_commands([f'echo idle stream memory > /tmp/{file_name}'])
    client.execute_commands([command])
    time.sleep(30)
    print('Start the unanswered event')
    client.execute_commands(['/ring/bin/ipc_cli dingRequest motion'])
    time.sleep(5)
    artifacts['ding_1'] = client.get_info_from_remote_host('/ring/bin/rp get ding.id | cut -d ":" -f2')
    time.sleep(55)
    print('Stop the unanswered event')
    time.sleep(30)
    print('Start the answered event')
    client.execute_commands(['/ring/bin/ipc_cli dingRequest motion'])
    time.sleep(30)
    artifacts['ding_2'] = client.get_info_from_remote_host('/ring/bin/rp get ding.id | cut -d ":" -f2')
    print('You must enable 2-way audio')
    time.sleep(120)
    print('Stop stream')
    client.execute_commands(['/ring/bin/ipc_cli streamStop'])
    time.sleep(30)
    print("Clean setup")
    __clean_setup(client)
    print('Stop test')
    return artifacts


def __clean_setup(client):
    print(*COMMANDS_CLEAN, sep=' ; ')
    client.execute_commands(COMMANDS_CLEAN)
