import sys
from pyenigma import enigma
from pyenigma import rotor

class Enigma:
    #Enigma I (German Army and Airforce)
    def __init__(self, rotors = [["III",0],["II",0],["I",0]], reflector = "UKW-B", ringsettings = "",plugboard = "AT BS DE FM IR KN LZ OW PV XY"):
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
        #adjusted rotor order to mimic left,mid,right order rather than backwards
        ringsettings = ringsettings.upper()
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if type(rotors) == list:
            try:
                if rotors[0][0] == rotors[1][0] or rotors[0][0] == rotors[2][0] or rotors[1][0] == rotors[2][0]:
                    print("Incorrect Rotor Settings")
                    sys.exit(1)
            except IndexError:
                print("Incorrect Rotor Settings")
                sys.exit(1)
            try:
                # added ring settings or offset option
                print(type(rotors))
                if ringsettings != "" and len(ringsettings) == 3 and ringsettings.isalpha():
                    rotors[0][1] = self.alphabet.index(ringsettings[0])
                    rotors[1][1] = self.alphabet.index(ringsettings[1])
                    rotors[2][1] = self.alphabet.index(ringsettings[2])
                self.rotor_left = Rotor(rotors[2])
                self.rotor_mid = Rotor(rotors[1])
                self.rotor_right = Rotor(rotors[0])
            except KeyError:
                print("Incorrect Rotor Settings")
                sys.exit(1)
        else:
            try:
                rotors_list = []
                rotors = rotors.strip().split(",")
                if ringsettings != "" and len(ringsettings) == 3 and ringsettings.isalpha():
                    for i in range(0,len(rotors)):
                        rotors_list.append([rotors[i],self.alphabet.index(ringsettings[i])])
                    rotors = rotors_list
                    self.rotor_left = Rotor(rotors[2])
                    self.rotor_mid = Rotor(rotors[1])
                    self.rotor_right = Rotor(rotors[0])
                else:
                    print("Incorrect Rotor Settings")
                    sys.exit(1)
            except IndexError:
                print("Incorrect Roto1r Settings")
                sys.exit(1)
            except KeyError:
                print("Incorrect Rotor2 Settings")
                sys.exit(1)
        try:
            self.reflector = Reflector(reflector)
        except KeyError:
            print("Incorrect Reflector")
            sys.exit(1)
        self.plugboard_map  = Plugboard(plugboard)

    def __str__(self):
        return """
        Left Rotor: %s 
        
        Mid Rotor: %s 
        
        Right Rotor: %s
        
        Reflector: %s
        
        Plugboard: %s""" % (self.rotor_left, self.rotor_mid, self.rotor_right, self.reflector, self.plugboard_map)

    def encrypt(self, plain_txt):
        #print("Plain Text:  ",plain_txt)
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
    """
    ROTOR_I = Rotor(wiring="EKMFLGDQVZNTOWYHXUSPAIBRCJ",notchs="R", name="I", model="Enigma 1", date="1930")
    ROTOR_II = Rotor(wiring="AJDKSIRUXBLHWTMCQGZNPYFVOE",notchs="F", name="II", model="Enigma 1", date="1930")
    ROTOR_III = Rotor(wiring="BDFHJLCPRTXVZNYEIWGAKMUSQO",notchs="W", name="III", model="Enigma 1", date="1930")
    ROTOR_IV = Rotor(wiring="ESOVPZJAYQUIRHXLNFTGKDCMWB",notchs="K", name="IV", model="M3 Army", date="December 1938")
    ROTOR_V = Rotor(wiring="VZBRGITYUPSDNHLXAWMJQOFECK",notchs="A", name="V", model="M3 Army", date="December 1938")
    ROTOR_VI = Rotor(wiring="JPGVOUMFYQBENHZRDKASXLICTW",notchs="AN", name="VI", model="M3 & M4 Naval(February 1942)", date="1939")
    ROTOR_VII = Rotor(wiring="NZJHGRCXMYSWBOUFAIVLPEKQDT",notchs="AN", name="VII", model="M3 & M4 Naval(February 1942)", date="1939")
    ROTOR_VIII = Rotor(wiring="FKQHTLXOCBJSPDZRAMEWNIUYGV",notchs="AN", name="VIII", model="M3 & M4 Naval(February 1942)", date="1939")

    """
    def __init__(self,settings):
        self.setting = settings[0]
        self.offset = settings[1]
        self.base_rotor = None
        self.rotor_settings = {
                "I":    ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "R",  "Q", "Enigma 1", "1930"],
                "II":   ["AJDKSIRUXBLHWTMCQGZNPYFVOE", "F",  "E", "Enigma 1", "1930"],
                "III":  ["BDFHJLCPRTXVZNYEIWGAKMUSQO", "W",  "V", "Enigma 1", "1930"],
                "IV":   ["ESOVPZJAYQUIRHXLNFTGKDCMWB", "K",  "J", "M3 Army", "December 1938"],
                "V":    ["VZBRGITYUPSDNHLXAWMJQOFECK", "A",  "Z", "M3 Army", "December 1938"],
                "VI":   ["JPGVOUMFYQBENHZRDKASXLICTW", "AN", "ZM", "M3 & M4 Naval(February 1942)", "1939"],
                "VII":  ["NZJHGRCXMYSWBOUFAIVLPEKQDT", "AN", "ZM", "M3 & M4 Naval(February 1942)", "1939"],
                "VIII": ["FKQHTLXOCBJSPDZRAMEWNIUYGV", "AN", "ZM", "M3 & M4 Naval(February 1942)", "1939"]
                }
        self.rotor_order = None
        self.turnover_letter = self.rotor_settings[self.setting][1]
        self.notch = self.rotor_settings[self.setting][2]
        self.turnover = False
        self.reset()
        self.model = self.rotor_settings[self.setting][3]
        self.date = self.rotor_settings[self.setting][4]

    def __str__(self):
        return """
        Name: %s
        Model: %s
        Date: %s
        Wiring: %s
        Offset: %s""" % (self.setting, self.model, self.date, self.rotor_order, self.original_offset)

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
        self.original_offset = self.base_rotor[0]

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
    cipher = Enigma(rotors = "I,II,III", reflector = "UKW-A",ringsettings="AAA", plugboard = "AV BS CG DL FU HZ IN KM OW RX")
    #print("Left cipher order: ",cipher.rotor_left.rotor_order)
    #print(cipher.plugboard_map.plugboard)
    cipher_txt = cipher.encrypt("A"*20000)
    #print("Encrypted Text:   QYQBPFOCGWJMZOSICSPZNBYSZYJCSXJYPCJRCSIZIIQOFYPWBRNHQHMKQQ")
    cipher.decrypt(cipher_txt)

    #print("My Machine:")
    #print()

    #print(rotor.ROTOR_GR_III)
    engine = enigma.Enigma(rotor.ROTOR_Reflector_A, rotor.ROTOR_I,
                                rotor.ROTOR_II, rotor.ROTOR_III, key="AAA",
                                plugs="AV BS CG DL FU HZ IN KM OW RX")
    #print(rotor.ROTOR_I.wiring)
    print(engine)
    secret = engine.encipher("A"*20000)
    #print(secret)
    #print(cipher_txt == secret)
    #print(rotor.ROTOR_I)
    print(cipher)
    """
    cipher = Enigma(rotors = [["VI",0],["II",0],["I",0]], reflector = "UKW-A", plugboard = "AV BS CG DL FU HZ IN KMOWRX")
    print(engine.transtab)
    plugboard = {}
    for k,v in cipher.plugboard_map.plugboard.items():
        plugboard[ord(k)] = ord(v)
    print(plugboard)
    print(plugboard == engine.transtab)
    """
