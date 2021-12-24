import random
import warnings
from datetime import datetime, timedelta

import urllib3.exceptions
from apscheduler.events import (
    EVENT_JOB_SUBMITTED,
    EVENT_JOB_MAX_INSTANCES,
    EVENT_JOB_ERROR,
)
from apscheduler.events import JobExecutionEvent
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from services.cluster.lodge_of_sorceresses import __entropy__
from services.cluster.mage import decouple
from services.cluster.witcher import devil_king_armed
from services.middleware.subscribe_io import SubscribeManager
from services.middleware.workers_io import EntropyHeap
from services.settings import logger, TIME_ZONE_CN, POOL_CAP
from services.utils import CoroutineSpeedup, ToolBox

warnings.simplefilter("ignore", category=UserWarning)


class CollectorScheduler(CoroutineSpeedup):
    def __init__(self, job_settings: dict):
        super(CollectorScheduler, self).__init__()

        self.scheduler = BlockingScheduler()
        self.sm = SubscribeManager()
        self.eh = EntropyHeap()

        self.collector_name = "Cirilla[M]"
        self.checker_name = "Checker[M]"
        self.decoupler_name = "Decoupler[M]"

        self.scheduler_name = "CollectorScheduler[M]"

        self.job_settings = {
            "interval_collector": 120,
            "interval_decoupler": 3600,
            # 任务队列源 within [remote local]
            "source": "remote"
        }
        self.job_settings.update(job_settings)
        self.interval_collector = self.job_settings["interval_collector"]
        self.interval_decoupler = self.job_settings["interval_decoupler"]
        self.task_source = self.job_settings["source"]

        self.running_jobs = {}

        # True: 不打印 monitor-log
        self.freeze_screen = False

    def deploy_jobs(self, available_collector=True, available_decoupler=True):
        if available_collector:
            self._deploy_collector()
            self.scheduler.add_listener(
                callback=self._monitor,
                mask=(EVENT_JOB_ERROR | EVENT_JOB_SUBMITTED | EVENT_JOB_MAX_INSTANCES)
            )
            logger.success(ToolBox.runtime_report(
                action_name=self.scheduler_name,
                motive="JOB",
                message="The Collector was created successfully."
            ))

        if available_decoupler:
            self._deploy_decoupler()
            logger.success(ToolBox.runtime_report(
                action_name=self.scheduler_name,
                motive="JOB",
                message="The Decoupler was created successfully."
            ))

        if any((available_decoupler, available_collector)):
            self.start()

    def start(self):
        try:
            self.scheduler.start()
        except KeyboardInterrupt:
            logger.debug(ToolBox.runtime_report(
                motive="EXITS",
                action_name=self.scheduler_name,
                message="Received keyboard interrupt signal."
            ))

    def _deploy_collector(self):
        self.scheduler.add_job(
            func=self.go,
            id=self.collector_name,
            trigger=IntervalTrigger(
                seconds=self.interval_collector,
                timezone="Asia/Shanghai",
            ),
            max_instances=4
        )
        self.scheduler.add_job(
            func=self.sm.refresh,
            id=self.checker_name,
            trigger=IntervalTrigger(
                seconds=60,
                timezone="Asia/Shanghai",
            ),
            max_instances=20
        )

    def _deploy_decoupler(self):
        self.scheduler.add_job(
            func=decouple,
            id=self.decoupler_name,
            trigger=IntervalTrigger(
                seconds=self.interval_decoupler,
                timezone="Asia/Shanghai"
            ),
            max_instances=15,
        )

    def _monitor_logger(self, event: JobExecutionEvent):
        debug_log = {
            "event": event,
            "pending_jobs": self.worker.qsize(),
            "running_jobs": len(self.running_jobs),
            "message": "pending_jobs[{}] running_jobs[{}]".format(
                self.worker.qsize(), self.running_jobs.__len__(),
            ),
        }

        if not self.freeze_screen:
            pool_status = "pool_status[{}/{}]".format(
                self.eh.__len__(), POOL_CAP
            )
            message = "{} {}".format(
                debug_log.get("message"), pool_status
            )
            logger.debug(ToolBox.runtime_report(
                motive="HEARTBEAT",
                action_name=self.scheduler_name,
                message=message,
                job_id=event.job_id if event.code >= 2 ** 9 else "__init__",
                event=event
            ))

    def _monitor(self, event):
        self._monitor_logger(event)

        if self.running_jobs.__len__() == 0:
            return True

        # 识别并移除失活实例
        for session_id, instance in list(self.running_jobs.items()):
            is_timeout = (
                    instance["start-time"]
                    + timedelta(seconds=instance["running-limit"])
                    < datetime.now(TIME_ZONE_CN)
            )
            if not is_timeout:
                continue

            try:
                instance["service"].quit()
                self.running_jobs.pop(session_id)
                logger.error(ToolBox.runtime_report(
                    motive="KILL",
                    action_name=instance["name"],
                    inactivated_instance=session_id
                ))
            except Exception as e:
                logger.critical(ToolBox.runtime_report(
                    motive="ERROR",
                    action_name=instance["name"],
                    by="CollectorSchedulerMonitor停用失活实例时出现未知异常",
                    error=e
                ))

        # 重置定时任务
        if (
                len(self.running_jobs) == 0
                and self.worker.qsize() == 0
        ):
            self.scheduler.remove_job(job_id=self.collector_name)
            self.scheduler.remove_job(job_id=self.checker_name)
            self._deploy_collector()

            logger.warning(ToolBox.runtime_report(
                motive="HEARTBEAT",
                action_name=self.scheduler_name,
                message="The echo-loop job of collector has been reset."
            ))

    # ---------------------
    # Coroutine
    # ---------------------
    def preload(self):
        """

        :return:
        """
        eh = self.eh

        # 根据任务源选择本地/远程任务队列 默认使用远程队列
        pending_entropy = eh.sync() if self.task_source == "remote" else __entropy__.copy()

        # 弹回空任务，防止订阅溢出
        if eh.__len__() >= POOL_CAP or not pending_entropy:
            return []

        # 消减任务实例，控制订阅池容量
        mirror_entropy = pending_entropy.copy()
        qsize = pending_entropy.__len__()
        random.shuffle(mirror_entropy)

        while eh.__len__() + qsize > int(POOL_CAP * 0.8):
            if mirror_entropy.__len__() < 1:
                break
            mirror_entropy.pop()
            qsize -= 1

        return mirror_entropy

    def overload(self):
        mirror_entropy = self.preload()

        if not mirror_entropy:
            self.max_queue_size = 0
            return False

        for atomic in mirror_entropy:
            self.worker.put_nowait(atomic)

        self.max_queue_size = self.worker.qsize()

    def launcher(self, *args, **kwargs):
        while not self.worker.empty():
            atomic = self.worker.get_nowait()
            self.control_driver(atomic=atomic, sm=self.sm, *args, **kwargs)
        logger.success("运行结束")

    @logger.catch()
    def control_driver(self, atomic: dict, *args, **kwargs):
        """

        :param atomic:
        :return:
        """

        """
        TODO [√]参数调整
        -------------------
        """
        # 协同模式
        is_synergy = bool(atomic.get("synergy"))

        # 添加节拍集群节拍
        if not atomic.get("hyper_params"):
            atomic["hyper_params"] = {}
        atomic["hyper_params"]["beat_dance"] = 0.5 * (self.max_queue_size - self.worker.qsize() + 1)

        """
        TODO [√]实例生产
        -------------------
        """
        cirilla = devil_king_armed(atomic, silence=True)

        service = cirilla.set_chrome_options()
        cirilla_id = service.session_id

        # 标记运行实例
        self.running_jobs.update(
            {
                cirilla_id: {
                    "service": service,
                    "start-time": datetime.now(TIME_ZONE_CN),
                    "running-limit": cirilla.work_clock_max_wait,
                    "name": cirilla.action_name
                }
            }
        )
        """
        TODO [√]实例投放
        -------------------
        """
        try:
            cirilla.assault(service, synergy=is_synergy, sm=kwargs.get("sm"))
        except urllib3.exceptions.ClosedPoolError:
            pass
        finally:
            try:
                self.running_jobs.pop(cirilla_id)
                logger.debug(ToolBox.runtime_report(
                    motive="DETACH",
                    action_name=cirilla.action_name,
                ))
            except KeyError:
                pass
