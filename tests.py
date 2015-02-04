import unittest
import rparse


class RParseTestCase(unittest.TestCase):

    def test_parse_loosy_requirement(self):
        requirements = "flask"
        package, version = next(rparse.parse(requirements))
        self.assertEqual(package, "flask")
        self.assertEqual(version, None)

    def test_parse_strict_requirement(self):
        requirements = "flask==0.10.1"
        package, version = next(rparse.parse(requirements))
        self.assertEqual(package, "flask")
        self.assertEqual(version, [("==", "0.10.1")])

    def test_parse_multiple_versions(self):
        requirements = "flask>=0.10.1, <0.11"
        package, version = next(rparse.parse(requirements))
        self.assertEqual(package, "flask")
        self.assertEqual(version, [(">=", "0.10.1"), ("<", "0.11")])

    def test_parse_requirements_with_comments(self):
        requirements = "flask==0.10.1 # latest version"
        package, version = next(rparse.parse(requirements))
        self.assertEqual(package, "flask")
        requirements = "flask # latest version"
        package, version = next(rparse.parse(requirements))
        self.assertEqual(package, "flask")
        self.assertEqual(version, None)
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
        package, version = next(ast)
        self.assertEqual(package, "redis")
        self.assertEqual(version, [("==", "1.0")])
        with self.assertRaises(ValueError, message="Invalid requirements line: 'flask=0.10.1'"):
            next(rparse.parse("flask=0.10.1"))
