from tablassert.ingests import from_yaml
from tablassert.ingests import fastmerge
from tablassert.enums import Qualifiers
from tablassert.models import Section
from functools import lru_cache
from functools import cache
from fastmcp import FastMCP
from typing import Union
from typing import Any
import trafilatura
import requests
import shutil
import json
import yaml
import gzip

MCP: object = FastMCP(
  name="QualifiersMCP",
  version="1.0.0",
  instructions="MCP that adds qualifiers to Tablassert Table Configuration"
)

@MCP.tool
@lru_cache(maxsize=24)
def get_biolink_qualifier_documentation(qualifier: str) -> str:
  url: str = f"https://raw.githubusercontent.com/biolink/biolink-model/gh-pages/{qualifier}/index.html"
  response: object = requests.get(url, timeout=30)
  html: str = response.text
  return trafilatura.extract(html, output_format="markdown", include_tables=True, include_links=True, include_images=False, no_fallback=False) or "ERROR 01: Invalid Qualifier"

@MCP.tool
@cache
def get_table_configuration_documentation() -> str:
  url: str = "https://raw.githubusercontent.com/SkyeAv/Tablassert/main/docs/configuration/table.md"
  response: object = requests.get(url, timeout=30)
  return response.text

@MCP.tool
@cache
def get_table_configuration_model_schema() -> str:
  return Section.model_json_schema()

@MCP.tool
@cache
def get_biolink_qualifier_list() -> str:
  return "\n".join(q.value for q in Qualifiers)

@MCP.tool
def read_yaml_to_sections_json(file_path: str) -> list[dict[str, Any]]:
  serialized_object: object = from_yaml(file_path)
  sections: Any = fastmerge(serialized_object)
  return sections

@MCP.tool
def write_json_table_configuration_to_yaml(json_configuration: str, file_path: str) -> None:
  serialized_object: object = json.loads(json_configuration)
  with open(file_path, "w") as f:
    yaml.safe_dump(serialized_object, f)

@MCP.tool
def validate_json_table_configuration_syntax(json_configuration: str) -> dict[str, Any]:
  serialized_object: object = json.loads(json_configuration)
  sections: Any = fastmerge(serialized_object)
  try:
    for s in sections:
      Section.model_validate(s)
    return {"ok": 200}
  except Exception as e:
    msg: dict[str, str] = {"error": str(e)}
    return msg

@MCP.tool
def download_pmc_file_from_local_mirror(pmc_id: str, file_name: str, download_root: str = "/15TB_1/users/gglusman/PMC/tars") -> str:
  if "PMC" not in pmc_id:
    pmc_id = f"PMC{pmc_id}"

  url: str = f"http://localhost:8051/extract-from-tar?filename={pmc_id}/{file_name}&tarpath={download_root}/{pmc_id[-3:]}/{pmc_id}.tar.xz"
  try:
    with requests.get(url, stream=True) as r:
      r.raise_for_status()
      with open(file_name, 'wb') as f:
        with gzip.GzipFile(fileobj=r.raw) as decompressed:
          shutil.copyfileobj(decompressed, f)
    msg: dict[str, str] = {"ok": file_name}
    return json.dumps(msg)
  except Exception as e:
    msg = {"error": str(e)}
    return json.dumps(msg)

@MCP.tool
def get_curies_entitry_from_dbssert_ner(entity: str) -> Union[str, dict[str, Any]]:
  url: str = f"http://localhost:8052/curies-with-ner?entity={entity}"
  try:
    with requests.get(url, stream=True) as r:
      r.raise_for_status()
      return r.text
  except Exception as e:
    msg = {"error": str(e)}
    return msg

@MCP.tool
def get_cannonical_curie_information_from_dbssert(curie: str) -> Union[str, dict[str, Any]]:
  url: str = f"http://localhost:8052/cannoical-curie-information?curie={curie}"
  try:
    with requests.get(url, stream=True) as r:
      r.raise_for_status()
      return r.text
  except Exception as e:
    msg = {"error": str(e)}
    return msg
