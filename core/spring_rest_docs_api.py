from __future__ import absolute_import

import pathlib
from typing import Dict, List, NamedTuple


class SpringRestDocsApi(NamedTuple):

  provider: str
  cases: Dict[str, Dict[str, str]]


class SpringRestDocsApiBuilder:

  def __init__(self, path: str | pathlib.Path):
    if not isinstance(path, pathlib.Path):
      path = pathlib.Path(path)

    self._path: pathlib.Path = path
    self._cases: Dict[str, Dict[str, str]] = {}

  def _add_case(self, current_path: pathlib.Path, snippet_paths: List[pathlib.Path]):
    snippets = {}

    for snippet_path in snippet_paths:
      assert snippet_path.name.endswith('.adoc')
      if 0 < snippet_path.stat().st_size:
        snippets[snippet_path.name[:-len('.adoc')]] = snippet_path.absolute().as_posix()

    self._cases[current_path.relative_to(self._path).as_posix()] = snippets

  def _find_cases(self, current_path: pathlib.Path):
    snippet_paths = []
    for item in current_path.iterdir():
      if not item.is_dir():
        if item.is_file() and item.name.endswith('.adoc'):
          snippet_paths.append(item)
        continue

      self._find_cases(item)

    if snippet_paths:
      self._add_case(current_path, snippet_paths)


  def build(self) -> SpringRestDocsApi:
    self._cases = {}
    self._find_cases(self._path)
    return SpringRestDocsApi(self._path.name, self._cases)

