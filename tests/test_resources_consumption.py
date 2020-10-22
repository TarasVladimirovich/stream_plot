import time
import logging


log = logging.getLogger(__name__)


def test_5_min(mxserver, resources_prepare, time_out=300):
    artifacts = dict()
    pid = mxserver.client.execute_command("systemctl status stream | awk '/Main PID/{print $3}'")
    time.sleep(3)
    part1 = f"timeout -t {time_out} top -b -d 0.2 -p {pid} "
    part2 = "| awk '/%Cpu/{idle=$8} /%Cpu/{sys=$4} /[0-9]+ root/{print idle,sys,$9,$10}'"
    part3 = f">> /tmp/{mxserver.file_name} & "
    command = part1 + part2 + part3

    log.info('==== Start test =====')
    mxserver.client.execute_commands([f'echo idle sys stream memory > /tmp/{mxserver.file_name}'])
    mxserver.client.execute_commands([command])

    time.sleep(30)
    log.info('!!!! Start the unanswered event !!!!')
    mxserver.client.execute_commands(['/ring/bin/ipc_cli dingRequest motion'])
    time.sleep(5)
    artifacts['ding_1'] = mxserver.client.execute_command('/ring/bin/rp get ding.id | cut -d ":" -f2')
    time.sleep(55)
    log.info('!!!! Stop the unanswered event !!!!')

    time.sleep(30)
    log.info('!!!! Start the answered event !!!!')
    mxserver.client.execute_commands(['/ring/bin/ipc_cli dingRequest motion'])
    time.sleep(30)
    artifacts['ding_2'] = mxserver.client.execute_command('/ring/bin/rp get ding.id | cut -d ":" -f2')
    log.info('!!!! You must enable 2-way audio !!!!')
    time.sleep(120)
    mxserver.client.execute_commands(['/ring/bin/ipc_cli streamStop'])
    log.info('!!!! Stop stream !!!!')
    time.sleep(30)

    mxserver.artifacts.update(artifacts)
    mxserver.client.download_file(file=f'/tmp/{mxserver.file_name}')
    log.info('==== End test ====')

