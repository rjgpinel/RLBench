from typing import List
from pyrep.objects.joint import Joint
from rlbench.backend.conditions import JointCondition
from rlbench.backend.task import Task


class OpenLaptopLid(Task):

    def init_task(self) -> None:
        self.register_success_conditions([JointCondition(Joint('joint'), 0.0)])

    def init_episode(self, index: int) -> List[str]:
        return ['open laptop lid',
                'open the laptop',
                'unlock the laptop lid',
                'lip the laptop lid open',
                'pull the laptop lid upwards to open',
                'flip the laptop lid up to open']

    def variation_count(self) -> int:
        return 1
