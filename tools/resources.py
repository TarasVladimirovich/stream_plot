import time
import logging

from lib.ipc import DingType


logger = logging.getLogger(__name__)


def test_5_min(device, profile, bitrate, idle=False, time_out=310):
    artifacts = dict()

    def prepare_setup():
        logger.info('==== START PREPARE =====')
        device.make_write_fs()
        commands_prepare = ['mkdir /usr/share/terminfo/d',
                            'cp /usr/share/terminfo/v/vt100 /usr/share/terminfo/d/dumb']
        device.client.execute_commands(commands_prepare)
        if profile is not None:
            device.rp.set_profile(profile)
            artifacts['Profile'] = profile
        if bitrate is not None:
            device.rp.set_test_bitrate(bitrate)
            artifacts['Test bitrate'] = bitrate
        if not idle:
            device.restart_service('stream')
        time.sleep(2)
        artifacts['Resolution'] = device.show_stream_info()
        logger.info('==== END PREPARE =====')

    def clean_setup():
        logger.info('==== START POSTCONDITION =====')
        if profile is not None:
            device.rp.unset_profile()
        if bitrate is not None:
            device.rp.unset_test_bitrate()
        device.client.execute_command('rm -rf /usr/share/terminfo/d')
        device.make_read_fs()
        if not idle:
            device.restart_service('stream')
        logger.info('==== END POSTCONDITION =====')

    prepare_setup()
    time.sleep(3)
    device.client.execute_commands(
        [f'echo idle stream memory pulseaudio memPulse ivaapp sys > /tmp/{device.file_name}'])

    pid_stream, pid_pulse, pid_ivaapp = device.service_pid('stream'), \
        device.service_pid('pulseaudio'), device.service_pid('ivaapp')
    time.sleep(3)

    logger.info('==== Start test =====')

    command = f"timeout -t {time_out} top -b -d 0.5 -p {pid_stream}, {pid_pulse}, {pid_ivaapp} " \
              f"| awk '/^%Cpu/{{idle=$8, sys=$4}} " \
              f"/{pid_stream}+ root/{{cpu=$9, mem=$10}} " \
              f"/{pid_ivaapp}+ root/{{cpuiv=$9}} " \
              f"/{pid_pulse}+ pulse/{{print idle,cpu,mem,$9,$10,cpuiv,sys}}' >> /tmp/{device.file_name} & "

    logger.info(f'execute command: {command}')

    device.client.execute_command(command)

    if idle:
        time.sleep(310)
    else:
        time.sleep(30)
        logger.info('!!!! Start the unanswered event !!!!')
        device.ipc.ding_request(DingType.MOTION)
        time.sleep(5)
        artifacts['ding_1'] = device.rp.get_ding_id()
        time.sleep(55)
        device.ipc.stream_stop()
        time.sleep(30)
        logger.info('!!!! Start the answered event with 2-way talk event!!!!')
        device.ipc.ding_request(DingType.MOTION)
        time.sleep(30)
        artifacts['ding_2'] = device.rp.get_ding_id()
        time.sleep(120)
        device.ipc.stream_stop()
        time.sleep(40)

    device.artifacts.update(artifacts)
    device.client.download_file(file=f'/tmp/{device.file_name}')
    logger.info('==== End test ====')

    clean_setup()
