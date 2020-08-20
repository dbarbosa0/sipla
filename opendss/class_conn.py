import opendssdirect
import platform
import unidecode


if platform.system() == "Windows":
    import win32com.client

class C_Conn(): # classe OpenDSS com métodos virtuais

    def __init__(self):
        self.FileOpenDSS = ''

    ##Funções Iguais
    def get_Topology_AllIsolatedBranches(self):
        return self.engineTopology.AllIsolatedBranches()

    def get_Circuit_AllBusVMag(self):
        return self.engineCircuit.AllBusVMag()

    def get_Circuit_AllNodeVmagPUByPhase(self, phase):
        return self.engineCircuit.AllNodeVmagPUByPhase(phase)

    def get_Circuit_AllNodeVmagByPhase(self, phase):
        return self.engineCircuit.AllNodeVmagByPhase(phase)

    def get_MonitorActive_DataChannel(self, idx):
        return self.engineMonitors.Channel(idx)
    #Testes


class C_OpenDSSDirect_Conn(C_Conn):  # classe OpenDSSDirect

    def __init__(self):
        self.engine = opendssdirect
        self.engineBasic = self.engine.Basic
        self.engineCircuit = self.engine.Circuit
        self.engineTopoly = self.engine.Topology
        self.engineMeters = self.engine.Meters
        self.engineMonitors = self.engine.Monitors
        self.engineSolution = self.engine.Solution
        self.engineLoads = self.engine.Loads

    def run(self, msg):
        self.engine.run_command(unidecode.unidecode(msg))

    def clear(self):
        self.engineBasic.ClearAll()

    def get_Circuit_AllBusNames(self):
        return self.engineCircuit.AllBusNames()

    def get_Circuit_AllBusVolts(self):
        return self.engineCircuit.AllBusVolts()

    def get_Solution_ProcessTime(self):
        return self.engineSolution.ProcessTime()

    def get_Monitor_AllNames(self):
        return self.engineMonitors.AllNames()

    def get_EnergyMeter_AllNames(self):
        return self.engineMeters.AllNames()

    def get_Circuit_AllElementNames(self):
        return self.engineCircuit.AllElementNames()

    def set_MonitorActive(self, name):
        self.engineMonitors.Name(name)

    def set_EnergyMeterActive(self, name):
        self.engineMeters.Name(name)

    def get_MonitorActive_ChannelNames(self):
        return self.engineMonitors.Header()

    def get_RegisterNames(self):
        return self.engineMeters.RegisterNames()
    def get_RegisterValues(self):
        return self.engineMeters.RegisterValues()

################


class C_OpenDSSCOM_Conn(C_Conn):  # classe OpenDSSCOM

    def __init__(self):
        # start an embedded DSS engine through COM
        # note: OpenDSSEngine.dll must already be registered
        self.engine = win32com.client.Dispatch("OpenDSSEngine.DSS")
        self.engine.Start("0")
        # use the Text interface to OpenDSS
        self.engine.Text.Command = "clear"
        self.engineCircuit = self.engine.ActiveCircuit
        self.engineSolution = self.engineCircuit.Solution
        self.engineMeters = self.engineCircuit.Meters
        self.engineMonitors = self.engineCircuit.Monitors

    def run(self, msg):
        self.engine.Text.Command = unidecode.unidecode(msg)

    def clear(self):
        self.run("clear")

    def get_Circuit_AllBusNames(self):
        return self.engineCircuit.AllBusNames

    def get_Circuit_AllBusVolts(self):
        return self.engineCircuit.AllBusVolts

    def get_Solution_ProcessTime(self):
        return self.engineSolution.Process_Time

    def get_Monitor_AllNames(self):
        return self.engineMonitors.AllNames

    def get_EnergyMeter_AllNames(self):
        return self.engineMeters.AllNames

    def get_Circuit_AllElementNames(self):
        return self.engineCircuit.AllElementNames

    def set_MonitorActive(self, name):
        self.engineMonitors.Name = name

    def set_EnergyMeterActive(self, name):
        self.engineMeters.Name = name

    def get_MonitorActive_ChannelNames(self):
        return self.engineMonitors.Header




