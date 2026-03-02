# QualifiersMCP Agents

## Overview

This document provides a code map of the QualifiersMCP server, which adds Biolink qualifier support to Tablassert.

## Tool Count

This server provides **10 MCP tools** organized into 3 groups.

## CODE MAP

| Line | Tool Name | Tags | Purpose |
|------|-----------|------|---------|
| 27 | get_biolink_qualifier_documentation | biolink | Fetches Biolink qualifier documentation from GitHub |
| 61 | get_table_configuration_documentation | table-config | Retrieves Tablassert Table Configuration documentation from GitHub |
| 80 | get_table_configuration_model_schema | table-config | Returns JSON schema for Tablassert Section model |
| 97 | get_biolink_qualifier_list | biolink | Lists all available Biolink qualifier enum values |
| 113 | read_yaml_to_sections_json | table-config | Converts YAML table configuration to Section JSON list |
| 133 | write_json_table_configuration_to_yaml | table-config | Converts JSON table configuration to YAML file |
| 155 | validate_json_table_configuration_syntax | table-config | Validates JSON table configuration against Section model schema |
| 183 | download_pmc_file_from_local_mirror | local-services | Downloads PMC file from local HTTP mirror service |
| 222 | get_curies_entity_from_dbssert_ner | local-services | Performs NER lookup on entity to find matching CURIEs via dbssert |
| 248 | get_canonical_curie_information_from_dbssert | local-services | Retrieves canonical CURIE information from dbssert |

## Tool Groups

### biolink (2 tools)
- `get_biolink_qualifier_documentation`: Fetch documentation for specific Biolink qualifiers
- `get_biolink_qualifier_list`: List all available Biolink qualifier enum values

### table-config (5 tools)
- `get_table_configuration_documentation`: Get Tablassert configuration documentation
- `get_table_configuration_model_schema`: Get JSON schema for validation
- `read_yaml_to_sections_json`: Convert YAML to JSON format
- `write_json_table_configuration_to_yaml`: Convert JSON to YAML format
- `validate_json_table_configuration_syntax`: Validate configuration against schema

### local-services (3 tools)
- `download_pmc_file_from_local_mirror`: Download PMC files from local mirror (requires localhost:8051)
- `get_curies_entity_from_dbssert_ner`: NER lookup for CURIEs (requires localhost:8052)
- `get_canonical_curie_information_from_dbssert`: Get canonical CURIE data (requires localhost:8052)

## Dependencies

- Tablassert: Core configuration and validation models
- Requests: HTTP client for fetching documentation and interacting with local services
- Trafilatura: HTML content extraction from Biolink documentation
- Local Services:
  - localhost:8051: PMC mirror service
  - localhost:8052: dbssert service for CURIE lookups
