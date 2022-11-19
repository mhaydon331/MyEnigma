from enigma import Enigma
from enigma import Rotor
from enigma import Reflector
from enigma import Plugboard
from pyenigma import enigma
from pyenigma import rotor
import pytest


def test_init():
    #tests cipher exists with correct settings
    cipher = Enigma(rotors = [["III",0],["II",0],["I",0]], reflector = "UKW-A", plugboard = "AV BS CG DL FU HZ IN KM OW RX")
    assert cipher.alphabet == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    #test duplicate rotor exits
    with pytest.raises(SystemExit) as excinfo:
        cipher = Enigma(rotors = [["II",0],["II",0],["I",0]], reflector = "UKW-A", plugboard = "AV BS CG DL FU HZ IN KM OW RX")
    #test incorrect rotor specified exits
    with pytest.raises(SystemExit) as excinfo:
        cipher = Enigma(rotors = [["I",0],["II",0],["VI",0]], reflector = "UKW-A", plugboard = "AV BS CG DL FU HZ IN KM OW RX")
    #test incorrect reflector specified exits
    with pytest.raises(SystemExit) as excinfo:
        cipher = Enigma(rotors = [["I",0],["II",0],["III",0]], reflector = "UKW-W", plugboard = "AV BS CG DL FU HZ IN KM OW RX")

def test_plugboard():
    #test incorrect plugboard used sets default plygboard
    plug_board = Plugboard("NKMOWRX")
    assert plug_board.plugboard == {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'}
    #test incorrect plugboard (duplicate plugs attempted) used sets default plygboard
    plug_board = Plugboard("AN MP BQ AK")
    assert plug_board.plugboard == {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'}
    #testing plugboard against pyenigma
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_I,
                                rotor.ROTOR_II, rotor.ROTOR_III, key="AAA",
                                plugs="AV BS CG DL FU HZ IN KM OW RX")

    cipher = Enigma(rotors = [["III",0],["II",0],["I",0]], reflector = "UKW-A",
                                plugboard = "AV BS CG DL FU HZ IN KM OW RX")
    plugboard = {}
    for k,v in cipher.plugboard_map.plugboard.items():
        plugboard[ord(k)] = ord(v)
    assert engine.transtab == plugboard
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_I,
                                rotor.ROTOR_II, rotor.ROTOR_III, key="AAA",
                                plugs="")

    cipher = Enigma(rotors = [["III",0],["II",0],["I",0]], reflector = "UKW-A",
                                plugboard = "")
    plugboard = {}
    for k,v in cipher.plugboard_map.plugboard.items():
        plugboard[ord(k)] = ord(v)
    assert engine.transtab == plugboard


def test_rotor():
    assert Rotor(["I",0]).rotor_order == rotor.ROTOR_I.wiring
    assert Rotor(["II",0]).rotor_order == rotor.ROTOR_II.wiring
    assert Rotor(["III",0]).rotor_order == rotor.ROTOR_III.wiring
    assert Rotor(["IV",0]).rotor_order == rotor.ROTOR_IV.wiring
    assert Rotor(["V",0]).rotor_order == rotor.ROTOR_V.wiring

def test_against_pyenigma():
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_I,
                                rotor.ROTOR_II, rotor.ROTOR_III, key="AAA",
                                plugs="AV BS CG DL FU HZ IN KM OW RX")
    secret = engine.encipher("A"*20000)
    cipher = Enigma(rotors = [["III",0],["II",0],["I",0]], reflector = "UKW-A", plugboard = "AV BS CG DL FU HZ IN KM OW RX")
    cipher_txt = cipher.encrypt("A"*20000)
    assert secret == cipher_txt


def test_encrypt():
    pass

def test_decrypt():
    pass
