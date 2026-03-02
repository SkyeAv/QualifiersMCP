{pkgs, lib, config, ...}: 
let
  py = pkgs.python313Packages;
in {
  packages.default = py.qualifiers-mcp;
  devShells.default = pkgs.mkShell {
    packages = with py; [
      qualifiers-mcp
    ];
  };
}