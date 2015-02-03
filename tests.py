import unittest
import rparse


class RParseTestCase(unittest.TestCase):

    def test_parse_loosy_requirement(self):
        requirements = "flask"
        ast = next(rparse.parse(requirements))
        self.assertEqual(list(ast.select("package > name *")), ["flask"])

    def test_parse_strict_requirement(self):
        requirements = "flask==0.10.1"
        ast = next(rparse.parse(requirements))
        self.assertEqual(list(ast.select("package > name *")), ["flask"])
        self.assertEqual(list(ast.select("package > vspec > comparison *")), ["=="])
        self.assertEqual(list(ast.select("package > vspec > version *")), ["0.10.1"])

    def test_parse_multiple_versions(self):
        requirements = "flask>=0.10.1, <0.11"
        ast = next(rparse.parse(requirements))
        self.assertEqual(list(ast.select("package > name *")), ["flask"])
        self.assertEqual(list(ast.select("package > vspec > comparison *")), [">=", "<"])
        self.assertEqual(list(ast.select("package > vspec > version *")), ["0.10.1", "0.11"])

    def test_parse_invalid_requirements(self):
        requirements = """
        flask 0.10.1
        redis==1.0
        """
        ast = rparse.parse(requirements)
        with self.assertRaises(ValueError, message="Invalid requirements line: 'flask 0.10.1'"):
            next(ast)
        ast = next(ast)
        self.assertEqual(list(ast.select("package > name *")), ["redis"])
        self.assertEqual(list(ast.select("package > vspec > comparison *")), ["=="])
        self.assertEqual(list(ast.select("package > vspec > version *")), ["1.0"])
