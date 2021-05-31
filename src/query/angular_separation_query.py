import math
from typing import Union

from constants import Planet
from generate.angular_separation import EclipticPosition
from query.database import Database
from query.abstract_query import AbstractQuery, SearchRange
from util import TimeValue


class AngularSeparationQuery(AbstractQuery):

    def __init__(self, db: Database, from_body: Union[Planet, str], to_body: Union[Planet, str], target_angle: float,
                 tolerance: float, target_position: Union[EclipticPosition, None], target_time: SearchRange):
        if type(from_body) == Planet:
            from_body = from_body.name
        if type(to_body) == Planet:
            to_body = to_body.name
        self.target_time = target_time
        self.from_body = from_body
        self.to_body = to_body
        self.target_angle = target_angle
        self.target_position = target_position
        self.tolerance = tolerance
        sep = db.separations_in_range(from_body, to_body, target_time.start, target_time.end)
        if len(sep) < 1:
            raise RuntimeError("Failed to find any separations between {} and {} at {} to {}, check database"
                               .format(from_body, to_body, target_time.start, target_time.end))
        sep.sort(key=lambda x: abs(x['angle'] - target_angle))
        if target_position is not None:
            filtered = list(filter(lambda x: x['angle'] <= tolerance and x['position'] == target_position.value, sep))
            if len(filtered) > 0:
                self.best = filtered[0]
            else:
                self.best = sep[0]
        else:
            self.best = sep[0]

    def get_search_range(self) -> SearchRange:
        return self.target_time

    def result_function(self, x: float) -> float:
        res = 1 - math.pow((x / (self.tolerance / 2.0)), 2)
        return max(res, 0)

    def quality_score(self) -> float:
        """
        If angle is within tolerance of the target_angle score 1.0
        Decreasing score as the angle moves from target_angle+tolerance up to target_angle + (1.5 * tolerance)
        Correct position (if specified) adds 0.2 to score
        """
        lower_bound = max(self.target_angle - self.tolerance, 0)
        upper_bound = self.target_angle + self.tolerance
        actual = self.best['angle']
        if lower_bound <= actual <= upper_bound:
            angle_score = 1.0
        else:
            diff = min(abs(actual - lower_bound), abs(actual - upper_bound))
            angle_score = self.result_function(diff)
        if angle_score == 0:
            return 0
        if self.target_position is not None:
            if self.best['position'] == self.target_position.value:
                position_score = 1
            else:
                position_score = 0
            return (angle_score * 0.8) + (position_score * 0.2)
        else:
            return angle_score

    def output(self) -> dict:
        return {
            'from_body': self.from_body,
            'to_body': self.to_body,
            'angle': self.best['angle'],
            'position': self.best['position'],
            'at_time': TimeValue(self.best['time']),
        }