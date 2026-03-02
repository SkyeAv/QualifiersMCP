# QualifiersMCP

## Version 1.0.0

### By the QualifiersMCP contributors

QualifiersMCP is an MCP server for authoring and validating Tablassert table configuration files with Biolink qualifiers. It provides tools to fetch qualifier documentation, convert YAML/JSON table configurations, validate configuration syntax against Tablassert models, and call local helper services for PMC extraction and CURIE lookup workflows.

## Documentation Context

This MCP is designed to support Tablassert table-configuration authoring:

- **Tablassert:** https://github.com/SkyeAv/Tablassert
- **Tablassert docs:** https://skyeav.github.io/Tablassert/

It also integrates with local companion services:

- **PMCTarsAPI (localhost:8051):** https://github.com/SkyeAv/PMCTarsAPI
- **DbssertAPI (localhost:8052):** https://github.com/SkyeAv/DbssertAPI
- **Dbssert database source:** https://github.com/SkyeAv/Dbssert

## Quick Start

```bash
# Clone repository
git clone https://github.com/SkyeAv/QualifiersMCP.git
cd QualifiersMCP

# Enter development shell
nix develop -L .

# Run MCP server
serve-mcp
```

## Usage (With Nix)

### Method 1: Development Shell (Recommended)

Best for active development and local testing.

```bash
git clone https://github.com/SkyeAv/QualifiersMCP.git
cd QualifiersMCP
nix develop -L .
serve-mcp
```

### Method 2: Direct Run from Flake

Run the default app directly from the repository flake.

```bash
nix run github:SkyeAv/QualifiersMCP
```

### Method 3: User Profile Installation

Install to your user profile for repeated use.

```bash
# Install
nix profile install github:SkyeAv/QualifiersMCP

# Run anywhere
serve-mcp
```

### Method 4: Use as Overlay

Integrate into your own Nix flake as a Python package.

```nix
{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    qualifiers-mcp.url = "github:SkyeAv/QualifiersMCP";
  };

  outputs = { self, nixpkgs, qualifiers-mcp }: {
    pkgs = import nixpkgs {
      system = "x86_64-linux";
      overlays = [ qualifiers-mcp.overlays.default ];
    };

    devShells.default = pkgs.mkShell {
      packages = [ pkgs.python313Packages.qualifiers-mcp ];
    };
  };
}
```

### Method 5: Docker (GHCR Prebuilt Images)

Use architecture-specific images published to GHCR. Under the current workflow trigger (`master`), images are tagged by commit SHA (`sha-<commit-sha>`); a shared `latest` tag is not emitted for normal branch pushes.

```bash
# x86_64 / amd64
docker run --rm ghcr.io/skyeav/qualifiers-mcp-amd64:sha-<commit-sha>
```

```bash
# aarch64 / arm64
docker run --rm ghcr.io/skyeav/qualifiers-mcp-arm64:sha-<commit-sha>
```

### Method 6: Docker (Build Locally via Nix)

Build the Docker image defined in this repository and run it locally.

```bash
# Build image tarball
nix build .#docker

# Load and run
docker load < result
docker run --rm qualifiers-mcp:latest
```

## What This MCP Provides

- **Biolink qualifier support:** Discover qualifier names and fetch qualifier docs from Biolink model pages
- **Table configuration authoring:** Convert between YAML and JSON-oriented table configuration representations
- **Validation:** Validate configuration payloads against the Tablassert `Section` model
- **Local service integration:** Access local PMC and CURIE services used in bioinformatics workflows
- **Health visibility:** Check local dependency availability from a single MCP tool

## MCP Tools

This server currently provides **11 MCP tools** in 3 groups.

### biolink (2 tools)

1. `get_biolink_qualifier_documentation`
   - Fetches Biolink qualifier documentation for a specific qualifier string
2. `get_biolink_qualifier_list`
   - Returns the available Biolink qualifier enum values

### table-config (5 tools)

1. `get_table_configuration_documentation`
   - Retrieves Tablassert table-configuration documentation markdown
2. `get_table_configuration_model_schema`
   - Returns JSON schema for the Tablassert `Section` model
3. `read_yaml_to_sections_json`
   - Reads table YAML and returns merged Section JSON objects
4. `write_json_table_configuration_to_yaml`
   - Writes table configuration JSON to YAML at a target path
5. `validate_json_table_configuration_syntax`
   - Validates JSON configuration syntax against Tablassert `Section` validation rules

### local-services (4 tools)

1. `download_pmc_file_from_local_mirror`
   - Downloads a file from the local PMC tar mirror service (`localhost:8051`)
2. `get_curies_entity_from_dbssert_ner`
   - Performs NER-based CURIE lookup through dbssert API (`localhost:8052`)
3. `get_canonical_curie_information_from_dbssert`
   - Retrieves canonical CURIE information from dbssert API (`localhost:8052`)
4. `check_local_service_statuses`
   - Checks health endpoints of both local services (`localhost:8051` and `localhost:8052`)

## Local Service Requirements

Some tools require local services to be running before use:

- **Port 8051:** PMCTarsAPI for local PMC tar extraction endpoints
- **Port 8052:** DbssertAPI for CURIE lookup and canonical CURIE endpoints

Recommended startup order for full functionality:

1. Start PMCTarsAPI (`localhost:8051`)
2. Start DbssertAPI (`localhost:8052`)
3. Start `serve-mcp`
4. Run `check_local_service_statuses` from your MCP client

## Typical Table-Configuration Workflow

1. Inspect available qualifiers with `get_biolink_qualifier_list`
2. Read qualifier details with `get_biolink_qualifier_documentation`
3. Fetch table-config guidance with `get_table_configuration_documentation`
4. Validate JSON config drafts using `validate_json_table_configuration_syntax`
5. Write YAML output with `write_json_table_configuration_to_yaml`
6. Optionally re-read YAML into merged JSON using `read_yaml_to_sections_json`

## Entry Points and Implementation Notes

- Python package name: `QualifiersMCP`
- MCP runtime entrypoint: `serve-mcp` (from `pyproject.toml`)
- Script target: `QualifiersMCP.mcp:serve_mcp`
- Core implementation: `lib/QualifiersMCP/mcp.py`
- Nix app path: `nix/shell.nix`
- Docker image definition: `nix/docker.nix`

## Development

```bash
# Enter dev shell
nix develop -L .

# Run server locally
serve-mcp
```

## Repository

- **QualifiersMCP:** https://github.com/SkyeAv/QualifiersMCP
