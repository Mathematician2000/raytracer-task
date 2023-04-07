import math
import numpy as np
import operator


class Vector:
    def __init__(self, x: float = 0, y: float | None = None, z: float | None = None, /):
        if y is None:
            y = z = x
        assert z is not None, "You should specify either 1 or all 3 vector coordinates"
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    @classmethod
    def from_array(cls, arr) -> "Vector":
        return cls(*arr)

    def __repr__(self) -> str:
        return f"Vector({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def __getitem__(self, idx: int) -> float:
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        elif idx == 2:
            return self.z
        raise IndexError(f"index {idx} not found")

    @property
    def length(self) -> float:
        """
        Find length of a vector.

        :return: vector length (L2 norm)
        """

        raise NotImplementedError

    def normalize(self) -> "Vector":
        """
        Normalize vector, so that it has length 1.

        :return: self
        """

        raise NotImplementedError

    def dot(self, other: "Vector") -> float:
        """
        Calculate dot product of two vectors.

        :param other: right-hand side operand
        :return: dot product
        """

        raise NotImplementedError

    def cross(self, other: "Vector") -> "Vector":
        """
        Calculate cross product of two vectors.

        :param other: right-hand side operand
        :return: cross product
        """

        raise NotImplementedError

    def __add__(self, other: "Vector") -> "Vector":
        """
        Calculate sum of two vectors (aka operator+).

        :param other: right-hand side operand
        :return: new vector
        """

        raise NotImplementedError

    def __iadd__(self, other: "Vector") -> "Vector":
        """
        Calculate sum of two vectors in-place (aka operator+=).

        :param other: right-hand side operand
        :return: self
        """

        raise NotImplementedError

    def __sub__(self, other: "Vector") -> "Vector":
        """
        Calculate difference of two vectors (aka operator-).

        :param other: right-hand side operand
        :return: new vector
        """

        raise NotImplementedError

    def __isub__(self, other: "Vector") -> "Vector":
        """
        Calculate difference of two vectors in-place (aka operator-=).

        :param other: right-hand side operand
        :return: self
        """

        raise NotImplementedError

    def __neg__(self) -> "Vector":
        """
        Negate the vector (aka unary operator-).

        :return: new vector
        """

        raise NotImplementedError

    def __mul__(self, other: float) -> "Vector":
        """
        Calculate product of a vector and a real number (aka operator*).

        :param other: right-hand side operand (number)
        :return: new vector
        """

        raise NotImplementedError

    def __rmul__(self, other: float) -> "Vector":
        """
        Calculate product of a vector and a real number (aka operator*).

        :param other: left-hand side operand (number)
        :return: new vector
        """

        raise NotImplementedError

    def __imul__(self, other: float) -> "Vector":
        """
        Calculate product of a vector and a real number in-place (aka operator*=).

        :param other: left-hand side operand (number)
        :return: self
        """

        raise NotImplementedError

    def hadamard(self, other: "Vector") -> "Vector":
        """
        Calculate Hadamard (element-wise) product of two vectors.

        :param other: right-hand side operand (vector)
        :return: new vector
        """

        raise NotImplementedError

    def __truediv__(self, other: float) -> "Vector":
        """
        Calculate ratio of a vector and a real number (aka operator/).

        :param other: right-hand side operand (number)
        :return: new vector
        """

        raise NotImplementedError

    def __itruediv__(self, other: float) -> "Vector":
        """
        Calculate ratio of a vector and a real number in-place (aka operator/=).

        :param other: right-hand side operand (number)
        :return: self
        """

        raise NotImplementedError

    def to_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def to_array(self):
        return np.array(self.to_tuple(), dtype=float)

    def __eq__(self, other: "Vector") -> bool:
        return np.allclose(self.to_tuple(), other.to_tuple())
