"""OpenSearch handler"""

from opensearchpy import OpenSearch

from .utils import retry


@retry(Exception, tries=6, delay=10)
def build_os_connection(*, target_data_args: dict) -> OpenSearch:
    """
    Function that allows to generate a client according to the target data
    :param target_data_args: dictionary that contains the target data args
    :type target_data_args: dict
    :return: OpenSearch
    """
    os_kwargs = {}

    # Enable authentication if there is a password.
    if (
            target_data_args['auth_user_name'] and
            target_data_args['auth_password']
    ):
        os_kwargs['http_auth'] = (
            target_data_args['auth_user_name'],
            target_data_args['auth_password']
        )

    return OpenSearch(
        hosts=[
            {
                'host': target_data_args['os_host'],
                'port': target_data_args['os_port']
            }
        ],
        http_compress=True,  # enables gzip compression for request bodies
        verify_certs=False,
        use_ssl=target_data_args['is_using_ssl'],
        **os_kwargs
    )
