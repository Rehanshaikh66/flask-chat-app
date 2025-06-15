{ pkgs }: {
  deps = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.python3Packages."flask"
    pkgs.python3Packages."flask-socketio"
    pkgs.python3Packages."python-dotenv"
    pkgs.python3Packages."pymongo"
    pkgs.python3Packages."nltk"
    pkgs.python3Packages."setuptools"
    pkgs.python3Packages."wheel"
  ];
}

