import os
from stockfish import Stockfish

def find_latest_file(folder):
    # Get a list of all the files in the folder
    files = os.listdir(folder)
    # Sort the list of files by modification time
    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    # Get the most recent file
    latest_file = files[-1]
    # Return the full path of the file
    return os.path.join(folder, latest_file)


def get_stock_fish():
  try:
    sf = Stockfish(r'stockfish\stockfish-windows-2022-x86-64-avx2.exe')
  except:
    sf = Stockfish(r'stockfish_linux\stockfish_15.1_x64_bmi2')
  sf.set_depth(18)
  sf.set_skill_level(20)
  return sf