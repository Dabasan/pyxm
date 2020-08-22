"""
Client for Python XOPSManipulator
"""
from py4j.java_gateway import JavaGateway
from py4j.java_collections import JavaArray,JavaList,JavaMap
from typing import Dict

class PyXMClient(object):
    """
    Client for Python XOPSManipulator
    """
    def __init__(self):
        super().__init__()

        self.gateway=JavaGateway()
        self.entry_point=self.gateway.entry_point

    def shutdown(self):
        self.entry_point.shutdown()
        self.gateway.shutdown()

    def get_gateway(self):
        return self.gateway
    def get_entry_point(self):
        return self.entry_point

class BD1Manipulator(object):
    """
    BD1Manipulator
    """
    def __init__(self,client:PyXMClient,java_port:int=10001,python_port:int=10002,filepath:str=None):
        super().__init__()

        self.gateway=client.get_gateway()
        self.entry_point=client.get_entry_point()

        entry_point.startBD1ManipulatorServer(java_port,python_port)
        if filepath is None:
            entry_point.instantiate_BD1Manipulator()
        else:
            entry_point.instantiate_BD1Manipulator(filepath)

    def get_num_blocks(self):
        return self.entry_point.getNumBlocks_BD1Manipulator()
    
    def get_texture_filename(self,texture_id:int)->str:
        return self.entry_point.getTextureFilename_BD1Manipulator(texture_id)
    def get_texture_filenames(self)->Dict[int,str]:
        java_map=self.entry_point.getTextureFilenames_BD1Manipulator()

        texture_filenames={}
        for key in java_map:
            texture_filenames[key]=java_map[key]

        return texture_filenames

    def set_texture_filename(self,texture_id:int,texture_filename:str):
        self.entry_point.setTextureFilename_BD1Manipulator(
            texture_id,texture_filename
        )
    def set_texture_filenames(self,texture_filenames:Dict[int,str]):
        java_map=self.gateway.jvm.java.util.HashMap()
        for k,v in texture_filenames.items():
            java_map[k]=v

        self.entry_point.setTextureFilenames_BD1Manipulator(java_map)

    def translate(self,translation_x:float,translation_y:float,translation_z:float):
        self.entry_point.translate_BD1Manipulator(translation_x,translation_y,translation_z)

    def rot_x(self,th:float):
        self.entry_point.rotX_BD1Manipulator(th)
    def rot_y(self,th:float):
        self.entry_point.rotY_BD1Manipulator(th)
    def rot_z(self,th:float):
        self.entry_point.rotZ_BD1Manipulator(th)
    def rot(self,axis_x:float,axis_y:float,axis_z:float,th:float):
        self.entry_point.rot_BD1Manipulator(axis_x,axis_y,axis_z,th)
    
    def rescale(self,scale_x:float,scale_y:float,scale_z:float):
        self.entry_point.rescale_BD1Manipulator(scale_x,scale_y,scale_z)
    
    def invert_z(self):
        self.entry_point.invertZ_BD1Manipulator()

    def save_as_bd1(self,filepath:str)->int:
        return self.entry_point.saveAsBD1_BD1Manipulator(filepath)
    def save_as_obj(self,filepath_obj,filepath_mtl,mtl_filename,flip_v)->int:
        return self.entry_point.saveAsOBJ_BD1Manipulator(
            filepath_obj,filepath_mtl,mtl_filename,flip_v
        )
