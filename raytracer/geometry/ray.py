import attr
import math

from .vector import Vector


@attr.s(slots=True, kw_only=True)
class Ray:
    origin: Vector = attr.ib()
    direction: Vector = attr.ib()

    def __attrs_post_init__(self):
        self.direction.normalize()


def reflect(direction: Vector, normal: Vector) -> Vector:
    """
    Reflect a ray with the given direction w.r.t. the given normal to the surface.

    Notes:
        - use dot product

    :param direction: falling ray direction
    :param normal: normal to the surface
    :return: direction of the reflected ray
    """

    raise NotImplementedError


def refract(direction: Vector, normal: Vector, eta: float) -> Vector | None:
    """
    Refract a ray with the given direction w.r.t. the given normal to the surface.

    Notes:
        - use dot product once again
        - don't forget the case of total internal reflection!

    :param direction: falling ray direction
    :param normal: normal to the surface
    :param eta: ratio of refraction indices of two environments, with the initial eta in the numerator
    :return: direction of the refracted ray, or None
    """

    raise NotImplementedError
