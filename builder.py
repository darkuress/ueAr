import unreal
import importlib
from . import helper
importlib.reload(helper)
from . import baseBuilder
importlib.reload(baseBuilder)
from . import legBuilder
importlib.reload(legBuilder)
from . import spineBuilder
importlib.reload(spineBuilder)
from . import armBuilder
importlib.reload(armBuilder)
import re

class RigBuilder(helper.UEHelper):
    def __init__(self, char):
        self.char = char
        self.armBuilder  = armBuilder.ArmBuilder("drac")
        self.legBuilder   = legBuilder.LegBuilder("drac")
        self.spineBuilder = spineBuilder.SpineBuilder("drac")
        self.baseBuilder  = baseBuilder.BaseBuilder("drac")

    def clearNodeGraph(self):
        """
        """
        nodes = self.rigVmGraph().get_nodes()
        for node in nodes:
            self.rigController().remove_node(node)

        #Clear out existing controllers
        for key in self.rigElementKeys():
            if key.name == "MotionSystem":
                self.hierarchyModifier().remove_element(key)
            if key.type != 1: #BONE
                try:
                    self.hierarchyModifier().remove_element(key)
                except:
                    pass           

    def createBeginNodes(self):
        """
        """
        node_pos_x = -700
        node_pos_y = -200
        begin_excution_node = self.addNode(self.sp() +'BeginExecution','Execute',node_name='RigUnit_BeginExecution')
        self.rigController().set_node_position(begin_excution_node, [node_pos_x - 300, node_pos_y])
        inverse_execution_node = self.addNode(self.sp() +'InverseExecution','Execute',node_name='RigUnit_InverseExecution')
        self.rigController().set_node_position(inverse_execution_node, [node_pos_y - 1200, node_pos_y])
        sequence_node = self.addNode(self.sp() +'SequenceExecution','Execute',node_name='RigUnit_SequenceExecution')
        self.rigController().set_node_position(sequence_node, [node_pos_x, -200])
        self.rigController().add_link('RigUnit_BeginExecution.ExecuteContext' , 'RigUnit_SequenceExecution.ExecuteContext')

    def run(self):                 
        self.clearNodeGraph()
        self.createBeginNodes()
        self.baseBuilder.run()
        self.legBuilder.run()
        self.spineBuilder.run()
        self.armBuilder.run()
