import attr
import math
import numpy as np
import tqdm
import multiprocessing

from PIL import Image

from ..geometry import BaseObject, Intersection, Ray, Vector, reflect, refract
from .matrix import look_at, point_matrix_multiply, vector_matrix_multiply


EPS = 1e-8
NONE_VECTOR = Vector(-3.14)
NONE_ARRAY = NONE_VECTOR.to_array()


@attr.s(slots=True, kw_only=True)
class PointLight:
    origin: Vector = attr.ib()
    intensity: Vector = attr.ib()


@attr.s(slots=True, kw_only=True)
class CameraOptions:
    screen_width: float = attr.ib()
    screen_height: float = attr.ib()
    fov: float = attr.ib(default=math.pi / 2)
    look_from: Vector = attr.ib(factory=Vector)
    look_to: Vector = attr.ib()

    @look_to.default
    def _(self) -> Vector:
        return Vector(0, 0, -1)


@attr.s(slots=True, kw_only=True)
class Scene:
    objects: list[BaseObject] = attr.ib(factory=list, init=False)
    lights: list[PointLight] = attr.ib(factory=list, init=False)

    _cached_last_intersected: BaseObject | None = attr.ib(default=None, init=False)

    def add_object(self, obj: BaseObject) -> None:
        self.objects.append(obj)

    def add_light(self, light: PointLight) -> None:
        self.lights.append(light)

    def find_closest_intersection(self, ray: Ray) -> tuple[Intersection | None, BaseObject | None]:
        """
        Find intersection of a ray with the first object in the scene.

        Notes:
            - implementation is straight-forward
            - you need the closest intersection!

        :param ray: a ray to intersect with objects
        :return: tuple of found intersection and an object, or two Nones
        """

        raise NotImplementedError

    def is_point_illuminated(self, point: Vector, light_dir: Vector) -> bool:
        """
        Check if a point is illuminated by a point light source.

        Notes:
            - yes, you have to iterate over objects once again
            - intersect all the objects with the ray starting at the point
            - return True immediately on having found any intersection
            - don't forget to check that an intersection lies *between* a point and a light source!
            - use shadow consistency trick to cache the last intersecting object and speed up computation

        :param point: a point to check
        :param light_dir: a difference vector pointing at the light source
        :return: True, if point is illuminated, or False otherwise
        """

        raise NotImplementedError

    def get_intensity(
        self,
        ray: Ray,
        intersection: Intersection,
        obj: BaseObject,
        *,
        inside: bool = False,
        eps: float = EPS,
    ) -> Vector:
        """
        Calculate total light intensity at the given point.

        Notes:
            - add ambient color of a material right from the very start
            - consider diffuse and specular components when tracing outside of an object and only if material.albedo.x is > EPS
            - iterate over light sources and check if they illuminate the intersection point
            - don't forget to make an EPS step along the normal while checking for an illimunation!
            - use Vector.hadamard and operator* wisely

        :param ray: a ray intersection with a scene object
        :param intersection: corresponding intersection instance
        :param obj: corresponding scene object
        :param inside: True, if a ray is inside an object with a volume
        :param eps: your god damn EPS
        :return: an RGB-vector of light intensity with each component normalized to [0; 1]
        """

        raise NotImplementedError

    def trace_ray(self, ray: Ray, *, depth: float, inside: bool = False, eps: float = EPS) -> Vector | None:
        """
        Trace a ray recursively over the scene, reflecting and refracting it when necessary.

        Notes:
            - find closest intersection with a scene, return None if there's no intersection
            - get light intensity at the intersection point
            - if depth > 1, trace reflected and refracted rays (if exist)
            - make a step of length EPS along the normal while reflecting or refracting a ray
            - don't forget to consider material.albedo while adding reflected and refracted light
            - replace material.albedo.z with 1 when inside a scene object with a volume

        :param ray: a ray to trace
        :param depth: max recusrion depth (should be positive)
        :param inside: True, if a ray is inside an object with a volume
        :param eps: your god damn EPS
        :return: light intensity Nector, or None (if a ray is cast outside the scene)
        """

        raise NotImplementedError

    def tone_mapping(self, pixels, background_color: Vector, *, eps: float = EPS) -> None:
        """
        Implement tone mapping postprocessing algorithm in-place.

        Notes:
            - use vectorized numpy operations for efficiency (max, broadcast_to, isclose, where, binary operations)
            - don't forget to replace None values (NONE_ARRAY) with background_color vector!

        :param pixels: array of shape (height, width, 3)
        :param background_color: background color intensity Vector
        :param eps: your god damn EPS
        :return: None
        """

        raise NotImplementedError

    def gamma_correction(self, pixels, *, gamma: float = 2.2, eps: float = EPS) -> None:
        """
        Implement gamma correction postprocessing algorithm in-place.

        Notes:
            - ignore a whole black square (when max is < EPS)

        :param pixels: array of shape (height, width, 3)
        :param gamma: gamma exponent value
        :param eps: your god damn EPS
        :return: None
        """

        raise NotImplementedError

    def postprocess(
        self,
        pixels,
        background_color: Vector,
        *,
        gamma: float = 2.2,
        eps: float = EPS,
    ) -> None:
        self.tone_mapping(pixels, background_color, eps=eps)
        self.gamma_correction(pixels, gamma=gamma, eps=eps)

    def render(
        self,
        cam_options: CameraOptions,
        *,
        background_color: Vector | None = None,
        depth: float = 3,
        verbose: bool = True,
        eps: float = EPS,
        parallel: bool = False,
        num_workers: int | None = None,
    ) -> Image.Image:
        if background_color is None:
            background_color = Vector(0, 0, 0)

        global _RENDER_SETTINGS, _SCENE
        _SCENE = self
        _RENDER_SETTINGS = RenderSettings(cam_options, eps, depth)
        width, height = _RENDER_SETTINGS.width, _RENDER_SETTINGS.height

        pixels = np.empty((height, width, 3), dtype=float)
        if parallel:
            results = []
            num_workers = num_workers or multiprocessing.cpu_count() - 1
            with multiprocessing.Pool(num_workers) as pool:
                for j in tqdm.tqdm(range(height), desc="Pool preparation", disable=not verbose):
                    results.append(pool.apply_async(_process_line, (j,)))

                for res in tqdm.tqdm(results, total=len(results), desc="Ray tracing", disable=not verbose):
                    j, line = res.get()
                    pixels[j] = line
        else:
            for j in tqdm.tqdm(range(height), desc="Ray tracing", disable=not verbose):
                pixels[j] = _process_line(j)[-1]

        self.postprocess(pixels, background_color, eps=eps)

        img = Image.fromarray(np.uint8(np.clip(0, 255, 256 * pixels)))
        return img


_SCENE: 'Scene' = None                     # type: ignore
_RENDER_SETTINGS: 'RenderSettings' = None  # type: ignore


@attr.s(slots=True)
class RenderSettings:
    cam_options: CameraOptions = attr.ib()
    eps: float = attr.ib()
    depth = attr.ib()

    width = attr.ib(default=None)
    height = attr.ib(default=None)
    aspect_ratio = attr.ib(default=None)
    scale = attr.ib(default=None)
    cam_to_world = attr.ib(default=None)
    origin = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.width = self.cam_options.screen_width
        self.height = self.cam_options.screen_height

        self.scale = math.tan(self.cam_options.fov / 2)
        self.aspect_ratio = self.width / self.height
        self.cam_to_world = look_at(self.cam_options.look_from, self.cam_options.look_to, eps=self.eps)
        self.origin = point_matrix_multiply(self.cam_to_world, Vector())


def _process_line(j):
    line = np.empty((_RENDER_SETTINGS.width, 3), dtype=float)
    for i in range(_RENDER_SETTINGS.width):
        line[i] = _process_pixel(i, j)

    return j, line


def _process_pixel(i, j):
    x = (2 * (i + 0.5) / _RENDER_SETTINGS.width - 1) * _RENDER_SETTINGS.aspect_ratio * _RENDER_SETTINGS.scale
    y = (1 - 2 * (j + 0.5) / _RENDER_SETTINGS.height) * _RENDER_SETTINGS.scale
    direction = vector_matrix_multiply(_RENDER_SETTINGS.cam_to_world, Vector(x, y, -1))
    ray = Ray(origin=_RENDER_SETTINGS.origin, direction=direction)

    pixel = _SCENE.trace_ray(ray, depth=_RENDER_SETTINGS.depth, eps=_RENDER_SETTINGS.eps)
    if pixel is None:
        pixel = NONE_VECTOR

    return pixel.to_array()
