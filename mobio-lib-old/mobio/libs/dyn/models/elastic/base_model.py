import os
from elasticsearch import Elasticsearch
from mobio.libs.Singleton import Singleton


@Singleton
class ElasticSearchBaseModel:
    __abstract__ = True
    _autoid = False
    # _doc_type = sys_conf.get_section_map('Elastic')['doc_type']
    # _index = sys_conf.get_section_map('Elastic')['index']
    if os.getenv('ELASTIC_SEARCH_7_HOST'):
        _hosts = os.getenv('ELASTIC_SEARCH_7_HOST').split(',')
    else:
        _hosts = os.getenv('ELASTIC_SEARCH_HOST').split(',')
    _port = os.getenv('ELASTIC_SEARCH_PORT')
    _es_user = os.getenv("ELASTIC_SEARCH_USER", "")
    _es_pass = os.getenv("ELASTIC_SEARCH_PASSWORD", "")
    if _es_user and _es_pass:
        _es = Elasticsearch(hosts=_hosts,
                            port=int(os.getenv('ELASTIC_SEARCH_PORT')),
                            http_auth=(_es_user, _es_pass)
                            )
    else:
        _es = Elasticsearch(hosts=_hosts,
                            port=int(os.getenv('ELASTIC_SEARCH_PORT')))

    def get_elasticsearch(self):
        return self._es

    # def get_index(self):
    #     return self._index
    #
    # def get_doc_type(self):
    #     return self._doc_type

    def get_hosts(self):
        return self._hosts

    def get_port(self):
        return self._port
