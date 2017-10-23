# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>
#
# ##### END GPL LICENSE BLOCK #####

from .PicoHarpComponents import Component
import sys
from taurus.core.util import argparse
from taurus.external.qt import Qt, QtGui
from taurus import Logger
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.taurusgui import TaurusGui
from .widgets import *

__author__ = "Sergi Blanch-Torne"
__copyright__ = "Copyright 2014, CELLS / ALBA Synchrotron"
__license__ = "GPLv3+"

# The version is updated automatically with bumpversion
# Do not update manually
__version = '1.1.1-alpha'

DEVICESERVERNAME = 'PH_PhotonCounter'
MODELS = 'models'
TYPE = 'type'


class MainWindow(TaurusGui):
    def __init__(self, parent=None):
        TaurusGui.__init__(self)
        self._components = None
        self.initComponents()
        self.prepareJorgsBar()
        self.loadDefaultPerspective()
        self.splashScreen().finish(self)

    panels = {'Histogram': {MODELS: ['Histogram'],
                            TYPE: HistogramPlot},
              'Channel0': {MODELS: ['ZeroCrossCh0', 'LevelCh0', 'syncdivider'],
                           TYPE: Channel0Form},
              'Channel1': {MODELS: ['ZeroCrossCh1', 'LevelCh1'],
                           TYPE: Channel1Form},
              'Acquisition': {MODELS: ['Resolution', 'binning', 'offset',
                                       'AcquisitionTime', 'ElapsedMeasTime',
                                       'OverflowStopper',
                                       'OverflowStopperThreshold'],
                              TYPE: AcquisitionForm},
              'Monitor': {MODELS: ['CountRateCh0', 'CountRateCh1',
                                   'IntegralCount', 'HistogramMaxValue'],
                          TYPE: MonitorForm},
              'Status': {MODELS: ['State', 'Status', 'Warnings'],
                         TYPE: StateForm},
              'Commands': {TYPE: PhCtCommands}
              }

    def initComponents(self):
        self._components = {}
        for panel in self.panels:
            self.splashScreen().showMessage("Building %s panel" % (panel))
            if MODELS in self.panels[panel]:
                attrNames = self.panels[panel][MODELS]
                haveCommands = False
            else:
                attrNames = None
                haveCommands = True
            if TYPE in self.panels[panel]:
                widget = self.panels[panel][TYPE]
            else:
                widget = None  # FIXME
            self._components[panel] = \
                Component(self, name=panel, widget=widget, attrNames=attrNames,
                          haveCommands=haveCommands)
        self._selectorComponent()

    def prepareJorgsBar(self):
        # Eliminate one of the two taurus icons
        self.jorgsBar.removeAction(self.jorgsBar.actions()[0])

    def loadDefaultPerspective(self):
        try:
            self.loadPerspective(name='default')
        except:
            QtGui.QMessageBox.\
                warning(self, "No default perspective",
                        "Please, save a perspective with the name "
                        "'default' to be used when launch")

    def _selectorComponent(self):
        self.splashScreen().showMessage("Building device selector")
        # create a TaurusDevCombo
        self._selector = TaurusDevCombo(self)
        # populate the combo
        self.splashScreen().showMessage("Searching for %s device servers"
                                        % (DEVICESERVERNAME))
        self._selector.setModel(DEVICESERVERNAME)
        self.splashScreen().\
            showMessage("Found %s device servers"
                        % (self._selector.getSelectedDeviceName()))
        # attach it to the toolbar
        self.selectorToolBar = self.addToolBar("Model:")
        self.selectorToolBar.setObjectName("selectorToolBar")
        self.viewToolBarsMenu.\
            addAction(self.selectorToolBar.toggleViewAction())
        self.selectorToolBar.addWidget(self._selector)
        # subscribe model change
        self._modelChange()
        self._selector.modelChosen.connect(self._modelChange)

    def _modelChange(self):
        newModel = self._selector.getSelectedDeviceName()
        if newModel != self.getModel():
            self.debug("Model has changed from %r to %r"
                       % (self.getModel(), newModel))
            self.setModel(newModel)
            for component in self._components.keys():
                self._components[component].devName = newModel


def main():
    parser = argparse.get_taurus_parser()
    parser.add_option("--model")
    app = TaurusApplication(sys.argv, cmd_line_parser=parser,
                            app_name='ctdiPicoHarp300', app_version=__version,
                            org_domain='ALBA', org_name='ALBA')
    options = app.get_command_line_options()
    ui = MainWindow()
    if options.model is not None:
        ui.setModel(options.model)
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
