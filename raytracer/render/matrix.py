import numpy as np

from ..geometry import Vector


class Matrix:
    def __init__(self, right: Vector, up: Vector, forward: Vector, from_: Vector):
        self._data = np.zeros((4, 4), dtype=float)
        self._data[0, :3] = right.to_array()
        self._data[1, :3] = up.to_array()
        self._data[2, :3] = forward.to_array()
        self._data[3, :3] = from_.to_array()
        self._data[3, 3] = 1

    def __getitem__(self, slice):
        return self._data[slice]


def look_at(look_from: Vector, look_to: Vector, eps: float = 1e-8) -> Matrix:
    """
    Build a 4x4 matrix for camera-to-world transformation given initial camera position and it's looking direction.

    Notes:
        - YES, you might need eps in case you didn't guess one of the vectors on the first try
        - NO, you don't have to overthink it, just implement as it is said in the lecture

    :param look_from: camera position
    :param look_to: looking direction
    :param eps: your holy EPS value
    :return: transformation (projection) matrix
    """

    raise NotImplementedError


def vector_matrix_multiply(matrix: Matrix, vector: Vector) -> Vector:
    return Vector.from_array(matrix[:3, :3].T @ vector.to_array())


def point_matrix_multiply(matrix: Matrix, point: Vector) -> Vector:
    result = vector_matrix_multiply(matrix, point)
    result += Vector.from_array(matrix[3, :3])
    depth = point.to_array() @ matrix[3, :3] + matrix[3, 3]
    return result / depth
