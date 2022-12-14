from enigma import Enigma
from enigma import Rotor
from enigma import Reflector
from enigma import Plugboard
from pyenigma import enigma
from pyenigma import rotor
import pytest
import random


def test_init():
    #tests cipher exists with correct settings
    cipher = Enigma(rotors=[["III", 0], ["II", 0], ["I", 0]], reflector="UKW-A",plugboard="AV BS CG DL FU HZ IN KM OW RX")
    assert cipher.alphabet == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    #test duplicate rotor exits
    with pytest.raises(SystemExit):
        Enigma(rotors=[["II", 0], ["II", 0], ["I", 0]], reflector="UKW-A",
               plugboard="AV BS CG DL FU HZ IN KM OW RX")
    #test incorrect rotor specified exits
    with pytest.raises(SystemExit) as excinfo:
        Enigma(rotors=[["I", 0], ["II", 0], ["VXI", 0]], reflector="UKW-A",
               plugboard="AV BS CG DL FU HZ IN KM OW RX")
    #test incorrect reflector specified exits
    with pytest.raises(SystemExit) as excinfo:
        Enigma(rotors=[["I", 0], ["II", 0], ["III", 0]], reflector="UKW-W",
               plugboard="AV BS CG DL FU HZ IN KM OW RX")

def test_plugboard():
    #test all one string only uses first two settings according to pyenigma
    plug_board = Plugboard("NKMOWRX")
    assert plug_board.plugboard == {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H',
                                    'I': 'I', 'J': 'J', 'K': 'N', 'L': 'L', 'M': 'M', 'N': 'K', 'O': 'O', 'P': 'P',
                                    'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X',
                                    'Y': 'Y', 'Z': 'Z'}
    #test incorrect plugboard (duplicate plugs attempted) used sets default plygboard
    plug_board = Plugboard("AN MP BQ AK")
    assert plug_board.plugboard == {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H',
                                    'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P',
                                    'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X',
                                    'Y': 'Y', 'Z': 'Z'}

def test_plugboard_v_pyengima():
    #testing plugboard against pyenigma
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_I,
                                rotor.ROTOR_II, rotor.ROTOR_III, key="AAA",
                                plugs="AV BS CG DL FU HZ IN KM OW RX")

    plug_board = Plugboard("AV BS CG DL FU HZ IN KM OW RX")
    plugboard = {}
    for k,v in plug_board.plugboard.items():
        plugboard[ord(k)] = ord(v)
    assert engine.transtab == plugboard
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_I,
                           rotor.ROTOR_II, rotor.ROTOR_III, key="AAA",
                           plugs="")

    plug_board = Plugboard("")
    plugboard = {}
    for k, v in plug_board.plugboard.items():
        plugboard[ord(k)] = ord(v)
    assert engine.transtab == plugboard
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_I,
                           rotor.ROTOR_II, rotor.ROTOR_III, key="AAA",
                           plugs="AV BS CG DL FU HZ IN KMOWRX")
    plug_board = Plugboard("AV BS CG DL FU HZ IN KMOWRX")
    plugboard = {}
    for k, v in plug_board.plugboard.items():
        plugboard[ord(k)] = ord(v)
    assert engine.transtab == plugboard


def test_rotor_v_pyenigma():
    assert Rotor(["I",0]).rotor_order == rotor.ROTOR_I.wiring
    assert Rotor(["II",0]).rotor_order == rotor.ROTOR_II.wiring
    assert Rotor(["III",0]).rotor_order == rotor.ROTOR_III.wiring
    assert Rotor(["IV",0]).rotor_order == rotor.ROTOR_IV.wiring
    assert Rotor(["V",0]).rotor_order == rotor.ROTOR_V.wiring
    assert Rotor(["VI",0]).rotor_order == rotor.ROTOR_VI.wiring
    assert Rotor(["VII",0]).rotor_order == rotor.ROTOR_VII.wiring
    assert Rotor(["VIII",0]).rotor_order == rotor.ROTOR_VIII.wiring

def test_relfector_v_pyengima():
    assert Reflector("A").order == Reflector("UKW-A").order == rotor.ROTOR_Reflector_A.wiring
    assert Reflector("B").order == Reflector("UKW-B").order == rotor.ROTOR_Reflector_B.wiring
    assert Reflector("C").order == Reflector("UKW-C").order == rotor.ROTOR_Reflector_C.wiring

def test_encrypt_against_pyenigma():
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_I,
                           rotor.ROTOR_II, rotor.ROTOR_III, key="AAA",
                           plugs="AV BS CG DL FU HZ IN KM OW RX")
    secret = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(0, 2000000)])
    ciper_txt_pyenigma = engine.encipher(secret)
    cipher = Enigma(rotors=[["I", 0], ["II", 0], ["III", 0]], reflector="UKW-A",
                    plugboard="AV BS CG DL FU HZ IN KM OW RX")
    cipher_txt = cipher.encrypt(secret)
    assert ciper_txt_pyenigma == cipher_txt
    secret = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(0, 2000000)])
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_II,
                           rotor.ROTOR_I, rotor.ROTOR_IV, key="ABC",
                           plugs="AV BS CG DL FU HZ IN KM OW RX")
    ciper_txt_pyenigma = engine.encipher(secret)
    cipher = Enigma(rotors=[["II", 0], ["I", 1], ["IV", 2]], reflector="UKW-A",
                    plugboard="AV BS CG DL FU HZ IN KM OW RX")
    cipher_txt = cipher.encrypt(secret)
    assert ciper_txt_pyenigma == cipher_txt
    secret = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(0, 2000000)])
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_II,
                           rotor.ROTOR_I, rotor.ROTOR_IV, key="ABC",
                           plugs="AV BS CG DL FU HZ IN KM OW RX")
    ciper_txt_pyenigma = engine.encipher(secret)
    cipher = Enigma(rotors=[["II", 0], ["I", 0], ["IV", 0]], reflector="UKW-A", ringsettings = "ABC",
                    plugboard="AV BS CG DL FU HZ IN KM OW RX")
    cipher_txt = cipher.encrypt(secret)
    assert ciper_txt_pyenigma == cipher_txt

def test_decrypt():
    cipher = Enigma(rotors=[["III", 0], ["II", 0], ["I", 0]], reflector="UKW-A",
                    plugboard="AV BS CG DL FU HZ IN KM OW RX")
    secret = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(0, 2000000)])
    cipher_txt = cipher.decrypt(cipher.encrypt(secret))
    assert secret == cipher_txt
    cipher = Enigma(rotors=[["III", 0], ["II", 0], ["I", 0]], reflector="UKW-A",
                    plugboard="AV BS CG DL FU HZ IN KM OW RX")
    secret = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(0, 2000000)])
    cipher_txt = cipher.decrypt(cipher.encrypt(secret))
    assert secret == cipher_txt
    secret = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(0, 2000000)])
    cipher = Enigma(rotors=[["V", 0], ["VI", 0], ["IV", 0]], reflector="UKW-A", ringsettings="ABC",
                    plugboard="AV BS CG DL FU HZ IN KM OW RX")
    cipher_txt = cipher.decrypt(cipher.encrypt(secret))
    assert secret == cipher_txt

def test_decrypt_v_pyenigma():
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_II,
                           rotor.ROTOR_I, rotor.ROTOR_IV, key="ABC",
                           plugs="AV BS CG DL FU HZ IN KM OW RX")
    secret = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(0, 2000000)])
    cipher_txt = engine.encipher(secret)
    cipher = Enigma(rotors=[["II", 0], ["I", 0], ["IV", 0]], reflector="UKW-A", ringsettings="ABC",
                    plugboard="AV BS CG DL FU HZ IN KM OW RX")
    cipher_txt = cipher.decrypt(cipher_txt)
    assert secret == cipher_txt
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_II,
                           rotor.ROTOR_I, rotor.ROTOR_IV, key="ABC",
                           plugs="AV BS CG DL FU HZ IN KM OW RX")
    secret = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(0, 2000000)])
    cipher_txt = engine.encipher(secret)
    cipher = Enigma(rotors=[["II", 0], ["I", 0], ["IV", 0]], reflector="UKW-A", ringsettings="ABC",
                    plugboard="AV BS CG DL FU HZ IN KM OW RX")
    cipher_txt = cipher.decrypt(cipher_txt)
    assert secret == cipher_txt
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_II,
                           rotor.ROTOR_I, rotor.ROTOR_IV, key="ABC",
                           plugs="AV BS CG DL FU HZ IN KM OW RX")
    secret = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(0,2000000)])
    cipher_txt = engine.encipher(secret)
    cipher = Enigma(rotors=[["II", 0], ["I", 0], ["IV", 0]], reflector="UKW-A", ringsettings="ABC",
                    plugboard="AV BS CG DL FU HZ IN KM OW RX")
    cipher_txt = cipher.decrypt(cipher_txt)
    assert secret == cipher_txt

