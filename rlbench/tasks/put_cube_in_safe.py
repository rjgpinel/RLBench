from typing import List, Tuple
import numpy as np
from pyrep.objects.shape import Shape
from pyrep.objects.dummy import Dummy
from pyrep.objects.proximity_sensor import ProximitySensor
from rlbench.backend.task import Task
from rlbench.backend.conditions import DetectedCondition, NothingGrasped
from rlbench.backend.spawn_boundary import SpawnBoundary

NUM_SHELVES_IN_SAFE = 3


class PutCubeInSafe(Task):

    def init_task(self) -> None:
        self.index_dic = {0: 'bottom', 1: 'middle', 2: 'top'}
        self.cube = Shape('cube')
        self.register_graspable_objects([self.cube])
        self.success_conditions = [NothingGrasped(self.robot.gripper)]

    def init_episode(self, index: int) -> List[str]:
        self.target_shelf = index
        w4 = Dummy('waypoint4')
        target_dummy_name = 'dummy_shelf' + str(self.target_shelf)
        target_pos_dummy = Dummy(target_dummy_name)
        target_pos = target_pos_dummy.get_position()
        w4.set_position(target_pos, reset_dynamics=False)

        self.success_detector = ProximitySensor(
            ('success_detector' + str(self.target_shelf))
        )

        while len(self.success_conditions) > 1:
            self.success_conditions.pop()

        self.success_conditions.append(
            DetectedCondition(self.cube, self.success_detector)
        )
        self.register_success_conditions(self.success_conditions)

        return ['put the cube away in the safe on the %s shelf'
                % self.index_dic[index],
                'leave the cube on the %s shelf on the safe'
                % self.index_dic[index],
                'place the cube on the %s shelf of the safe'
                % self.index_dic[index]]

    def variation_count(self) -> int:
        return NUM_SHELVES_IN_SAFE

    def base_rotation_bounds(self) -> Tuple[List[float], List[float]]:
        return [0.0, 0.0, 0.0], [0.0, 0.0, +0.5 * np.pi]
