from unittest import TestCase


class TestEnviron(TestCase):

    def setUp(self) -> None:
        pass

    def test_get_env(self):
        """
        Test that the get_env function returns the correct value
        """
        from get_envrion import get_env

        result = str(get_env('VERSION'))
        print(result)
        self.assertEqual(result, '1.0.0')
