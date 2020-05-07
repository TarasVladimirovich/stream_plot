import time
import logging


log = logging.getLogger(__name__)


def test_5_min(client_setup, resources_prepare, time_out=300):
    artifacts = dict()
    pid = client_setup.execute_command("systemctl status stream | grep 'Main PID' | awk \{'print $3'\}")
    time.sleep(3)
    part1 = f"timeout -t {time_out} top -b -d 0.2 -p {pid} "
    part2 = "| awk '/%Cpu/{idle=$8} /KiB Mem/{total=$4} /avail Mem/{avail=$9} /[0-9]+ root/{print idle,$9,$10}' "
    part3 = f">> /tmp/{client_setup.file_name} & "
    command = part1 + part2 + part3

    log.info('==== Start test =====')
    # client_setup.execute_commands([f'echo idle stream memory > /tmp/{client_setup.file_name}'])
    # client_setup.execute_commands([command])
    #
    # time.sleep(30)
    # log.info('!!!! Start the unanswered event !!!!')
    # client_setup.execute_commands(['/ring/bin/ipc_cli dingRequest motion'])
    # time.sleep(5)
    # artifacts['ding_1'] = client_setup.execute_command('/ring/bin/rp get ding.id | cut -d ":" -f2')
    # time.sleep(55)
    # log.info('!!!! Stop the unanswered event !!!!')
    #
    # time.sleep(30)
    # log.info('!!!! Start the answered event !!!!')
    # client_setup.execute_commands(['/ring/bin/ipc_cli dingRequest motion'])
    # time.sleep(30)
    # artifacts['ding_2'] = client_setup.execute_command('/ring/bin/rp get ding.id | cut -d ":" -f2')
    # log.info('!!!! You must enable 2-way audio !!!!')
    # time.sleep(120)
    # log.info('!!!! Stop stream !!!!')
    # client_setup.execute_commands(['/ring/bin/ipc_cli streamStop'])
    # time.sleep(30)

    client_setup.artifacts.update(artifacts)
    client_setup.download_file(file=f'/tmp/{client_setup.file_name}')
    log.info('==== End test ====')

