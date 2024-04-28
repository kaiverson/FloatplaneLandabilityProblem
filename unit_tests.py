"""
unit test to test some work pat did
-pat
"""
from toolbox.polygons import *
import os

def test_is_point_in_polygon():
    """
    Unit test for "is_point_in_polygon"
    Returns:

    """
    verbose = os.getenv("VERBOSE") == '1'

    vertices = [
        (0, 0), (1, 0), (1, 1), (0, 1)
    ]

    test_point_inside = (0.5, 0.5)
    test_point_outside = (1.5, 1.5)
    test_point_on_border = (0, 0.5)
    test_points = [test_point_inside, test_point_outside, test_point_on_border]

    results = [is_point_in_polygon(vertices, p) for p in test_points]
    desired_results = [True, False, False]

    for result, desired_result, test_point in zip(results, desired_results, test_points):
        test = result == desired_result
        test_string = f"""Looking at point {test_point} and the polygon defined by
{str(vertices)}
the point {test_point} lies {"inside" if result else "outside"}
the desired result was {"inside" if desired_result else "outside"}
"""
        if verbose:
            print(test_string)
        assert test



