from unittest import TestCase
from unittest.mock import patch

from logging_decorator import TrackIt


class TestLoggerDecorator(TestCase):
    """
    Tests different functions decorated with the TrackIt decorator by mocking out either logging.info or logging.error.
    """
    @patch('logging.info')
    def test_greet__start_true_end_true(self, mock):
        @TrackIt(start=True, end=True)
        def greet(name):
            return 'Hi {name}'.format(name=name)

        greet('Jane')
        mock.assert_called_with('Called function greet with following return value: Hi Jane')

    @patch('logging.info')
    def test_greet__end_false(self, mock):
        @TrackIt(start=True, end=False)
        def greet(name):
            return 'Hi {name}'.format(name=name)

        greet('Jane')
        mock.assert_called_with("Calling function greet with following arguments: 'Jane'")

    @patch('logging.info')
    def test_greet__start_false(self, mock):
        @TrackIt(start=False, end=True)
        def greet(name):
            return 'Hi {name}'.format(name=name)

        greet('Jane')
        mock.assert_called_with('Called function greet with following return value: Hi Jane')

    @patch('logging.error')
    def test_add_two__error(self, mock):
        @TrackIt(start=True, end=False)
        def add_two(a, b):
            return a + b

        with self.assertRaises(TypeError):
            add_two(2, 'foo')
        mock.assert_called_with('Unsuccessfully called function: Exception was raised')

    @patch('logging.info')
    def test_add_two(self, mock):
        @TrackIt(start=True, end=False)
        def add_two(a, b):
            return a + b

        add_two(3, 2)
        mock.assert_called_with('Calling function add_two with following arguments: 3, 2')

    @patch('logging.error')
    def test_get_value_from_dict__error(self, mock):
        @TrackIt(start=False, end=False)
        def get_value_from_dict(dict, key):
            return dict[key]

        with self.assertRaises(KeyError):
            get_value_from_dict({}, 'foo')
        mock.assert_called_with('Unsuccessfully called function: Exception was raised')
