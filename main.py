from __future__ import absolute_import

import sys
import pathlib
import toml
from argparse import ArgumentParser
from collections import namedtuple
from typing import List

import core
from core.spring_rest_docs_api import SpringRestDocsApi


def load_cfg(cfg_dir: str | pathlib.Path):

  if not isinstance(cfg_dir, pathlib.Path):
    cfg_dir = pathlib.Path(cfg_dir)

  if not cfg_dir.exists():
    print('Doc path not found: ' + cfg_dir.absolute().as_posix())
    sys.exit(-1)

  cfg = {}
  for cfg_path in cfg_dir.iterdir():
    if not cfg_path.is_file() or not cfg_path.name.endswith('.toml'):
      continue

    piece = toml.load(cfg_path)
    for api_provider in piece.keys():
      piece[api_provider]['api-cases'] = dict([[case['name'], case] for case in piece[api_provider]['api-cases']])
      cfg[api_provider] = piece[api_provider]

  return cfg


def glob_apis(collection_path: str | pathlib.Path) -> List[SpringRestDocsApi]:

  if not isinstance(collection_path, pathlib.Path):
    collection_path = pathlib.Path(collection_path)

  collection_path: pathlib.Path = pathlib.Path(collection_path)
  if not collection_path.exists():
    print('Directory not found: ' + collection_path.absolute().as_posix())
    sys.exit(-1)

  return [api for path in collection_path.iterdir() if (api := core.SpringRestDocsApiBuilder(path).build()) is not None]


def main(apis_path: str, cfg_dir: str | None, output_dir: str):

  output_dir: pathlib.Path = pathlib.Path(output_dir)
  output_dir.mkdir(parents=True, exist_ok=True)

  cfg, apis = load_cfg(cfg_dir) if cfg_dir else {}, glob_apis(apis_path)

  for api in apis:
    if api.provider not in cfg:
      print('undefined api: ' + api.provider)  # TODO(meo-s): use log library
      continue

    core.AsciiDocBuilder(api, cfg[api.provider]).build(output_dir)


if __name__ == '__main__':
  arg_parser = ArgumentParser()

  arg = arg_parser.add_argument
  arg('--cfg', '-c', dest='cfg_dir', type=str, default=None)
  arg('--apis', dest='apis_path', type=str, required=True)
  arg('--output_dir', '-o', type=str, required=True)

  sys.exit(main(**dict(vars(arg_parser.parse_args()))))
