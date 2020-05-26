import time
import logging

from lib.ipc import DingType


logger = logging.getLogger(__name__)


def test_5_min(device, profile, bitrate, time_out=310):

    def prepare_setup():
        logger.info('==== START PREPARE =====')
        device.make_write_fs()
        commands_prepare = ['mkdir /usr/share/terminfo/d',
                            'cp /usr/share/terminfo/v/vt100 /usr/share/terminfo/d/dumb']
        device.client.execute_commands(commands_prepare)
        device.rp.set_profile(profile)
        device.rp.set_test_bitrate(bitrate)
        device.restart_service('stream')
        logger.info('==== END PREPARE =====')

    def clean_setup():
        logger.info('==== START POSTCONDITION =====')
        device.rp.unset_profile()
        device.rp.unset_test_bitrate()
        device.client.execute_command('rm -rf /usr/share/terminfo/d')
        device.make_read_fs()
        device.restart_service('stream')
        logger.info('==== END POSTCONDITION =====')

    artifacts = dict()
    prepare_setup()
    time.sleep(3)
    device.client.execute_commands(
        [f'echo idle stream memory pulseaudio memPulse ivaapp sys > /tmp/{device.file_name}'])

    pid_stream, pid_pulse, pid_ivaapp = device.service_pid('stream'), \
        device.service_pid('pulseaudio'), device.service_pid('ivaapp')
    time.sleep(3)

    logger.info('==== Start test =====')

    command = f"timeout -t {time_out} top -b -d 0.2 -p {pid_stream}, {pid_pulse}, {pid_ivaapp} " \
              f"| awk '/^%Cpu/{{idle=$8, sys=$4}} " \
              f"/{pid_stream}+ root/{{cpu=$9, mem=$10}} " \
              f"/{pid_ivaapp}+ root/{{cpuiv=$9}} " \
              f"/{pid_pulse}+ pulse/{{print idle,cpu,mem,$9,$10,cpuiv,sys}}' >> /tmp/{device.file_name} & "

    logger.info(f'execute command: {command}')

    device.client.execute_command(command)

    time.sleep(30)
    logger.info('!!!! Start the unanswered event !!!!')
    device.ipc.ding_request(DingType.MOTION)
    time.sleep(5)
    artifacts['ding_1'] = device.rp.get_ding_id()
    time.sleep(55)
    device.ipc.stream_stop()
    logger.info('!!!! Stop the unanswered event !!!!')

    time.sleep(30)
    logger.info('!!!! Start the answered event with 2-way talk event!!!!')
    device.ipc.ding_request(DingType.MOTION)
    time.sleep(30)
    artifacts['ding_2'] = device.rp.get_ding_id()
    time.sleep(120)
    device.ipc.stream_stop()
    time.sleep(30)

    device.artifacts.update(artifacts)
    device.client.download_file(file=f'/tmp/{device.file_name}')
    logger.info('==== End test ====')

    clean_setup()
