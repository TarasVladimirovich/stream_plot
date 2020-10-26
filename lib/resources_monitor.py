import logging

from lib.constansts import SECOND

logger = logging.getLogger(__name__)


class ResourcesMonitor:
    """
    Implementation of object which collects next performance data from MX/GW
    1) CPU (idle, system, user) time
    """

    def __init__(self, mxserver):
        self.mxserver = mxserver

    def generate_executor_script(self, interval: int = SECOND) -> str:

        pid_mxserver = self.mxserver.pidof('java')

        command = f"timeout {interval} top -b -d 1 -p {pid_mxserver} " \
                  f"| awk '/^%Cpu0/{{id0=$9; sy0=$5}} " \
                  f"/^%Cpu1/{{id1=$9; sy1=$5}} " \
                  f"/^%Cpu2/{{id2=$9; sy2=$5}} " \
                  f"/^%Cpu3/{{id3=$9; sy3=$5}} " \
                  f"/{pid_mxserver}+ mxserver/{{print id0,sy0,id1,sy1,id2,sy2,id3,sy3,mem,$9,$10; fflush() }}' " \
                  f">> /tmp/{self.mxserver.file_name} &"

        return command
