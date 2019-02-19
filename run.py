import letsdothis
import sysinfo
from pprint import pprint

def run():
    player_1 = str(input("Enter the name for player 1: "))
    player_2 = str(input("Enter the name for player 2: "))
    letsdothis.play(player_1, player_2)

if __name__=="__main__":
    run()
