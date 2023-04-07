import attr
import math

from .base import BaseObject, Intersection, Ray
from .vector import Vector


def solve_quadratic(a, b, c) -> tuple[float, float] | None:
    """
    Find all roots of a quadratic equation and return the in sorted order.

    Notes:
        - is it actually quadratic?

    :param a: leading coefficient
    :param b: linear coefficient
    :param c: absolute (constant) term
    :return: tuple of two (probably equal) roots of ax^2 + bx + c = 0 in sorted order, or None
    :raises RuntimeError: infinity solutions
    """

    raise NotImplementedError


@attr.s(slots=True, kw_only=True)
class Sphere(BaseObject):
    center: Vector = attr.ib()
    radius: float = attr.ib(converter=float)

    def intersect(self, ray: Ray) -> Intersection | None:
        """
        Intersect a sphere with a ray.

        Notes:
            - solve quadratic equation for a parameter
            - having found the roots, don't rush to return the intersection!
            - use get_normal() helper below
            - what if a ray was spawned right inside the sphere??

        :param ray: a ray to intersect a sphere with
        :return: intersection object, or None
        """

        raise NotImplementedError

    def get_normal(self, point: Vector) -> Vector:
        """
        Return outer normal to the surface at the given point.

        Notes:
            - while tracing a ray, it's not always that you need the outer normal, so be careful
            - do we really need to call .normalize() on a result, or it can be sped up significantly?

        :param point: a point on a surface
        :return: outer normal vector
        """

        raise NotImplementedError

    def has_volume(self) -> bool:
        return True
