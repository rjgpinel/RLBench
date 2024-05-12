from typing import List, Tuple

import numpy as np
from pyrep.objects.dummy import Dummy
from pyrep.objects.joint import Joint
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition, ConditionSet
from rlbench.backend.task import Task


ITEMS = ["block", "cylinder", "moon"]

class PutItemsInDrawer(Task):

    def init_task(self) -> None:
        self._options = ['bottom', 'middle', 'top']
        self._options_items = [['block', 'cylinder', 'moon'],
                               ['block', 'moon', 'cylinder'],
                               ['cylinder', 'block', 'moon'],
                               ['cylinder', 'moon', 'block'],
                               ['moon', 'block', 'cylinder'],
                               ['moon', 'cylinder', 'block']]
        self._anchors = [Dummy('waypoint_anchor_%s' % opt)
                         for opt in self._options]
        self._joints = [Joint('drawer_joint_%s' % opt)
                        for opt in self._options]
        self._waypoint1 = Dummy('waypoint2')
        self._block = Shape('block')
        self._cylinder = Shape('cylinder')
        self._moon = Shape('moon')
        self._items = {'block': self._block, 'cylinder': self._cylinder, 'moon': self._moon}

        self._items_waypoints = {item: [Dummy(f"{item}_waypoint{i}") for i in range(3)] for item in ITEMS}

        self._grasp_item1 = [Dummy("waypoint6"), Dummy("waypoint7"), Dummy("waypoint8")]
        self._grasp_item2 = [Dummy("waypoint12"), Dummy("waypoint13"), Dummy("waypoint14")]
        self._grasp_item3 = [Dummy("waypoint18"), Dummy("waypoint19"), Dummy("waypoint20")]

        self._grasp_items = [self._grasp_item1, self._grasp_item2, self._grasp_item3]
        self.register_graspable_objects([self._block, self._cylinder, self._moon])

    def init_episode(self, index) -> List[str]:
        option = self._options[index % 3]
        anchor = self._anchors[index % 3]
        option_items = self._options_items[index // 3]
        self._waypoint1.set_position(anchor.get_position())
        success_sensor = ProximitySensor('success_' + option)

        self._success_conditions = []
        for item_id, item_name in enumerate(option_items):
            for waypoint_id in range(len(self._items_waypoints[item_name])):
                self._grasp_items[item_id][waypoint_id].set_pose(self._items_waypoints[item_name][waypoint_id].get_pose())
            item = self._items[item_name]
            self._success_conditions.append(DetectedCondition(item, success_sensor))

        self.register_success_conditions([ConditionSet(self._success_conditions, True, True)])


        rtn0 = f'put the {option_items[0]} in the {option} drawer, then the {option_items[1]} and then the {option_items[2]}'
        rtn1 = f'put the {option_items[0]} away in the {option} drawer, then put the {option_items[1]} and then put the {option_items[2]}'
        rtn2 = f'open the {option} drawer and place the {option_items[0]} inside of it, then place the {option_items[1]} inside and finally the {option_items[2]}'
        rtn3 = f'leave the {option_items[0]} in the {option} drawer, then leave the {option_items[1]} and finish by leaving the {option_items[2]} inside'

        return [rtn0, rtn1, rtn2, rtn3]

    def variation_count(self) -> int:
        num_options_drawer = 3
        num_options_items = 6
        return num_options_drawer * num_options_items

    def base_rotation_bounds(self) -> Tuple[List[float], List[float]]:
        return [0, 0, - np.pi / 8], [0, 0, np.pi / 8]
