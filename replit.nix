{pkgs}: {
  deps = [
    pkgs.rustc
    pkgs.openssl
    pkgs.libxcrypt
    pkgs.libiconv
    pkgs.cargo
    pkgs.cacert
    pkgs.pkg-config
    pkgs.libffi
  ];
}
