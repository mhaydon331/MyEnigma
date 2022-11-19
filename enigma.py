import sys
import string
import json
from pyenigma import enigma
from pyenigma import rotor

class Enigma:
    #Enigma I (German Army and Airforce)
    def __init__(self, rotors = [["I",0],["II",0],["III",0]], reflector = "UKW-B", ringsettings = "ABC",ringpositions = "DEF",plugboard = "AT BS DE FM IR KN LZ OW PV XY"):
        """
        Rotors
        Setting Wiring                      Notch   Window  Turnover
        Base    ABCDEFGHIJKLMNOPQRSTUVWXYZ
        I       EKMFLGDQVZNTOWYHXUSPAIBRCJ  Y       Q       R
        II      AJDKSIRUXBLHWTMCQGZNPYFVOE  M       E       F
        III     BDFHJLCPRTXVZNYEIWGAKMUSQO  D       V       W
        IV      ESOVPZJAYQUIRHXLNFTGKDCMWB  R       J       K
        V       VZBRGITYUPSDNHLXAWMJQOFECK  H       Z       A
        VI      JPGVOUMFYQBENHZRDKASXLICTW  H/U     Z/M     A/N
        VII     NZJHGRCXMYSWBOUFAIVLPEKQDT  H/U     Z/M     A/N
        VIII    FKQHTLXOCBJSPDZRAMEWNIUYGV  H/U     Z/M     A/N
        """
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if rotors[0][0] == rotors[1][0] or rotors[0][0] == rotors[2][0] or rotors[1][0] == rotors[2][0]:
            print("Incorrect Keys")
            sys.exit(1)
        try:
            self.rotor_left = Rotor(rotors[0])
            self.rotor_mid = Rotor(rotors[1])
            self.rotor_right = Rotor(rotors[2])
        except KeyError:
            print("Incorrect Keys")
            sys.exit(1)
        try:
            self.reflector = Reflector(reflector)
        except KeyError:
            print("Incorrect Reflector")
            sys.exit(1)
        self.plugboard_map  = Plugboard(plugboard)

    def encrypt(self, plain_txt):
        print("Plain Text:  ",plain_txt)
        cipher_txt = ""
        #Time to encrypt
        #if not alpha just skip
        plain_txt = plain_txt.upper()
        """
        print(self.rotor_right.base_rotor)
        print(self.rotor_right.rotor_order)
        print(self.rotor_mid.base_rotor)
        print(self.rotor_mid.rotor_order)
        print(self.rotor_left.base_rotor)
        print(self.rotor_left.rotor_order)
        """
        for i in plain_txt:
            #if not alpha just skip
            if not i.isalpha():
                cipher_txt += i
                continue
            rotor_trigger = False
            #right rotor rotates on every key press

            ##This is not working right
            self.rotor_right.rotate()
            #mid rotates on notch
            if self.rotor_mid.base_rotor[0] in self.rotor_mid.notch:
                self.rotor_mid.rotate()
            #rotate on turnover
            if self.rotor_right.turnover:
                self.rotor_right.turnover = False
                self.rotor_mid.rotate()
            if self.rotor_mid.turnover:
                self.rotor_mid.turnover = False
                self.rotor_left.rotate()


            #pass through plugboard
            i = self.plugboard_map.forward(i)

            #pass through rotors right to left
            i = self.rotor_right.forward(i)
            i = self.rotor_mid.forward(i)
            i = self.rotor_left.forward(i)

            #pass through reflector
            i = self.reflector.forward(i)

            #pass through rotors left to right
            i = self.rotor_left.backward(i)
            i = self.rotor_mid.backward(i)
            i = self.rotor_right.backward(i)

            #pass back through plugboard
            cipher_txt += self.plugboard_map.backward(i)


        #print("Encrypted Text:  ",cipher_txt)
        return cipher_txt

    def reset(self):
        self.rotor_right.reset()
        self.rotor_mid.reset()
        self.rotor_left.reset()

    def decrypt(self,cipher_txt):
        self.reset()
        return self.encrypt(cipher_txt)

class Plugboard:
    #could expand this to allow alternate forms and check until unusable string
    def __init__(self,settings):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.plugboard = {}
        if type(settings) != str:
            print("Incorrect Plugboard settings. No plugboard used")
            for c in self.alphabet:
                self.plugboard[c] = c
        else:
            try:
                plugboard = settings.split(" ")
                #for i in plugboard:
                #    if len(i)!= 2:
                #       raise IndexError("Incorrect Plugboard settings. No plugboard used")
                for c in self.alphabet:
                    self.plugboard[c] = c
                map_set = set()
                for map in plugboard:
                    if map[0] in map_set or map[1] in map_set:
                        raise IndexError("Incorrect Plugboard settings. No plugboard used")
                    self.plugboard[map[0]] = map[1]
                    self.plugboard[map[1]] = map[0]
                    map_set.add(map[0])
                    map_set.add(map[1])
            except IndexError:
                print("Incorrect Plugboard settings. No plugboard used")
                for c in self.alphabet:
                    self.plugboard[c] = c

    def forward(self,letter):
        #return the mapped char
        return self.alphabet.index(self.plugboard[letter])

    def backward(self,index):
        #return the mapped char
        return self.plugboard[self.alphabet[index]]

class Rotor:
    def __init__(self,settings):
        self.setting = settings[0]
        self.offset = settings[1]
        self.base_rotor = None
        self.rotor_settings = {
                "I":    ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "R",  "Q"],
                "II":   ["AJDKSIRUXBLHWTMCQGZNPYFVOE", "F",  "E"],
                "III":  ["BDFHJLCPRTXVZNYEIWGAKMUSQO", "W",  "V"],
                "IV":   ["ESOVPZJAYQUIRHXLNFTGKDCMWB", "K",  "J"],
                "V":    ["VZBRGITYUPSDNHLXAWMJQOFECK", "A",  "Z"],
                "VI":   ["JPGVOUMFYQBENHZRDKASXLICTW", "AN", "ZM"],
                "VII":  ["NZJHGRCXMYSWBOUFAIVLPEKQDT", "AN", "ZM"],
                "VIII": ["FKQHTLXOCBJSPDZRAMEWNIUYGV", "AN", "ZM"]
                }
        self.rotor_order = None
        self.turnover_letter = self.rotor_settings[self.setting][1]
        self.notch = self.rotor_settings[self.setting][2]
        self.turnover = False
        self.reset()

    #might need to reverse these?
    def forward(self,index):
        #self.rotor_order[self.base_rotor.index(letter)]
        return self.base_rotor.index(self.rotor_order[index])

    def backward(self,index):
        #self.base_rotor[self.rotor_order.index(letter)]
        return self.rotor_order.index(self.base_rotor[index])

    def rotate(self):
        self.base_rotor = self.base_rotor[1:] + self.base_rotor[0]
        self.rotor_order = self.rotor_order[1:] + self.rotor_order[:1]
        if(self.base_rotor[0] in self.turnover_letter):
            self.turnover = True

    def reset(self):
        #Reset the rotor positions
        self.base_rotor = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.rotor_order = self.rotor_settings[self.setting][0]
        for _ in range(0,self.offset):
            self.rotate()

class Reflector:
    def __init__(self,settings):
        self.setting = settings
        self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.reflector_settings = {
                "UKW-A": "EJMZALYXVBWFCRQUONTSPIKHGD",
                "UKW-B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
                "UKW-C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
                "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
                "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
                "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
                }
        self.order = self.reflector_settings[self.setting]

    def forward(self, index):
        #passing through reflector and returning index
        return self.order.index(self.base[index])

if __name__ == "__main__":
    cipher = Enigma(rotors = [["VI",0],["II",0],["I",0]], reflector = "UKW-A", plugboard = "AV BS CG DL FU HZ IN KM OW RX")
    print("Left cipher order: ",cipher.rotor_left.rotor_order)
    print(cipher.plugboard_map.plugboard)
    cipher_txt = cipher.encrypt("A"*20000)
    #print("Encrypted Text:   QYQBPFOCGWJMZOSICSPZNBYSZYJCSXJYPCJRCSIZIIQOFYPWBRNHQHMKQQ")
    cipher.decrypt(cipher_txt)

    #print("My Machine:")
    #print()

    #print(rotor.ROTOR_GR_III)
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_I,
                                rotor.ROTOR_II, rotor.ROTOR_VI, key="AAA",
                                plugs="AV BS CG DL FU HZ IN KM OW RX")
    #print(rotor.ROTOR_I.wiring)
    print(engine)
    secret = engine.encipher("A"*20000)
    #print(secret)
    print(cipher_txt == secret)
    """
    cipher = Enigma(rotors = [["VI",0],["II",0],["I",0]], reflector = "UKW-A", plugboard = "AV BS CG DL FU HZ IN KMOWRX")
    print(engine.transtab)
    plugboard = {}
    for k,v in cipher.plugboard_map.plugboard.items():
        plugboard[ord(k)] = ord(v)
    print(plugboard)
    print(plugboard == engine.transtab)
    """
