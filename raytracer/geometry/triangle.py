import attr
from typing import Any, Sequence

from .vector import Vector
from .base import BaseObject, Intersection, Ray


EPS = 1e-8


def get_triangle_area(v1: Vector, v2: Vector, v3: Vector) -> float:
    """
    Calculate the area of a triangle based on three given vertices.

    Notes:
        - use cross product

    :param v1: first vertex of a triangle
    :param v2: second vertex of a triangle
    :param v3: third vertex of a triangle
    :return: triangle area
    """

    raise NotImplementedError


@attr.s(slots=True, init=False)
class Triangle(BaseObject):
    _vertices: tuple[Vector] = attr.ib(converter=tuple)

    def __init__(self, vertices: Sequence[Vector], **kwargs: Any):
        if len(vertices) != 3:
            raise RuntimeError('Triangle has exactly three vertices most of the time.')
        super().__init__(**kwargs)
        self._vertices = tuple(vertices)

    @property
    def area(self) -> float:
        return get_triangle_area(*self._vertices)

    def __getitem__(self, idx: int) -> Vector:
        return self._vertices[idx]

    def intersect(self, ray: Ray) -> Intersection | None:
        """
        Intersect a ray with a triangle using Moller-Trumbore algorithm.

        Notes:
            - use as many dot and cross products as you need (we used 5 dots and 3 crosses)
            - don't forget to treat your EPS value properly! (thx GOD we have EPS)
            - you're likely to have to assign up to 15 variables
            - good luck! and have fun

        :param: ray: a ray to intersect a triangle with
        :return: intersection, or None
        """

        raise NotImplementedError

    def get_barycentric_coords(self, point: Vector) -> Vector:
        """
        Find barycentric coordinates of a point w.r.t. the current triangle.

        Notes:
            - use get_triangle_area (you'll have to find 4 areas, god damn)
            - you might not need these coordinates in your raytracer implementation
            - you could use these to interpolate vertex attributes, such as normals and colors, to render gradients

        :param point: a point for which coordinates are to be found
        :return: vector of barycentric coordinates
        """

        raise NotImplementedError

    def has_volume(self) -> bool:
        return False
