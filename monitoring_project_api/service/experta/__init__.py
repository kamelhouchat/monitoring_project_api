"""Experta (Expert system manager)"""

from typing import Generator
from typing import Optional
from typing import TYPE_CHECKING

from experta import *

from monitoring_project_api.models import Task
from .facts import NotRequiredProperty
from .selecting_method import SelectingMethodRules
from .stats import StatisticProcessingRules

if TYPE_CHECKING:
    from .. import Detector


class ExpertSystem(KnowledgeEngine,
                   SelectingMethodRules,
                   StatisticProcessingRules):
    """
    Class which allows the expert system to be initialized by retrieving all
    the task properties. The class allows applying rules in order to choose
    the appropriate processing methods and their hyper-parameters according
    to the context.
    """
    # Typing
    not_required_properties: Optional[dict]
    detector: 'Detector'
    task: Optional[Task]

    def __init__(self, *, detector) -> None:
        """
        Class Initializer
        :param detector: The detector that process the current task
        :type detector: Detector
        """
        # Init not required properties
        self.not_required_properties = None

        # Init detector
        self.detector = detector

        # Init task attribute
        self.task = None
        super().__init__()

    @DefFacts()
    def init(self, task: Task) -> Generator:
        """
        Method which allows to initialize the expert system with a set of
        facts.
        More precisely:
           - Not required properties: black_list, accepted_urls
        :param task: The task on which the detection will be launched
        :type task: Task
        """
        # Save the task in an attribute
        self.task = task

        # Init not required properties
        self.not_required_properties = task.properties
        for task_property in self.not_required_properties.keys():
            yield NotRequiredProperty(property_name=task_property)
