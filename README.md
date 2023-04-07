Raytracer implementation in Python

## Task details
Your task is to implement your own raytracer in Python following the guides in this template project.

You need to fill in the gaps in the following files:
- `geometry`:
    + `vector.py`: all basic operations on Vector instances
    + `ray.py`: reflection and refraction of rays
    + `sphere.py`: quadratic equations, normals to the sphers surface, and ray-sphere intersection
    + `triangle.py`: triangle area, Moller-Trumbore algorithm of ray-triangle intersection, and barycentric coordinates
- `render`:
    + `matrix.py`: camera-to-world projection matrix
    + `scene.py`: raytracer implementation, namely:
        - `find_closest_intersection`: find intersection of a ray with the first object in the scene
        - `is_point_illuminated`: check if a point is illuminated by a point light source
        - `get_intensity`: calculate total light intensity at the given point
        - `trace_ray`: trace a ray recursively over the scene, reflecting and refracting it when necessary
        - `tone_mapping`: implement tone mapping postprocessing algorithm in-place
        - `gamma_correction`: implement gamma correction postprocessing algorithm in-place

Don't forget to run `pytest` tests in `geometry` and `render` folders to check your implementation!

Sources:
- [Raytracer sketch](https://cseweb.ucsd.edu/~alchern/teaching/cse167_fa21/7-1RayTracing.pdf)
- [Generating camera rays](https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-generating-camera-rays/generating-camera-rays.html)
- [Moller-Trumbore algorithm](https://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm)
- [Bounded Volume Hierarchy](http://15462.courses.cs.cmu.edu/fall2019content/lectures/15_spatialdatastructures/15_spatialdatastructures_slides.pdf)

Good luck!
