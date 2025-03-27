import clr
clr.AddReference(".\\instruments\\topas\\NET_SDK\\Topas4Lib")
import Mint
from Topas4Lib import TopasDevice

class Topas:
    topas = None
    interaction = None
    wavelength = None
    shutter = False
    _interactions = {}

    def __init__(self, serialNumber):
        self.topas = TopasDevice.FindTopasDevice(serialNumber)
        if self.topas is None:
            print('Device with serial number %s not found' % serialNumber)
        else:
            print(f"Connected to {serialNumber}.")
            self.interaction = self.topas.WavelengthService.GetOutputInteraction()
            self.wavelength = self.topas.WavelengthService.GetOutput().Wavelength
            self.shutter = self.topas.ShutterService.GetIsShutterOpen()
            for item in self.topas.WavelengthService.GetExpandedInteractions():
                self._interactions[item.Type] = [item.OutputRange.From, item.OutputRange.To]

    def set_interaction(self, interaction):
        if interaction in self._interactions.keys():
            self.interaction = interaction
            print(f"Interaction set to {interaction}, you can set wavelength from {self._interactions[self.interaction][0]} nm to {self._interactions[self.interaction][1]} nm.")
            print("Please check the manual options and set a valid wavelength to update topas.")
            return True
        else:
            print(f"Not such a interaction named {interaction}.")
            return False

    def set_wavelength(self, wavelength):
        if self.interaction != None:
            if self._interactions[self.interaction][0] <= wavelength <= self._interactions[self.interaction][1]:
                self.wavelength = wavelength
                print(f"Wavelength is setting to {wavelength}...")
                self.topas.SetWavelength(self.wavelength, self.interaction)
                self.waitTillWavelengthIsSet()
                print(f"Wavelength set to {wavelength}.")
                return True
            else:
                print("Wavelength is out of range.")
                return False

    def changeShutter(self):
        if self.shutter:
            self.topas.ShutterService.SetShutterClose()
            self.shutter = False
        else:
            self.topas.ShutterService.SetShutterOpen()
            self.shutter = True

    def waitTillWavelengthIsSet(self):
        while (True):
            s = self.topas.WavelengthService.GetOutput()
            # sys.stdout.write("\r %d %% done" % (s.WavelengthSettingCompletionPart * 100.0))
            if s.IsWavelengthSettingInProgress == False or s.IsWaitingForUserAction:
                break
            options = Mint.Services.FinishSettingWavelengthOptions()
            options.RestoreShutter = False
            self.topas.WavelengthService.FinishWavelengthSettingAfterUserActions(options)

if __name__ == "__main__":
    serialNumber = "T23231P-Demo-7069"
    topas = Topas(serialNumber)
    topas.set_interaction('IDL')
    topas.set_wavelength(2000)