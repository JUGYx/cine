def fmtc(color, string):
    colors = {"red":"\033[31m",
              "yellow":"\033[33m",
              "none":"\033[34m"
              }
    return f"{colors[color]}{string}{colors['none']}"

def printerr(string):
    print(fmtc("red", "\n[!] "+string+"\n"))
