from unittest import TestCase
from src.application import load_data_from_json, Application


class TestApplication(TestCase):
    def setUp(self) -> None:
        self.path = 'test_user.json'

    def test_load_json(self):
        data = load_data_from_json(self.path)

        expected_data = [Application.User(name="Adam", department="Marketing", birth="01.05.1980", salary=85000, role="1")]

