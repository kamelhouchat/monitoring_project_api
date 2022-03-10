"""Service package"""


class DummyDetector:

    def __init__(self, *, task) -> None:
        self.task_name = task.name

    def launch(self):
        print(f'{self.task_name} launched successfully')
