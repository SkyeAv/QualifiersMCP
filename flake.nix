{
  description = "QualifiersMCP (1.0.0)";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    systems.url = "github:nix-systems/default";
    flake-parts.url = "github:hercules-ci/flake-parts";
    tablassert.url = "github:SkyeAv/Tablassert";
  };
  outputs = inputs @ {self, systems, nixpkgs, flake-parts, tablassert, ...}:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = import inputs.systems;
      perSystem = {pkgs, lib, config, system, ...}: {
        _module.args.pkgs = import nixpkgs {
          inherit system;
          overlays = [
            tablassert.overlays.default
            self.overlays.default
          ];
        };
        imports = [
          ./nix/docker.nix
          ./nix/shell.nix
        ];
      };
      flake = {
        overlays.default = import ./nix/overlay.nix;
      };
    };
}