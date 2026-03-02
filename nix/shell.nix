{pkgs, lib, config, ...}: 
let
  py = pkgs.python313Packages;
in {
  packages.default = py.qualifiers-mcp;
  apps.default = {
    type = "app";
    program = "${py.qualifiers-mcp}/bin/serve-mcp";
  };
  devShells.default = pkgs.mkShell {
    packages = with py; [
      qualifiers-mcp
    ];
  };
}