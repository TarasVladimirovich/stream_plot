import time
import logging

from lib.resources_monitor import ResourcesMonitor


logger = logging.getLogger(__name__)


def test_5_min(mxserver, resources_prepare, time_out=310):

    resource = ResourcesMonitor(mxserver)
    # mxserver.client.execute_commands(
    #     [f'echo idle Stream StreamMem Pulseaudio PulseMem Ivaapp sys > /tmp/{mxserver.file_name}'])

    logger.info('======== Start test =========')

    mxserver.client.execute_command(resource.generate_executor_script(time_out))
    time.sleep(time_out)

    # mxserver.client.download_file(file=f'/tmp/{mxserver.file_name}')
    logger.info('======== End test ========')
