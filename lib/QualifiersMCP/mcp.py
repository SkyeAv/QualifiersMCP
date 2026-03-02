from tablassert.ingests import from_yaml
from tablassert.ingests import fastmerge
from tablassert.enums import Qualifiers
from tablassert.models import Section
from functools import lru_cache
from functools import cache
from fastmcp import FastMCP
from typing import Union
from typing import Annotated
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
  instructions="QualifiersMCP provides tools for working with Biolink qualifiers in Tablassert Table Configuration. Tablassert is a system for managing and validating tabular data with structured metadata. Biolink qualifiers add semantic meaning to biological relationships by providing additional context such as negation, subject/object constraints, and other modalities. This MCP server offers three tool groups: biolink tools for fetching Biolink documentation and qualifier lists, table-config tools for managing Tablassert configurations including YAML conversion and validation, and local-services tools that depend on external services running on localhost (port 8051 for PMC mirror, port 8052 for dbssert)."
)


@lru_cache(maxsize=24)
def _get_biolink_qualifier_documentation_cached(qualifier: str) -> str:
  url: str = f"https://raw.githubusercontent.com/biolink/biolink-model/gh-pages/{qualifier}/index.html"
  response: object = requests.get(url, timeout=30)
  html: str = response.text
  return trafilatura.extract(html, output_format="markdown", include_tables=True, include_links=True, include_images=False, no_fallback=False) or "ERROR 01: Invalid Qualifier"


@cache
def _get_table_configuration_documentation_cached() -> str:
  url: str = "https://raw.githubusercontent.com/SkyeAv/Tablassert/main/docs/configuration/table.md"
  response: object = requests.get(url, timeout=30)
  return response.text


@cache
def _get_table_configuration_model_schema_cached() -> str:
  return Section.model_json_schema()


@cache
def _get_biolink_qualifier_list_cached() -> str:
  return "\n".join(q.value for q in Qualifiers)

@MCP.tool(tags={"biolink"})
def get_biolink_qualifier_documentation(qualifier: Annotated[str, "The Biolink qualifier to fetch documentation for (e.g., 'negation', 'object', 'subject')."]) -> str:
  """Fetches Biolink qualifier documentation from GitHub.

  Args:
    qualifier: The Biolink qualifier name to retrieve documentation for.

  Returns:
    Markdown-formatted documentation text extracted from the qualifier's index.html page.

  Raises / Notes:
    Error format: {"error": "message"} on failure.
  """
  return _get_biolink_qualifier_documentation_cached(qualifier)

@MCP.tool(tags={"table-config"})
def get_table_configuration_documentation() -> str:
  """Retrieves Tablassert Table Configuration documentation from GitHub.

  Args:
    None.

  Returns:
    Raw markdown documentation text from the Tablassert configuration guide.

  Raises / Notes:
    Error format: {"error": "message"} on failure.
  """
  return _get_table_configuration_documentation_cached()

@MCP.tool(tags={"table-config"})
def get_table_configuration_model_schema() -> str:
  """Returns JSON schema for Tablassert Section model.

  Args:
    None.

  Returns:
    JSON schema string defining the structure and validation rules for Tablassert Section objects.

  Raises / Notes:
    Error format: {"error": "message"} on failure.
  """
  return _get_table_configuration_model_schema_cached()

@MCP.tool(tags={"biolink"})
def get_biolink_qualifier_list() -> str:
  """Lists all available Biolink qualifier enum values.

  Args:
    None.

  Returns:
    Newline-separated string of all Biolink qualifier enum values.

  Raises / Notes:
    Error format: {"error": "message"} on failure.
  """
  return _get_biolink_qualifier_list_cached()

@MCP.tool(tags={"table-config"})
def read_yaml_to_sections_json(file_path: Annotated[str, "Path to the YAML file to read."]) -> list[dict[str, Any]]:
  """Converts YAML table configuration to Section JSON list.

  Args:
    file_path: Absolute or relative path to the YAML configuration file.

  Returns:
    List of dictionaries representing Tablassert Section objects.

  Raises / Notes:
    Error format: {"error": "message"} on failure.
  """
  serialized_object: object = from_yaml(file_path)
  sections: Any = fastmerge(serialized_object)
  return sections

@MCP.tool(tags={"table-config"})
def write_json_table_configuration_to_yaml(json_configuration: Annotated[str, "JSON string of table configuration to convert."], file_path: Annotated[str, "Path where the YAML file should be written."]) -> None:
  """Converts JSON table configuration to YAML file.

  Args:
    json_configuration: JSON-formatted string containing the table configuration.
    file_path: Absolute or relative path where the YAML file will be saved.

  Returns:
    None.

  Raises / Notes:
    Error format: {"error": "message"} on failure.
  """
  serialized_object: object = json.loads(json_configuration)
  with open(file_path, "w") as f:
    yaml.safe_dump(serialized_object, f)

@MCP.tool(tags={"table-config"})
def validate_json_table_configuration_syntax(json_configuration: Annotated[str, "JSON string of table configuration to validate."]) -> dict[str, Any]:
  """Validates JSON table configuration against Section model schema.

  Args:
    json_configuration: JSON-formatted string containing the table configuration to validate.

  Returns:
    {"ok": 200} on success, {"error": "message"} on validation failure.

  Raises / Notes:
    Error format: {"error": "message"} on failure.
  """
  serialized_object: object = json.loads(json_configuration)
  sections: Any = fastmerge(serialized_object)
  try:
    for s in sections:
      Section.model_validate(s)
    return {"ok": 200}
  except Exception as e:
    msg: dict[str, str] = {"error": str(e)}
    return msg

@MCP.tool(tags={"local-services"})
def download_pmc_file_from_local_mirror(pmc_id: Annotated[str, "PMC identifier (e.g., 'PMC123456' or '123456')."], file_name: Annotated[str, "Name of the file to extract from the archive."], download_root: Annotated[str, "Root directory for PMC tar files."] = "/15TB_1/users/gglusman/PMC/tars") -> str:
  """Downloads PMC file from local HTTP mirror service.

  Args:
    pmc_id: PubMed Central identifier, with or without 'PMC' prefix.
    file_name: Name of the specific file to extract from the PMC archive.
    download_root: Base directory path where PMC tar archives are stored.

  Returns:
    JSON string {"ok": "file_name"} on success, {"error": "message"} on failure.

  Raises / Notes:
    Error format: {"error": "message"} on failure.
    Requires localhost:8051 (PMC mirror) to be running.
  """
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

@MCP.tool(tags={"local-services"})
def get_curies_entity_from_dbssert_ner(entity: Annotated[str, "Entity text to perform NER lookup on."]) -> Union[str, dict[str, Any]]:
  """Performs NER lookup on entity to find matching CURIEs via dbssert.

  Args:
    entity: Text string of the entity to search for.

  Returns:
    Response text with matching CURIEs on success, {"error": "message"} on failure.

  Raises / Notes:
    Error format: {"error": "message"} on failure.
    Requires localhost:8052 (dbssert) to be running.
  """
  url: str = f"http://localhost:8052/curies-with-ner?entity={entity}"
  try:
    with requests.get(url, stream=True) as r:
      r.raise_for_status()
      return r.text
  except Exception as e:
    msg = {"error": str(e)}
    return msg

@MCP.tool(tags={"local-services"})
def get_canonical_curie_information_from_dbssert(curie: Annotated[str, "CURIE identifier to fetch information for."]) -> Union[str, dict[str, Any]]:
  """Retrieves canonical CURIE information from dbssert.

  Args:
    curie: CURIE identifier string (e.g., 'HGNC:12345').

  Returns:
    Response text with canonical CURIE information on success, {"error": "message"} on failure.

  Raises / Notes:
    Error format: {"error": "message"} on failure.
    Requires localhost:8052 (dbssert) to be running.
  """
  url: str = f"http://localhost:8052/canonical-curie-information?curie={curie}"
  try:
    with requests.get(url, stream=True) as r:
      r.raise_for_status()
      return r.text
  except Exception as e:
    msg = {"error": str(e)}
    return msg

def serve_mcp() -> None:
  MCP.run() # pyright: ignore
