final: prev: {
  python313Packages = prev.python313Packages.override {
    overrides = pyFinal: pyPrev: {
      qualifiers-mcp = pyFinal.buildPythonApplication rec {
        pname = "QualifiersMCP";
        version = "1.0.0";
        format = "pyproject";
        src = ../.;
        build-system = with pyFinal; [
          setuptools
          wheel
        ];
        propagatedBuildInputs = (with pyFinal; [
          trafilatura
          tablassert
          fastmcp
          pyyaml
        ]);
        doCheck = false;
      };
    };
  };
}