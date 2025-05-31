{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.streamlit
    pkgs.python311Packages.pandas
    pkgs.python311Packages.yfinance
    pkgs.python311Packages.requests
    pkgs.python311Packages.schedule
    pkgs.python311Packages.python-dotenv
  ];
}
