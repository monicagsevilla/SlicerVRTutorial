import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

#
# VRTutorial
#

class VRTutorial(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "VRTutorial"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#VRTutorial">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""

    # Additional initialization step after application startup is complete
    slicer.app.connect("startupCompleted()", registerSampleData)

#
# Register sample data sets in Sample Data module
#

def registerSampleData():
  """
  Add data sets to Sample Data module.
  """
  # It is always recommended to provide sample data for users to make it easy to try the module,
  # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

  import SampleData
  iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

  # To ensure that the source code repository remains small (can be downloaded and installed quickly)
  # it is recommended to store data sets that are larger than a few MB in a Github release.

  # VRTutorial1
  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='VRTutorial',
    sampleName='VRTutorial1',
    # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
    # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
    thumbnailFileName=os.path.join(iconsPath, 'VRTutorial1.png'),
    # Download URL and target file name
    uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
    fileNames='VRTutorial1.nrrd',
    # Checksum to ensure file integrity. Can be computed by this command:
    #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
    checksums = 'SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95',
    # This node name will be used when the data set is loaded
    nodeNames='VRTutorial1'
  )

  # VRTutorial2
  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='VRTutorial',
    sampleName='VRTutorial2',
    thumbnailFileName=os.path.join(iconsPath, 'VRTutorial2.png'),
    # Download URL and target file name
    uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
    fileNames='VRTutorial2.nrrd',
    checksums = 'SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97',
    # This node name will be used when the data set is loaded
    nodeNames='VRTutorial2'
  )

#
# VRTutorialWidget
#

class VRTutorialWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False
    self.tutorialPart = 1
    self.info_display = False

    self.instructionsPath = slicer.modules.vrtutorial.path.replace("VRTutorial.py","") + 'Resources/Instructions/'





  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/VRTutorial.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)
    
    #
    # Setup view
    #
    # show 3D View
    self.layoutManager= slicer.app.layoutManager()
    # self.layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
    # set layout
    self.setCustomLayout()
    self.layoutManager.setLayout(self.customLayout_1_ID) # Set 3D only view layout
    # quit box and axis
    view = slicer.util.getNode('View1')
    view.SetBoxVisible(0)
    view.SetAxisLabelsVisible(0)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    uiWidget.setMRMLScene(slicer.mrmlScene)

    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = VRTutorialLogic()

    # Add controllers instructions image (HTC by default)
    self.markerSelectedIconPixmap = qt.QPixmap(self.instructionsPath + 'HTCControllers.png')
    self.ui.controllerInstructionsImage.setPixmap(self.markerSelectedIconPixmap)
    self.ui.controllerInstructionsImage.scaledContents = True
    self.ui.controllerInstructionsImage.visible = True

    # Connections

    # These connections ensure that we update parameter node when scene is closed
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

    # These connections ensure that whenever user changes some settings on the GUI, that is saved in the MRML scene
    # (in the selected parameter node).
    self.ui.loadTutorialDataButton.connect('clicked(bool)', self.onLoadTutorialData)
    self.ui.createConnectionButton.connect('clicked(bool)', self.onSwitchVirtualRealityActivation)
    self.ui.startTutorialButton.connect('clicked(bool)', self.onStartTutorial)
    self.ui.showInstructionsButton.clicked.connect(self.onShowInstructionsButtonClicked)
    self.ui.nextButton.connect('clicked(bool)', self.onNextButtonClicked)
    self.ui.previousButton.connect('clicked(bool)', self.onPreviousButtonClicked)

    # Settings
    self.ui.controllersVisibilityCheckBox.toggled.connect(self.onControllerVisibilityCheckBoxClicked)
    self.ui.resetVRViewButton.connect('clicked(bool)', self.onResetVRViewButtonClicked)


    self.ui.HTCRadioButton.connect('clicked(bool)', self.onControllerSelected)
    self.ui.OculusRadioButton.connect('clicked(bool)', self.onControllerSelected)
    self.ui.HPRadioButton.connect('clicked(bool)', self.onControllerSelected)



    # Make sure parameter node is initialized (needed for module reload)
    self.initializeParameterNode()

  def cleanup(self):
    """
    Called when the application closes and the module widget is destroyed.
    """
    self.removeObservers()

  def enter(self):
    """
    Called each time the user opens this module.
    """
    # Make sure parameter node exists and observed
    self.initializeParameterNode()

  def exit(self):
    """
    Called each time the user opens a different module.
    """
    # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
    self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

  def onSceneStartClose(self, caller, event):
    """
    Called just before the scene is closed.
    """
    # Parameter node will be reset, do not use it anymore
    self.setParameterNode(None)

  def onSceneEndClose(self, caller, event):
    """
    Called just after the scene is closed.
    """
    # If this module is shown while the scene is closed then recreate a new parameter node immediately
    if self.parent.isEntered:
      self.initializeParameterNode()

  def initializeParameterNode(self):
    """
    Ensure parameter node exists and observed.
    """
    # Parameter node stores all user choices in parameter values, node selections, etc.
    # so that when the scene is saved and reloaded, these settings are restored.

    self.setParameterNode(self.logic.getParameterNode())

    # Select default input nodes if nothing is selected yet to save a few clicks for the user
    if not self._parameterNode.GetNodeReference("InputVolume"):
      firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
      if firstVolumeNode:
        self._parameterNode.SetNodeReferenceID("InputVolume", firstVolumeNode.GetID())

  def setParameterNode(self, inputParameterNode):
    """
    Set and observe parameter node.
    Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
    """

    if inputParameterNode:
      self.logic.setDefaultParameters(inputParameterNode)

    # Unobserve previously selected parameter node and add an observer to the newly selected.
    # Changes of parameter node are observed so that whenever parameters are changed by a script or any other module
    # those are reflected immediately in the GUI.
    if self._parameterNode is not None:
      self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
    self._parameterNode = inputParameterNode
    if self._parameterNode is not None:
      self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    # Initial GUI update
    self.updateGUIFromParameterNode()

  def updateGUIFromParameterNode(self, caller=None, event=None):
    """
    This method is called whenever parameter node is changed.
    The module GUI is updated to show the current state of the parameter node.
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
    self._updatingGUIFromParameterNode = True

    # Update node selectors and sliders
    # self.ui.inputSelector.setCurrentNode(self._parameterNode.GetNodeReference("InputVolume"))
    # self.ui.outputSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolume"))
    # self.ui.invertedOutputSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolumeInverse"))
    # self.ui.imageThresholdSliderWidget.value = float(self._parameterNode.GetParameter("Threshold"))
    # self.ui.invertOutputCheckBox.checked = (self._parameterNode.GetParameter("Invert") == "true")

    # if self._parameterNode.GetNodeReference("InputVolume") and self._parameterNode.GetNodeReference("OutputVolume"):
    #   self.ui.applyButton.toolTip = "Compute output volume"
    #   self.ui.applyButton.enabled = True
    # else:
    #   self.ui.applyButton.toolTip = "Select input and output volume nodes"
    #   self.ui.applyButton# Update buttons states and tooltips
    # .enabled = False

    # All the GUI updates are done
    self._updatingGUIFromParameterNode = False

  def updateParameterNodeFromGUI(self, caller=None, event=None):
    """
    This method is called when the user makes any change in the GUI.
    The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch

    # self._parameterNode.SetNodeReferenceID("InputVolume", self.ui.inputSelector.currentNodeID)
    # self._parameterNode.SetNodeReferenceID("OutputVolume", self.ui.outputSelector.currentNodeID)
    # self._parameterNode.SetParameter("Threshold", str(self.ui.imageThresholdSliderWidget.value))
    # self._parameterNode.SetParameter("Invert", "true" if self.ui.invertOutputCheckBox.checked else "false")
    # self._parameterNode.SetNodeReferenceID("OutputVolumeInverse", self.ui.invertedOutputSelector.currentNodeID)

    self._parameterNode.EndModify(wasModified)

  def onSwitchVirtualRealityActivation(self):
    modulesInstalled = self.logic.checkInstallationRequiredModules()
    if not modulesInstalled:
      self.ui.statusText.text = "Please install SlicerVR and IGT extensions"
      return
    connected = self.logic.activateVirtualReality()
    if connected:
      # modify button text and show connection status
      wr = slicer.modules.virtualreality.widgetRepresentation()
      label = slicer.util.findChild(wr, 'ConnectionStatusLabel').text
      self.ui.statusText.text = label
      self.ui.createConnectionButton.setText("Deactivate VR")
      self.ui.startTutorialButton.enabled = True
      self.logic.loadModels()
      self.logic.loadInstructions()
      self.logic.applyTransformsToAvatars()
    else:
      self.ui.createConnectionButton.setText("Activate VR")
      self.ui.statusText.text = ''    

    if not self.logic.slicerVRinstalled:
      self.ui.statusText.text = 'install SlicerVR extension'

  def onLoadTutorialData(self):
    # load scenario
    self.logic.loadScenario()
    self.logic.adjustViewpoint()
    self.ui.createConnectionButton.enabled = True


  def onStartTutorial(self):
    print("starting tutorial")
    self.logic.applyTransformsToAvatars()
    self.onShowInstructionsButtonClicked()
    if self.tutorialPart == 1:
      self.logic.startPart1()
    elif self.tutorialPart == 2:
      self.logic.startPart2()


  ## Layout
  def setCustomLayout(self):
      layoutLogic = self.layoutManager.layoutLogic()
      customLayout_1 = ("<layout type=\"horizontal\">"
      " <item>"
      "  <view class=\"vtkMRMLViewNode\" singletontag=\"1\">"
      "   <property name=\"viewlabel\" action=\"default\">1</property>"
      "  </view>"
      " </item>"
      "</layout>")
      customLayout_2 = ("<layout type=\"horizontal\" split=\"true\">"
      " <item>"
      "  <layout type=\"vertical\">"
      "   <item>"
      "    <view class=\"vtkMRMLSliceNode\" singletontag=\"Yellow\">"
      "     <property name=\"orientation\" action=\"default\">Axial</property>"
      "     <property name=\"viewlabel\" action=\"default\">Y</property>"
      "     <property name=\"viewcolor\" action=\"default\">#F34A33</property>"
      "    </view>"
      "   </item>"
      "   <item>"
      "    <view class=\"vtkMRMLSliceNode\" singletontag=\"Green\">"
      "     <property name=\"orientation\" action=\"default\">Coronal</property>"
      "     <property name=\"viewlabel\" action=\"default\">G</property>"
      "     <property name=\"viewcolor\" action=\"default\">#F34A33</property>"
      "    </view>"
      "   </item>"
      "  </layout>"
      " </item>"
      " <item>"
      "  <view class=\"vtkMRMLViewNode\" singletontag=\"1\">"
      "  <property name=\"viewlabel\" action=\"default\">T</property>"
      "  </view>"
      " </item>"
      "</layout>")
      customLayout_3 = ("<layout type=\"horizontal\">"
      " <item>"
      "  <view class=\"vtkMRMLSliceNode\" singletontag=\"Red\">"
      "   <property name=\"orientation\" action=\"default\">Axial</property>"
      "     <property name=\"viewlabel\" action=\"default\">R</property>"
      "     <property name=\"viewcolor\" action=\"default\">#F34A33</property>"
      "  </view>"
      " </item>"
      "</layout>")
      self.customLayout_1_ID=996
      self.customLayout_2_ID=997
      self.customLayout_3_ID=998
      layoutLogic.GetLayoutNode().AddLayoutDescription(self.customLayout_1_ID, customLayout_1)
      layoutLogic.GetLayoutNode().AddLayoutDescription(self.customLayout_2_ID, customLayout_2)
      layoutLogic.GetLayoutNode().AddLayoutDescription(self.customLayout_3_ID, customLayout_3)

  # INFORMATION
  def onShowInstructionsButtonClicked(self):

    # Update layout to show or hide info
    if self.info_display:
        self.layoutManager.setLayout(self.customLayout_1_ID) # Set 3D view only layout
        self.info_display = False
        self.ui.showInstructionsButton.setText('Show Instructions')
    else:
        self.layoutManager.setLayout(self.customLayout_3_ID) # Set red slice view layout
        self.info_display = True
        self.ui.showInstructionsButton.setText('Hide Instructions')
        self.logic.red_logic.FitSliceToAll()
        self.logic.red_logic.SetSliceOffset(0)

  def onPreviousButtonClicked(self):
    self.logic.hideSuccessMessage()
    self.onShowInstructionsButtonClicked()
    self.logic.changeInfoSlide('PREVIOUS')

  def onNextButtonClicked(self):
    self.logic.hideSuccessMessage()
    self.onShowInstructionsButtonClicked()
    self.logic.changeInfoSlide('NEXT')
    
  def onControllerVisibilityCheckBoxClicked(self):
    logging.debug('change controller visibility')
    if self.ui.controllersVisibilityCheckBox.checked:
      self.logic.changeControllerVisibility(True)
    else:
      self.logic.changeControllerVisibility(False)

  def onResetVRViewButtonClicked(self):
    logging.debug('reset VR view')
    # zoomOut = 100
    self.logic.resetVRView()
    

  def onControllerSelected(self):

    if self.ui.HTCRadioButton.isChecked():
      self.controllerSelectedIconPixmap = qt.QPixmap(self.instructionsPath + 'HTCControllers.png')
      self.ui.controllerInstructionsImage.setPixmap(self.controllerSelectedIconPixmap)
      self.ui.controllerInstructionsImage.scaled()
      self.controllerSelected = "HTC"

    if self.ui.OculusRadioButton.isChecked():
      self.controllerSelectedIconPixmap = qt.QPixmap(self.instructionsPath + 'OculusControllers.png')
      self.ui.controllerInstructionsImage.setPixmap(self.controllerSelectedIconPixmap)
      self.ui.controllerInstructionsImage.scaled()
      self.controllerSelected = "Oculus"

    if self.ui.HPRadioButton.isChecked():
      self.controllerSelectedIconPixmap = qt.QPixmap(self.instructionsPath + '/HPControllers.png')
      self.ui.controllerInstructionsImage.setPixmap(self.controllerSelectedIconPixmap)
      self.ui.controllerInstructionsImage.scaled()
      self.controllerSelected = "HP"


#
# VRTutorialLogic
#

class VRTutorialLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)
    self.vrEnabled = False
    self.threeDView = slicer.app.layoutManager().threeDWidget(0).threeDView()
    self.instructionsImagesVisible = False
    self.slicerVRinstalled = False
    try:
      self.vrLogic = slicer.modules.virtualreality.logic()
      self.slicerVRinstalled = True
    except:
      self.slicerVRinstalled = False

    # CREATE PATHS
    self.modelsPath = slicer.modules.vrtutorial.path.replace("VRTutorial.py","") + 'Resources/Models/'
    self.transformsPath = slicer.modules.vrtutorial.path.replace("VRTutorial.py","") + 'Resources/Transforms/'
    self.instructionsPath = slicer.modules.vrtutorial.path.replace("VRTutorial.py","") + 'Resources/Instructions/'

    # Viewpoint module (SlicerIGT extension)
    self.slicerIGTinstalled = False
    try:
      import Viewpoint # Viewpoint Module must have been added to Slicer 
      self.viewpointLogic = Viewpoint.ViewpointLogic()
      self.slicerIGTinstalled = True
    except:
      self.slicerIGTinstalled = False
      logging.error('ERROR: "Viewpoint" module was not found.')

    # Info
    self.red_logic = slicer.app.layoutManager().sliceWidget("Red").sliceLogic()
    


  def setDefaultParameters(self, parameterNode):
    """
    Initialize parameter node with default settings.
    """
    if not parameterNode.GetParameter("Threshold"):
      parameterNode.SetParameter("Threshold", "100.0")
    if not parameterNode.GetParameter("Invert"):
      parameterNode.SetParameter("Invert", "false")


  def checkInstallationRequiredModules(self):
    if not self.slicerIGTinstalled:
      print("IGT extension missing")
      return False
    if not self.slicerVRinstalled:
      print("SlicerVR extension missing")
      return False
    else:
      print("All required modules are installed")
      return True


  def activateVirtualReality(self):
    if (self.vrEnabled):
      self.vrLogic.SetVirtualRealityConnected(False)
      self.vrEnabled = False
      return False
    else:
      self.vrLogic.SetVirtualRealityConnected(True)    
      vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
      vrViewNode.SetLighthouseModelsVisible(False)
      vrViewNode.SetControllerModelsVisible(False)

      # Just for being sure
      reference = slicer.app.layoutManager().threeDWidget(0).mrmlViewNode() # 3D View node
      vrViewNode.SetAndObserveReferenceViewNode(reference)
      slicer.modules.virtualreality.viewWidget().updateViewFromReferenceViewCamera()

      self.vrEnabled = True

      # Devices transforms visible to the scene
      vrViewNode.SetControllerTransformsUpdate(True)
      vrViewNode.SetHMDTransformUpdate(True)

      vrViewNode.Modified()
      
      self.vrLogic.SetVirtualRealityActive(True)

      return True

  
  def loadScenario(self):
    # load model and texture
    try:
      self.scenarioModel = slicer.util.getNode('ClinicalScenario_1')
    except:
      self.scenarioModel = slicer.util.loadModel(self.modelsPath + '/ClinicalScenario/ClinicalScenario_1.obj')
    try:
      self.scenarioTexture = slicer.util.getNode('ClinicalScenario1_Texture')
    except:
      self.scenarioTexture = slicer.util.loadVolume(self.modelsPath + '/ClinicalScenario/ClinicalScenario1_Texture.png')
    # apply texture
    self.showTextureOnModel(self.scenarioModel, self.scenarioTexture)
    # make it non selectable
    self.scenarioModel.SelectableOff()


  def loadModels(self):
    # load avatars
    try:
      self.headModel = slicer.util.getNode('Head')
    except:
      self.headModel = slicer.util.loadModel(self.modelsPath + 'Avatar/Head.vtk')
      self.headModel.GetModelDisplayNode().SetColor([0.8549019607843137, 0.7450980392156863, 0.5725490196078431])
    try:
      self.handRightModel = slicer.util.getNode('Hand_Right')
    except:
      self.handRightModel = slicer.util.loadModel(self.modelsPath + 'Avatar/Hand_Right.vtk')
      self.handRightModel.GetModelDisplayNode().SetColor([0,0,1])
    try:
      self.handLeftModel = slicer.util.getNode('Hand_Left')
    except:
      self.handLeftModel = slicer.util.loadModel(self.modelsPath + 'Avatar/Hand_Left.vtk')
      self.handLeftModel.GetModelDisplayNode().SetColor([1,0,0])
    
    # load interaction models
    try:
      self.cylinderModel = slicer.util.getNode('CylinderModel')
    except:
      self.cylinderModel = slicer.util.loadModel(self.modelsPath + 'CylinderModel.vtk')
      # self.cylinderModel.GetModelDisplayNode().SetColor([1,0,0])
      self.cylinderModel.GetModelDisplayNode().SetOpacity(0)
    try:
      self.femurModel = slicer.util.getNode('femurModel')
    except:
      self.femurModel = slicer.util.loadModel(self.modelsPath + 'femurModel.vtk')
      self.femurModel.GetModelDisplayNode().SetColor([0.94,0.84,0.57])
      self.femurModel.GetModelDisplayNode().SetOpacity(0)
    try:
      self.femurModelCopy = slicer.util.getNode('femurModelCopy')
    except:
      self.femurModelCopy = slicer.util.loadModel(self.modelsPath + 'femurModelCopy.vtk')
      self.femurModelCopy.GetModelDisplayNode().SetColor([0.94,0.84,0.57])
      self.femurModelCopy.GetModelDisplayNode().SetOpacity(0)

    # load text model
    try:
      self.successTextModel = slicer.util.getNode('SuccessTextModel')
    except:
      self.successTextModel = slicer.util.loadModel(self.modelsPath + 'SuccessTextModel.stl')
      self.successTextModel.GetModelDisplayNode().SetColor([0,1,0])
      self.successTextModel.GetModelDisplayNode().SetOpacity(0)


  def applyTransformsToAvatars(self):
    # apply transforms
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    try:
      self.HMDTransform = vrViewNode.GetHMDTransformNode()
      self.headModel.SetAndObserveTransformNodeID(self.HMDTransform.GetID())
    except:
      print("unable to get HMD transform")
    try:
      self.RightControllerTransform = vrViewNode.GetRightControllerTransformNode()
      self.handRightModel.SetAndObserveTransformNodeID(self.RightControllerTransform.GetID())
    except:
      print("unable to get Right controller transform")
    try:
      self.LeftControllerTransform = vrViewNode.GetLeftControllerTransformNode()
      self.handLeftModel.SetAndObserveTransformNodeID(self.LeftControllerTransform.GetID())
    except:
      print("unable to get Left controller transform")


  def showTextureOnModel(self, modelNode, textureImageNode):
    modelDisplayNode = modelNode.GetDisplayNode()
    modelDisplayNode.SetBackfaceCulling(0)
    textureImageFlipVert = vtk.vtkImageFlip()
    textureImageFlipVert.SetFilteredAxis(1)
    textureImageFlipVert.SetInputConnection(textureImageNode.GetImageDataConnection())
    modelDisplayNode.SetTextureImageDataConnection(textureImageFlipVert.GetOutputPort())


  def adjustViewpoint(self):

    self.scenarioViewPointTransform = self.loadTransformFromFile(self.transformsPath, 'StartCamera_1')

    # Get 3D view node
    threeDViewNode = slicer.app.layoutManager().threeDWidget(0).mrmlViewNode()

    # Disable bulleye mode if active
    bullseyeMode = self.viewpointLogic.getViewpointForViewNode(threeDViewNode).getCurrentMode()
    if bullseyeMode:
      self.viewpointLogic.getViewpointForViewNode(threeDViewNode).bullseyeStop()
    
    # Update viewpoint
    if self.scenarioViewPointTransform:
      self.viewpointLogic.getViewpointForViewNode(threeDViewNode).setViewNode(threeDViewNode)
      self.viewpointLogic.getViewpointForViewNode(threeDViewNode).bullseyeSetTransformNode(self.scenarioViewPointTransform)
      self.viewpointLogic.getViewpointForViewNode(threeDViewNode).bullseyeStart()
      self.viewpointLogic.getViewpointForViewNode(threeDViewNode).bullseyeStop()


  def loadTransformFromFile(self, transformFilePath, transformFileName):
    try:
        node = slicer.util.getNode(transformName)
    except:
        try:
          node = slicer.util.loadTransform(transformFilePath + transformFileName + '.h5')
        except:
          node=slicer.vtkMRMLLinearTransformNode()
          node.SetName(transformFileName)
          slicer.mrmlScene.AddNode(node)
          logging.error('ERROR: ' + transformFileName + ' transform not found in path. Creating node as identity...')
    return node
    

  def changeControllerVisibility(self, display):
    self.vrLogic.SetVirtualRealityConnected(True)    
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    vrViewNode.SetControllerModelsVisible(display)


  def resetVRView(self):
    slicer.modules.virtualreality.viewWidget().updateViewFromReferenceViewCamera()


  def hideSuccessMessage(self):
    self.successTextModel.GetModelDisplayNode().SetOpacity(0)


  def findMeshCollision(self, node1, node2, verbose=False ):
    '''
        Find Mesh Collision
            This function finds a collision or intersection between two surface meshesu=fluvio_lobo
    '''
    #
    # Variables
    collisionDetection = vtk.vtkCollisionDetectionFilter()
    numberOfCollisions = 0
    collisionFlag = False
    #
    # Collision Detection
    node1ToWorldTransformMatrix = vtk.vtkMatrix4x4()
    node2ToWorldTransformMatrix = vtk.vtkMatrix4x4()
    node1ParentTransformNode = node1.GetParentTransformNode()
    node2ParentTransformNode = node2.GetParentTransformNode()
    if node1ParentTransformNode != None:
        node1ParentTransformNode.GetMatrixTransformToWorld(node1ToWorldTransformMatrix)
    if node2ParentTransformNode != None:
        node2ParentTransformNode.GetMatrixTransformToWorld(node2ToWorldTransformMatrix)
    #
    collisionDetection.SetInputData( 0, node1.GetPolyData() )
    collisionDetection.SetInputData( 1, node2.GetPolyData() )
    collisionDetection.SetMatrix( 0, node1ToWorldTransformMatrix )
    collisionDetection.SetMatrix( 1, node2ToWorldTransformMatrix )
    collisionDetection.SetBoxTolerance( 0.0 )
    collisionDetection.SetCellTolerance( 0.0 )
    collisionDetection.SetNumberOfCellsPerNode( 2 )
    collisionDetection.Update()
    #
    numberOfCollisions = collisionDetection.GetNumberOfContacts()
    if numberOfCollisions > 0:
        collisionFlag = True
    else:
        collisionFlag = False
    #
    # Status Verbose
    if(verbose):
        if(collisionFlag == True ):
            print( "{} Collisions Detected".format( numberOfCollisions ) )
        else:
            print( "No Collisions Detected" )
    #
    # Return;
    return collisionFlag, numberOfCollisions


  def loadInstructions(self):
    # Load instructions images
    try:
        self.instructionsImageVolume = slicer.util.getNode('Slide1')
    except:
      try:
        self.instructionsImageVolume = slicer.util.loadVolume(self.instructionsPath + 'Slides/Slide1.PNG')
        self.red_logic.SetSliceOffset(0)
        self.red_logic.FitSliceToAll()
      except:
        logging.error('ERROR: Instructions files could not be loaded...')


  def changeInfoSlide(self, directionID):
    # Change slice offset
    if directionID == 'PREVIOUS':
      self.red_logic.SetSliceOffset(0)
      self.startPart1()
    elif directionID == 'NEXT':
      self.red_logic.SetSliceOffset(1)
      self.startPart2()



  def startPart1(self):
    # show cylinder
    self.cylinderModel.GetModelDisplayNode().SetOpacity(0.3)
    self.femurModel.GetModelDisplayNode().SetOpacity(0)
    self.femurModelCopy.GetModelDisplayNode().SetOpacity(0)
    # add observer to detect collision of head with cylinder
    self.addObserverToHMDTransformNode()

  def startPart2(self):
    # show femur
    self.femurModel.GetModelDisplayNode().SetOpacity(1)
    self.femurModelCopy.GetModelDisplayNode().SetOpacity(0.6)
    self.cylinderModel.GetModelDisplayNode().SetOpacity(0)
    # add observer to detect collision of head with cylinder
    self.addObserverToHMDTransformNode()


  #------------------------------------------------------------------------------
  def addObserverToHMDTransformNode(self):
    """
    Add observer to master sequence node.
    """
    try:
      self.observerID = self.HMDTransform.AddObserver(slicer.vtkMRMLTransformableNode.TransformModifiedEvent, self.detectCylinderCollision)
    except:
      logging.error('Error adding observer to HMD transform node...')    

  #------------------------------------------------------------------------------
  def removeObserverToHMDTransformNode(self):
    """
    Remove observer from master sequence node.
    """
    if self.observerID:
      try:
        self.HMDTransform.RemoveObserver(self.observerID)
      except:
        logging.error('Error removing observer from HMD transform node...')   

  #------------------------------------------------------------------------------
  def detectCylinderCollision(self, unused1=None, unused2=None):
    collisionDetected, numberOfCollisions = self.findMeshCollision(self.headModel, self.cylinderModel, False)
    if (collisionDetected):
      print("Collision detected!")
      self.successTextModel.SetAndObserveTransformNodeID(self.HMDTransform.GetID())
      self.successTextModel.GetModelDisplayNode().SetOpacity(1)
      self.removeObserverToHMDTransformNode()


#
# VRTutorialTest
#

class VRTutorialTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_VRTutorial1()

  def test_VRTutorial1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")

    # Get/create input data

    import SampleData
    registerSampleData()
    inputVolume = SampleData.downloadSample('VRTutorial1')
    self.delayDisplay('Loaded test data set')

    inputScalarRange = inputVolume.GetImageData().GetScalarRange()
    self.assertEqual(inputScalarRange[0], 0)
    self.assertEqual(inputScalarRange[1], 695)

    outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
    threshold = 100

    # Test the module logic

    logic = VRTutorialLogic()

    # Test algorithm with non-inverted threshold
    logic.process(inputVolume, outputVolume, threshold, True)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], threshold)

    # Test algorithm with inverted threshold
    logic.process(inputVolume, outputVolume, threshold, False)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], inputScalarRange[1])

    self.delayDisplay('Test passed')
