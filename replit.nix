{ pkgs }: {
  deps = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.python3Packages.flask
    pkgs.python3Packages.nltk
    pkgs.python3Packages.flask_socketio
    pkgs.python3Packages.python_dotenv
    pkgs.python3Packages.pymongo
  ];
}
