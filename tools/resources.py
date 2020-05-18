import time
import logging

COMMANDS_PREPARE = ['mount -o remount,rw /', 'mkdir /usr/share/terminfo/d',
                    'cp /usr/share/terminfo/v/vt100 /usr/share/terminfo/d/dumb',
                    '/ring/bin/rp set test.profile_id 6', '/ring/bin/rp set test.bitrate 2500000',
                    'systemctl restart stream']

COMMANDS_CLEAN = ['rm -rf /usr/share/terminfo/d',
                  '/ring/bin/rp unset test.profile_id ', '/ring/bin/rp unset test.bitrate 2500000',
                  'systemctl restart stream', 'mount -o remount,ro /']

log = logging.getLogger(__name__)


def __prepare_setup(device):
    log.info('Prepare setup \n {}'.format(' ;\n '.join(COMMANDS_PREPARE)))
    device.client.execute_commands(COMMANDS_PREPARE)


def test_5_min(device, time_out=300):
    artifacts = dict()
    __prepare_setup(device)
    pid_stream = device.client.execute_command("systemctl status stream | awk '/Main PID/{print $3}'")
    pid_pulse = device.client.execute_command("systemctl status pulseaudio | awk '/Main PID/{print $3}'")
    pid_ivaapp = device.client.execute_command("systemctl status ivaapp | awk '/Main PID/{print $3}'")
    time.sleep(3)

    part1 = f"timeout -t {time_out} top -b -d 0.2 -p {pid_stream}, {pid_pulse}, {pid_ivaapp} "
    part2 = f"| awk '/^%Cpu/{{idle=$8, sys=$4}} /{pid_stream}/{{cpu=$9, mem=$10}} /{pid_ivaapp}/{{cpuiv=$9}} " \
            f"/{pid_pulse}/{{print idle,cpu,mem,$9,$10,cpuiv,sys}}' >> /tmp/{device.file_name} & "
    command = part1 + part2

    log.info('==== Start test =====')
    device.client.execute_commands([f'echo idle stream memory pulseaudio memPulse ivaapp sys > /tmp/{device.file_name}'])
    device.client.execute_commands([command])

    time.sleep(30)
    log.info('!!!! Start the unanswered event !!!!')
    device.client.execute_commands(['/ring/bin/ipc_cli dingRequest motion'])
    time.sleep(5)
    artifacts['ding_1'] = device.client.execute_command('/ring/bin/rp get ding.id | cut -d ":" -f2')
    time.sleep(55)
    log.info('!!!! Stop the unanswered event !!!!')

    time.sleep(30)
    log.info('!!!! Start the answered event !!!!')
    device.client.execute_commands(['/ring/bin/ipc_cli dingRequest motion'])
    time.sleep(30)
    artifacts['ding_2'] = device.client.execute_command('/ring/bin/rp get ding.id | cut -d ":" -f2')
    log.info('!!!! You must enable 2-way audio !!!!')
    time.sleep(120)
    device.client.execute_commands(['/ring/bin/ipc_cli streamStop'])
    log.info('!!!! Stop stream !!!!')
    time.sleep(30)

    __clean_setup(device)
    device.artifacts.update(artifacts)
    device.client.download_file(file=f'/tmp/{device.file_name}')
    log.info('==== End test ====')


def __clean_setup(device):
    log.info('Clean setup \n {}'.format(' ;\n '.join(COMMANDS_CLEAN)))
    device.client.execute_commands(COMMANDS_CLEAN)
