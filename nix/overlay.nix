final: prev: {
  python313Packages = prev.python313Packages.override {
    overrides = pyFinal: pyPrev: {
      fastmcp = pyPrev.fastmcp.overridePythonAttrs (old: {
        dontCheckRuntimeDeps = true;
        doCheck = false;
      });
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
          requests
          fastmcp
          pyyaml
        ]) ++ (with prev.python313Packages; [
          optimum-onnx
          tablassert
        ]);
        doCheck = false;
      };
    };
  };
}