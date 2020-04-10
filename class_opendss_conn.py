import opendssdirect

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
        opendssdirect.run_command(msg)

    def Circuit_AllBusNames(self):
        return opendssdirect.Circuit.AllBusNames()

    def Topology_AllIsolatedBranches(self):
        return opendssdirect.Topology.AllIsolatedBranches()

    def Circuit_AllBusVolts(self):
        return opendssdirect.Circuit.AllBusVolts()

    def Circuit_AllBusVMag(self):
        return opendssdirect.Circuit.AllBusVMag()

    def Circuit_AllNodeVmagPUByPhase(self, phase):
        return opendssdirect.Circuit.AllNodeVmagPUByPhase(phase)

    def Circuit_AllNodeVmagByPhase(self, phase):
        return opendssdirect.Circuit.AllNodeVmagByPhase(phase)

class C_OpenDSSCOM_Conn(C_OpenDSS_Conn):  # classe OpenDSSCOM

    def __init__(self):
        pass

