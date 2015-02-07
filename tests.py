import unittest
import rparse


class RParseTestCase(unittest.TestCase):

    def test_parse_loosy_requirement(self):
        requirements = "flask"
        package = next(rparse.parse(requirements))
        self.assertEqual(package.name, "flask")
        self.assertEqual(package.specs, None)

    def test_parse_strict_requirement(self):
        requirements = "flask==0.10.1"
        package = next(rparse.parse(requirements))
        self.assertEqual(package.name, "flask")
        self.assertEqual(package.specs, [("==", "0.10.1")])

    def test_parse_extra_requirements(self):
        requirements = "raven[foo, bar]==0.10.1"
        package = next(rparse.parse(requirements))
        self.assertEqual(package.name, "raven")
        self.assertEqual(package.specs, [("==", "0.10.1")])
        self.assertEqual(package.extras, ["foo", "bar"])

    def test_parse_multiple_versions(self):
        requirements = "flask>=0.10.1, <0.11"
        package = next(rparse.parse(requirements))
        self.assertEqual(package.name, "flask")
        self.assertEqual(package.specs, [(">=", "0.10.1"), ("<", "0.11")])

    def test_parse_requirements_with_comments(self):
        requirements = "flask==0.10.1 # latest version"
        package = next(rparse.parse(requirements))
        self.assertEqual(package.name, "flask")
        requirements = "flask # latest version"
        package = next(rparse.parse(requirements))
        self.assertEqual(package.name, "flask")
        self.assertEqual(package.specs, None)
        with self.assertRaises(StopIteration):
            next(rparse.parse("# comment"))

    def test_parse_invalid_requirements(self):
        requirements = """
        flask 0.10.1
        redis==1.0
        """
        ast = rparse.parse(requirements)
        with self.assertRaises(ValueError, message="Invalid requirements line: 'flask 0.10.1'"):
            next(ast)
        package = next(ast)
        self.assertEqual(package.name, "redis")
        self.assertEqual(package.specs, [("==", "1.0")])
        with self.assertRaises(ValueError, message="Invalid requirements line: 'flask=0.10.1'"):
            next(rparse.parse("flask=0.10.1"))
