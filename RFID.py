print("Demarrage 'RFID.py'")
def RFID_presence():
    return (MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)[0]==MIFAREReader.MI_OK)
def RFID_carteCheck():
    _time=time()
    while (time()-_time<1):
        if RFID_presence():
            return True
    return False
def RFID_waitRetireCarte():
    _counter=1
    while RFID_carteCheck():
        MENU_clear() #Nettoie l'écran
        _counter=_counter%4+1
        hint("RETIRER LA CARTE",_counter)
    return
def RFID_read(block):
    while True:
        try:
            if RFID_presence():
                (status,uid)=MIFAREReader.MFRC522_Anticoll()
                if status==MIFAREReader.MI_OK:
                    MIFAREReader.MFRC522_SelectTag(uid)
                    TAG=STRING_Tag(MIFAREReader.MFRC522_Read(block)[0:4])
                    return TAG
        except:
            hint("! PROBLEME LECTURE !",4)
            sleep(1)
            hint("",4)
def RFID_readCarte():
    while True:
        try:
            if RFID_presence():
                (status,uid)=MIFAREReader.MFRC522_Anticoll()
                if status==MIFAREReader.MI_OK:
                    return (int(STRING_Tag(uid)),int(STRING_Tag(MIFAREReader.MFRC522_Read(config.blockArgent)[0:8])),int(STRING_Tag(MIFAREReader.MFRC522_Read(config.blockHashCodeGuinche)[0:8])),int(STRING_Tag(MIFAREReader.MFRC522_Read(config.blockHashUID)[0:8])),int(STRING_Tag(MIFAREReader.MFRC522_Read(config.blockHashArgent)[0:8])))
        except:
            hint("! PROBLEME LECTURE !",4)
            sleep(1)
            hint("",4)
        sleep(0.01)
def RFID_write(block,TAG):
    tag=STRING_List(TAG)
    while True:
        try:
            if RFID_presence():
                (status,uid) = MIFAREReader.MFRC522_Anticoll()
                if status == MIFAREReader.MI_OK:
                    MIFAREReader.MFRC522_Read(block)
                    MIFAREReader.MFRC522_Write(block,tag)
                    TAG_read=RFID_read(block)
                    if str(int(TAG_read))==str(int(TAG)):
                        return
                    hint("! ERREUR ECRITURE  !",4)
                    sleep(1)
                    hint("",4)
        except:
            hint("!PROBLEME ECRITURE !",4)
            sleep(1)
            hint("",4)
def RFID_setArgent(montant):
    montant=("0"*8+str(max(0,montant)))[-8:]
    RFID_write(config.blockArgent,montant)
    RFID_write(config.blockHashArgent,CRYPT_hashage(int(montant)))
def RFID_getUID():
    while True:
        try:
            if RFID_presence():
                (status,uid)=MIFAREReader.MFRC522_Anticoll()
                if status==MIFAREReader.MI_OK:
                    MIFAREReader.MFRC522_SelectTag(uid)
                    return int(STRING_Tag(uid))
        except:
            pass
def RFID_resetCarte():
    RFID_setArgent(0)
    RFID_write(config.blockHashCodeGuinche,str(int(CRYPT_hashage(config.codeGuinche))))
    RFID_write(config.blockHashUID,str(int(CRYPT_hashage(RFID_getUID()))))