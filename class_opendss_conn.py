import opendssdirect
import platform

if platform.system() == "Windows":
    import win32com.client

class C_OpenDSS_Conn(): # classe OpenDSS com métodos virtuais

    def __init__(self):
        self.FileOpenDSS = ''

    @classmethod
    def run(cls, argFileMsg):
        pass

    def Topology_AllIsolatedBranches(self):
        return self.engineTopology.AllIsolatedBranches()

    def Circuit_AllBusVMag(self):
        return self.engineCircuit.AllBusVMag()

    def Circuit_AllNodeVmagPUByPhase(self, phase):
        return self.engineCircuit.AllNodeVmagPUByPhase(phase)

    def Circuit_AllNodeVmagByPhase(self, phase):
        return self.engineCircuit.AllNodeVmagByPhase(phase)

    #Acesso a classe EnergyMeter

    def EnergyMeter_AllNames(self):
        return self.engineMeters.AllNames()

    def EnergyMeter_AllElementNames(self):
        return self.engineCircuit.AllElementNames()

    def EnergyMeter_ResetAll(self):
        return self.run("Show losses")


class C_OpenDSSDirect_Conn(C_OpenDSS_Conn):  # classe OpenDSSDirect

    def __init__(self):
        self.engine = opendssdirect
        self.engineCircuit = self.engine.Circuit
        self.engineTopoly = self.engine.Topology
        self.engineMeters = self.engine.Meters

    def run(self, msg):
        self.engine.run_command(msg)

    def Circuit_AllBusNames(self):
        return self.engineCircuit.AllBusNames()

    def Circuit_AllBusVolts(self):
        return self.engineCircuit.AllBusVolts()


class C_OpenDSSCOM_Conn(C_OpenDSS_Conn):  # classe OpenDSSCOM

    def __init__(self):
        # start an embedded DSS engine through COM
        # note: OpenDSSEngine.dll must already be registered
        self.engine = win32com.client.Dispatch("OpenDSSEngine.DSS")
        self.engine.Start("0")
        # use the Text interface to OpenDSS
        self.engine.Text.Command = "clear"
        self.engineCircuit = self.engine.ActiveCircuit

    def run(self, msg):
        self.engine.Text.Command = msg

    def Circuit_AllBusNames(self):
        return self.engineCircuit.AllBusNames

    def Circuit_AllBusVolts(self):
        return self.engineCircuit.AllBusVolts


