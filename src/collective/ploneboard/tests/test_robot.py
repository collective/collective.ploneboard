from collective.ploneboard.testing import COLLECTIVE_PLONEBOARD_FUNCTIONAL_TESTING
from plone.testing import layered
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("robot_hello.txt"),
                layer=COLLECTIVE_PLONEBOARD_FUNCTIONAL_TESTING)
    ])
    return suite
