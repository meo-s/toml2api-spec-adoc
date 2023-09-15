from __future__ import absolute_import

import io
import pathlib
from typing import Any, Dict

from core.spring_rest_docs_api import SpringRestDocsApi


class AsciiDocBuilder:
  def __init__(self, api: SpringRestDocsApi, cfg):
    self._api = api
    self._cfg = cfg

  def _api_title(self, doc: io.TextIOWrapper):
    doc.write('= ' + self._cfg['api-name'] + '\n\n')

  def _api_description(self, doc: io.TextIOWrapper):
    if 'api-description' not in self._cfg:
      # TODO(meo-s): log missing api desripoin warning message
      return
    doc.write(self._cfg['api-description'] + '\n\n')

  def _api_case_request(self, doc: io.TextIOWrapper, cfg: Dict[str, str], snippets: Dict[str, str]):
    SNIPPETS = (('http-request', 'Sample'), ('request-headers', 'Headers'), ('query-parameters', 'Query Parameters'),
                ('request-fields', 'Fields'))

    cfg = cfg['request'] if 'request' in cfg else {}
    if 'emit' in cfg and cfg['emit']:
      return

    doc.write('=== Request\n\n')
    doc.write(cfg['description'] + '\n\n') if 'description' in cfg and cfg['description'] else None

    for snippet_name, snippet_title in SNIPPETS:
      if snippet_name in snippets:
        doc.write('==== ' + snippet_title + '\n\n')
        doc.write('include::' + snippets[snippet_name] + '[]\n\n')

  def _api_case_response(self, doc: io.TextIOWrapper, cfg: Dict[str, str], snippets: Dict[str, str]):
    SNIPPETS = (('http-response', 'Sample'), ('response-headers', 'Headers'), ('response-fields', 'Fields'))

    cfg = cfg['response'] if 'response' in cfg else {}
    if 'emit' in cfg and cfg['emit']:
      return

    doc.write('=== Response\n\n')
    doc.write(cfg['description'] + '\n\n') if 'description' in cfg and cfg['description'] else None

    for snippet_name, snippet_title in SNIPPETS:
      if snippet_name in snippets:
        doc.write('==== ' + snippet_title + '\n\n')
        doc.write('include::' + snippets[snippet_name] + '[]\n\n')

  def _api_case(self, doc: io.TextIOWrapper, cfg: Dict[str, str], snippets: Dict[str, str]):
    doc.write('== ' + cfg['alias'] + '\n\n')
    doc.write(cfg['description'] + '\n\n') if 'description' in cfg and cfg['description'] else None
    self._api_case_request(doc, cfg, snippets)
    self._api_case_response(doc, cfg, snippets)

  def _response(self, doc, api_case: Dict[Any, Any]):
    def sample():
      if 'http-response' in self._api.flows:
        doc.write('=== Sample\n\n')
        doc.write('include::' + self._api.flows['http-response'] + '[]\n\n')

    def headers():
      if 'response-headers' in self._api.flows:
        doc.write('=== Headers\n\n')
        doc.write('include::' + self._api.flows['response-headers'] + '[]\n\n')

    def fields():
      if 'response-fields' in self._api.flows:
        doc.write('=== Fields\n\n')
        doc.write('include::' + self._api.flows['response-fields'] + '[]\n\n')

    doc.write('== Response\n\n')
    sample()
    headers()
    fields()

  def build(self, output_dir: str | pathlib.Path):
    if not isinstance(output_dir, pathlib.Path):
      output_dir = pathlib.Path(output_dir)

    if not output_dir.exists():
      raise RuntimeError('')  # TODO(meo-s): write exception message

    if not output_dir.is_dir():
      raise RuntimeError('')  # TODO(meo-s): write exception message

    api_name: str = self._cfg['api-name']
    output_path = output_dir.joinpath(api_name.lower().replace(' ', '-') + '.adoc')

    with open(output_path, 'wt', encoding='utf-8') as doc:
      self._api_title(doc)
      self._api_description(doc)

      for api_case_cfg in sorted(self._cfg['api-cases'].values(), key=lambda v: v['priority']
                                 if 'priority' in v else 0):
        if 'emit' in api_case_cfg and api_case_cfg['emit']:
          continue
        self._api_case(doc, api_case_cfg, self._api.cases[api_case_cfg['name']])
