import time
import logging


log = logging.getLogger(__name__)


def test_5_min(device, resources_prepare, time_out=300):
    artifacts = dict()
    pid = device.client.execute_command("systemctl status stream | awk '/Main PID/{print $3}'")
    time.sleep(3)
    part1 = f"timeout -t {time_out} top -b -d 0.2 -p {pid} "
    part2 = "| awk '/%Cpu/{idle=$8} /%Cpu/{sys=$4} /[0-9]+ root/{print idle,sys,$9,$10}'"
    part3 = f">> /tmp/{device.file_name} & "
    command = part1 + part2 + part3

    log.info('==== Start test =====')
    device.client.execute_commands([f'echo idle sys stream memory > /tmp/{device.file_name}'])
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
    log.info('!!!! Stop stream !!!!')
    device.client.execute_commands(['/ring/bin/ipc_cli streamStop'])
    time.sleep(30)

    device.artifacts.update(artifacts)
    device.client.download_file(file=f'/tmp/{device.file_name}')
    log.info('==== End test ====')

