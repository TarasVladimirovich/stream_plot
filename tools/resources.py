import time
import logging

from lib.ipc import DingType


logger = logging.getLogger(__name__)


def test_5_min(mxserver, time_out=10):

    def prepare_setup():
        logger.info('==== START PREPARE =====')
        time.sleep(2)
        logger.info('==== END PREPARE =====')

    def clean_setup():
        logger.info('==== START POSTCONDITION =====')
        time.sleep(2)
        logger.info('==== END POSTCONDITION =====')

    prepare_setup()
    time.sleep(3)
    # mxserver.client.execute_commands(
    #     [f'echo idle Stream StreamMem Pulseaudio PulseMem Ivaapp sys > /tmp/{mxserver.file_name}'])

    pid_mxserver = mxserver.pidof('java')
    time.sleep(3)

    logger.info('==== Start test =====')

    command = f"timeout {time_out} top -b -d 1 -p {pid_mxserver} " \
              f"| awk '/^%Cpu0/{{id0=$9; sy0=$5}} " \
              f"/^%Cpu1/{{id1=$9; sy1=$5}} " \
              f"/^%Cpu2/{{id2=$9; sy2=$5}} " \
              f"/^%Cpu3/{{id3=$9; sy3=$5}} " \
              f"/{pid_mxserver}+ mxserver/{{print id0,sy0,id1,sy1,id2,sy2,id3,sy3,mem,$9,$10}}' " \
              f">> /tmp/{mxserver.file_name}"

    logger.info(f'execute command: {command}')
    mxserver.client.execute_command(command)
    time.sleep(time_out)

    # mxserver.client.download_file(file=f'/tmp/{mxserver.file_name}')
    logger.info('==== End test ====')

    clean_setup()
