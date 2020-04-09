import opendssdirect as dss

class C_OpenDSS_Conn(): # classe OpenDSS com métodos virtuais

    def __init__(self):
        self.FileOpenDSS = ''

    @classmethod
    def run(cls, argFileMsg):
        pass

    @classmethod
    def AllBusNames(cls):
        pass


class C_OpenDSSDirect_Conn(C_OpenDSS_Conn):  # classe OpenDSSDirect

    def __init__(self):
        pass

    def run(self, msg):
        dss.run_command(msg)

    def AllBusNames(self):
        return dss.Circuit.AllBusNames()

class C_OpenDSSCOM_Conn(C_OpenDSS_Conn):  # classe OpenDSSCOM

    def __init__(self):
        pass

