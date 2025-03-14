# Add needed dll references
import os
import sys
import time
import numpy as np

from pyexpat.errors import messages

sys.path.append(os.environ['LIGHTFIELD_ROOT'])
sys.path.append(os.environ['LIGHTFIELD_ROOT']+"\\AddInViews")
import clr
clr.AddReference('PrincetonInstruments.LightFieldViewV5')
clr.AddReference('PrincetonInstruments.LightField.AutomationV5')
clr.AddReference('PrincetonInstruments.LightFieldAddInSupportServices')

# Import System.IO for saving and opening files
from System.IO import *
# Import c compatible List and String
from System import String
from System.Collections.Generic import List

# PI imports
from PrincetonInstruments.LightField.Automation import Automation
from PrincetonInstruments.LightField.AddIns import DeviceType, ExperimentSettings, CameraSettings, RegionOfInterest, AdcQuality, SpectrometerSettings

class LightFieldApp():
    def __init__(self, experiment: str = None, interface=True):
        self.auto = None
        self.experiment = None
        self.counts = 0
        try:
            self.auto = Automation(interface, List[String]())
            self.experiment = self.auto.LightFieldApplication.Experiment
            if not experiment is None:
                self.experiment.Load(experiment)
            print(f"Successfully loaded experiment {self.experiment.Name}.")
        except Exception as err:
            print(err)
    def close(self):
        print('Releasing LightFieldApp object...')
        # self.auto.Dispose()
        if not self.auto is None:
            print("Closing App...")
            if not self.auto.IsDisposed:
                self.auto.Dispose()
            print("LightField app has been closed.")
    def set_value(self, setting, value):
        if self.experiment.Exists(setting):
            self.experiment.SetValue(setting, value)
            print(f"{setting} set to {value}.")
            return True
        else:
            print(f"{setting} is not a valid setting.")
            return False
    def save_data(self):
        pass
    def frames(self, frame_num):
        self.set_value(ExperimentSettings.AcquisitionFramesToStore, float(frame_num))
    def exposure(self, exposure_time):
        self.set_value(CameraSettings.ShutterTimingExposureTime, float(exposure_time))
    def em_gain(self, multiple):
        if (self.set_value(CameraSettings.AdcQuality, AdcQuality.ElectronMultiplied)):
            self.set_value(CameraSettings.AdcSpeed, float(8.0))
            if 1 <= multiple <= 100:
                self.set_value(CameraSettings.AdcEMGain, float(multiple))
            else:
                print("EM Gain must be within [1, 100].")
        else:
            print("AdcQuality failed to set to ElectronMultiplied, check the device and the application.")
    def roi(self, mode):
        if mode in [1, 2, 3, 4]:
            self.set_value(CameraSettings.ReadoutControlRegionsOfInterestSelection, float(mode))
        else:
            print("ROI mode must be with in [1, 2, 3, 4].")
    def grating(self, density):
        if density == 1800:
            self.set_value(SpectrometerSettings.Grating, '[500nm,1800][0][0]')
        elif density == 1200:
            self.set_value(SpectrometerSettings.Grating, '[500nm,1200][1][0]')
        elif density == 150:
            self.set_value(SpectrometerSettings.Grating, '[500nm,150][2][0]')
        else:
            print(f"No grating with Density of {density} g/mm, give a density within 150, 1200 and 1800.")
    def center_wavelength(self, wv):
        self.set_value(SpectrometerSettings.GratingCenterWavelengt, float(wv))
    def acquire(self):
        pass
    def clean(self):
        self.counts = 0

class LightFieldSimplestApp():
    def __init__(self, experiment: str = None, interface=True):
        self.auto = None
        self.experiment = None
        self.counts = 0
        # self.savedir = self.experiment.GetValue(ExperimentSettings.FileNameGenerationDirectory)
        try:
            self.auto = Automation(interface, List[String]())
            self.experiment = self.auto.LightFieldApplication.Experiment
            if not experiment is None:
                self.experiment.Load(experiment)
            print(f"Successfully loaded experiment {self.experiment.Name}.")
        except Exception as err:
            print(err)
    def close(self):
        print('Releasing LightFieldApp object...')
        # self.auto.Dispose()
        if not self.auto is None:
            print("Closing App...")
            if not self.auto.IsDisposed:
                self.auto.Dispose()
            print("LightField app has been closed.")
    def get_dir(self):
        return self.experiment.GetValue(ExperimentSettings.FileNameGenerationDirectory)
    def acquire(self, path="C:\\Users\\zhenggroup\\Documents\\LightField"):
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationDirectory, path)
        filename = str(self.counts).zfill(5)
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, filename)
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationAttachIncrement, False)
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationAttachDate, False)
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationAttachTime, False)
        if self.experiment.IsReadyToRun:
            self.experiment.Acquire()
            time.sleep(self.acquire_time())
            data = self.frame_avg()
            message = "Image {num} saved to {path}".format(num=filename, path=self.get_dir())
            print(message)
            self.counts = self.counts + 1
            return data, message
        else:
            message = "Devices is not ready."
            print(message)
            return np.zeros((1600,2)), message
    def acquire_time(self):
        frames = self.experiment.GetValue(ExperimentSettings.AcquisitionFramesToStore)
        exposure = self.experiment.GetValue(CameraSettings.ShutterTimingExposureTime)
        return float(frames)*(float(exposure)*0.001+0.1)+2
    def frame_avg(self):
        filelist = os.listdir(self.get_dir())
        csvlist = []
        for file in filelist:
            if str(self.counts).zfill(5) in file and '.csv' in file:
                csvlist.append(file)
        data = np.zeros((1600, 2))
        frame_num = 0
        for file in csvlist:
            data = data + np.loadtxt(self.get_dir() + '\\' + file, delimiter=',')
            frame_num = frame_num + 1
        data = data / frame_num
        np.savetxt(self.get_dir() + '\\' + str(self.counts).zfill(5) + '.csv', data, delimiter=',')
        return data
    def clean(self):
        self.counts = 0
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, '')

if __name__ == '__main__':
    app = LightFieldSimplestApp()
    app.acquire()
    app.close()
