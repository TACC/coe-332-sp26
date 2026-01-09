{
  description = "Computational Methods for Automated Formal Reasoning";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
    shell-utils.url = "github:waltermoreira/shell-utils";
  };

  outputs = { self, nixpkgs, flake-utils, shell-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        shell = shell-utils.myShell.${system};
        python = pkgs.python311;
        docsPython = python.withPackages (ps: [
          ps.sphinx
          ps.sphinx-autobuild
          ps.sphinx_rtd_theme
          ps.sphinx-tabs
          ps.docutils
          ps.setuptools
        ]);
        commonPackages = [ docsPython pkgs.rsync pkgs.gnumake pkgs.lesspipe pkgs.less pkgs.coreutils pkgs.bashInteractive pkgs.which ];
      in {
        devShells.default = pkgs.mkShell {
          name = "332";
          buildInputs = commonPackages;
          shellHook = ''
           eval "$(lesspipe.sh)"
           '';
        };
      }
    );
}