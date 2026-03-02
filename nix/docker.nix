{pkgs, lib, config, ...}: 
let 
  py = pkgs.python313Packages;
in {
  packages.docker = pkgs.dockerTools.buildImage {
    name = "qualifiers-mcp";
    tag = "latest";
    copyToRoot = pkgs.buildEnv {
      name = "image-root";
      paths = (with py; [
        qualifiers-mcp
      ]);
      pathsToLink = [
        "/bin"
        "/etc"
      ];
    };
    config = {
      Entrypoint = ["serve-mcp"];
    };
  };
}