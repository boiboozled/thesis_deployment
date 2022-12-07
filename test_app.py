import pandas as pd
import collections
from app import add_all_players_to_nba_card,add_all_players_to_wts,add_all_players_to_custom,add_all_players_to_pres_2,add_all_players_to_ast_to_trend,add_all_players_to_pres_3,add_all_players_to_pres_ft

data = pd.read_csv("./data/player_performance_pressure.csv")
names= data.PLAYER_NAME.unique()
def test_001_add_all_players_to_nba_card():
    output= add_all_players_to_nba_card(1)
    assert collections.Counter(output) == collections.Counter(names)

def test_002_add_all_players_to_wts():
    output= add_all_players_to_wts(1)
    assert collections.Counter(output) == collections.Counter(names)

def test_003_add_all_players_to_custom():
    output = add_all_players_to_custom(1)
    assert collections.Counter(output) == collections.Counter(names)

def test_004_add_all_players_to_pres_2():
    output = add_all_players_to_pres_2(1)
    assert collections.Counter(output) == collections.Counter(names)

def test_005_add_all_players_to_pres_3():
    output = add_all_players_to_pres_3(1)
    assert collections.Counter(output) == collections.Counter(names)

def test_006_add_all_players_to_pres_ft():
    output = add_all_players_to_pres_ft(1)
    assert collections.Counter(output) == collections.Counter(names)

def test_007_add_all_players_to_nba_card():
    output = add_all_players_to_nba_card(1)
    assert collections.Counter(output) == collections.Counter(names)
