"""Anomaly detector"""

from socket import timeout
from typing import Any
from typing import Dict
from typing import Generator

import pandas as pd
from opensearchpy.exceptions import AuthenticationException
from opensearchpy.exceptions import NotFoundError
from pandas import DataFrame

from monitoring_project_api.models.init_db_values import PROCESSING_METHODS
from .exceptions import InvalidDataSourceException
from .exceptions import InvalidWorkflowInputException
from .exceptions import NoProcessingMethodFoundException
from .experta import ExpertSystem
from .method_base import DetectionMethod
from .opensearch import build_os_connection
from ..models import Data
from ..models import Task


class Detector:
    """
    Class which allows to generate all the processing methods (by selecting
    the right parameters) and to launch them.
    """
    # Typing
    task: Task
    target_data: Data
    target_data_dataframe: DataFrame
    _workflow: Dict[Any, Any]

    def __init__(self, *, task: Task) -> None:
        """
        Class initializer
        :param task: The task on which the detection will be launched
        :type task: Task
        """
        # Init task
        self.task = task

        # Get target data
        self.target_data = task.target_data

        # Init dataframe
        self.target_data_dataframe = self._get_data()

        # Init an empty workflow
        self._workflow = {}

        # Init an Expert Sys
        expert_sys = ExpertSystem(detector=self)

        # Start the expert system on the current task (Note that the Expert Sys
        # modifies directly the attribute `workflow` of the current object)
        expert_sys.reset(task=self.task)
        expert_sys.run()

    @property
    def workflow(self) -> dict:
        """
        The getter of the attribute `_workflow`.
        :return: The attribute `_workflow`
        :rtype: dict
        """
        return self._workflow

    @workflow.setter
    def workflow(self, item: tuple) -> None:
        """
        The setter of the attribute `_workflow`
        :param item: A tuple which must contain the new processing method name
        (ACCEPTED_URLS_METHOD...) and a dictionary of its parameters.
        :type item: tuple
        :raise InvalidWorkflowInputException: The exception is thrown if the
        processing method is not implemented.
        """
        # Validate item type
        if not isinstance(item, tuple):
            raise InvalidWorkflowInputException(item, message='The workflow '
                                                              'item must be '
                                                              'of type '
                                                              '`tuple`')

        # Unpack a tuple
        try:
            processing_method_name, parameters = item
        except ValueError as e:
            raise InvalidWorkflowInputException(item) from e

        # Validate the new processing method
        if processing_method_name not in PROCESSING_METHODS:
            raise InvalidWorkflowInputException(item)

        # Update `workflow` dictionary
        if processing_method_name not in self.workflow:
            self.workflow[processing_method_name] = {}

        self.workflow[processing_method_name].update(parameters)

    def launch(self):
        """
        It is the main method, it allows to launch the processing. First,
        the method calls `_construct_pipeline` to construct a pipeline using
        the data provided by the expert system, then, the pipeline is
        launched and the processing results are sent to` destination_id`.
        """
        # Get detector and launch it
        processors: Generator[DetectionMethod] = self._get_detectors()

        for processor in processors:
            processor.launch()

    def _get_data(self) -> DataFrame:
        """
        Method which allows to retrieve the input data from the endpoint
        `opensearch`, the data is then saved in a temporary directory, read and
        returned as dataframe.
        :return: The input data as a dataframe
        :rtype: pd.Dataframe
        """
        # Get target data args
        target_data_args = Data.get(self.target_data.id, as_dict=True)

        # Build client
        client = build_os_connection(target_data_args=target_data_args)

        # Get indice
        indice = target_data_args['indice']

        # Build query
        query = {
            'size': 200,
            'query': {
                'match_all': {}
            }
        }
        # Make an HTTP request to get the dataframe
        try:
            response = client.search(body=query, index=indice)
        except timeout as e:
            raise InvalidDataSourceException('Invalid OpenSearch URL') from e
        except AuthenticationException as e:
            raise InvalidDataSourceException('Invalid OpenSearch user name '
                                             'or password') from e
        except NotFoundError as e:
            raise InvalidDataSourceException('Invalid data indice') \
                from e

        # Get items
        items = [item['_source'] for item in response.pop('hits')['hits']]

        # Return dataframe
        dataframe = pd.DataFrame(items)
        dataframe['@timestamp'] = pd.to_datetime(dataframe['@timestamp'])
        dataframe.rename(columns={'@timestamp': 'timestamp'}, inplace=True)
        return dataframe

    def _get_detectors(self) -> Generator:
        """
        Private method which allows to build an adapted pipeline using the
        decisions taken by the expert system.
        :return: The pipeline which contains all the processing methods.
        :rtype: Generator
        """
        # At least one processing method must be in the workflow.
        if not self.workflow:
            raise NoProcessingMethodFoundException

        import logging

        for processing_method, params in self.workflow.items():
            yield PROCESSING_METHODS[processing_method](
                dataframe=self.target_data_dataframe,
                logger=logging.getLogger(f'{self.task.id}_'
                                         f'{processing_method}'),
                **params
            )
