"""
BD1
"""
from py4j.java_collections import JavaArray,JavaList,JavaMap
from npy3d.vector import Vector
from npy3d.matrix import Matrix
from typing import Dict,List,Tuple
import pathlib

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from client import PyXMClient

class UV(object):
    """
    UV
    """
    def __init__(self,init_values:Tuple[float,float]=None):
        super().__init__()

        if init_values is None:
            self.u=0.0
            self.v=0.0
        else:
            self.u=init_values[0]
            self.v=init_values[1]

    def get(self):
        return self.u,self.v
    def get_u(self):
        return self.u
    def get_v(self):
        return self.v

    def set(self,u,v):
        self.u=u
        self.v=v
    def set_u(self,u):
        self.u=u
    def set_v(self,v):
        self.v=v

class BD1Block(object):
    """
    BD1Block
    """
    def __init__(self):
        super().__init__()

        self.vertex_positions=[]
        self.uvs=[]
        self.texture_ids=[]
        self.enabled=True

        for i in range(8):
            self.vertex_positions.append(Vector())
        for i in range(24):
            self.uvs.append(UV())
        for i in range(6):
            self.texture_ids.append(0)

    def get_vertex_positions(self)->List[Vector]:
        return self.vertex_positions
    def get_uvs(self)->List[UV]:
        return self.uvs
    def get_texture_ids(self)->List[int]:
        return self.texture_ids
    def is_enabled(self)->bool:
        return self.enabled

    def set_vertex_positions(self,vertex_positions:List[Vector]):
        if len(vertex_positions)!=8:
            message="Expected 8 elements but got {}.".format(len(vertex_positions))
            raise ValueError(message)

        self.vertex_positions=vertex_positions
    def set_uvs(self,uvs:List[UV]):
        if len(uvs)!=24:
            message="Expected 24 elements but got {}.".format(len(uvs))
            raise ValueError(message)

        self.uvs=uvs
    def set_texture_ids(self,texture_ids:List[int]):
        if len(texture_ids)!=6:
            message="Expected 6 elements but got {}.".format(len(uvs))
            raise ValueError(message)

        self.texture_ids=texture_ids
    def set_enabled(self,enabled:bool):
        self.enabled=enabled

class BD1Manipulator(object):
    """
    BD1Manipulator
    """
    def __init__(self,client:PyXMClient,java_port:int=10001,python_port:int=10002,filepath:str=None):
        super().__init__()

        self.gateway=client.get_gateway()
        self.entry_point=client.get_entry_point()

        self.entry_point.startBD1ManipulatorServer(java_port,python_port)
        if filepath is None:
            self.entry_point.instantiate_BD1Manipulator()
        else:
            abs_filepath=pathlib.Path(filepath).resolve().__str__()
            self.entry_point.instantiate_BD1Manipulator(abs_filepath)

    def get_blocks(self)->List[BD1Block]:
        self.entry_point.loadBlocksToLists_BD1Manipulator()
        vertex_positions_list=self.entry_point.getVertexPositionsList_BD1Manipulator()
        uvs_list=self.entry_point.getUVsList_BD1Manipulator()
        texture_ids_list=self.entry_point.getTextureIDsList_BD1Manipulator()
        enabled_flags_list=self.entry_point.getEnabledFlagsList_BD1Manipulator()

        num_blocks=len(enabled_flags_list)

        blocks=[]
        for i in range(num_blocks):
            vertex_positions=[]
            uvs=[]
            texture_ids=[]
            enabled=True

            #Vertex positions
            for j in range(8):
                index=i*24+j*3

                pos=Vector()
                pos.set_x(vertex_positions_list[index])
                pos.set_y(vertex_positions_list[index+1])
                pos.set_z(vertex_positions_list[index+2])

                vertex_positions.append(pos)
            #UVs
            for j in range(24):
                index=i*48+j*2

                uv=UV()
                uv.set_u(uvs_list[index])
                uv.set_v(uvs_list[index+1])

                uvs.append(uv)
            #Texture IDs
            for j in range(6):
                index=i*6+j
                texture_ids.append(texture_ids_list[index])
            #Enabled flag
            enabled=enabled_flags_list[i]

            block=BD1Block()
            block.set_vertex_positions(vertex_positions)
            block.set_uvs(uvs)
            block.set_texture_ids(texture_ids)
            block.set_enabled(enabled)

            blocks.append(block)

        return blocks
    def set_blocks(self,blocks:List[BD1Block]):
        vertex_positions_list=self.gateway.jvm.java.util.ArrayList()
        uvs_list=self.gateway.jvm.java.util.ArrayList()
        texture_ids_list=self.gateway.jvm.java.util.ArrayList()
        enabled_flags_list=self.gateway.jvm.java.util.ArrayList()

        for block in blocks:
            vertex_positions=block.get_vertex_positions()
            uvs=block.get_uvs()
            texture_ids=block.get_texture_ids()
            enabled=block.is_enabled()

            for pos in vertex_positions:
                vertex_positions_list.append(pos.get_x())
                vertex_positions_list.append(pos.get_y())
                vertex_positions_list.append(pos.get_z())
            for uv in uvs:
                uvs_list.append(uv.get_u())
                uvs_list.append(uv.get_v())
            for texture_id in texture_ids:
                texture_ids_list.append(texture_id)
            enabled_flags_list.append(enabled)

        self.entry_point.setBlocksAsLists_BD1Manipulator(
            vertex_positions_list,uvs_list,texture_ids_list,enabled_flags_list
        )

    def get_num_blocks(self)->int:
        return self.entry_point.getNumBlocks_BD1Manipulator()
    
    def get_texture_filename(self,texture_id:int)->str:
        return self.entry_point.getTextureFilename_BD1Manipulator(texture_id)
    def get_texture_filenames(self)->Dict[int,str]:
        java_map=self.entry_point.getTextureFilenames_BD1Manipulator()

        texture_filenames={}
        for k in java_map:
            texture_filenames[k]=java_map[k]

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

    def transform(self,mat:Matrix):
        double_class=self.gateway.jvm.double
        mat_array=self.gateway.new_array(double_class,16)
        for i in range(4):
            for j in range(4):
                mat_array[i*4+j]=mat.get(i,j)

        self.entry_point.transform_BD1Manipulator(mat_array)

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
        abs_filepath=pathlib.Path(filepath).resolve().__str__()
        return self.entry_point.saveAsBD1_BD1Manipulator(abs_filepath)
    def save_as_obj(self,filepath_obj,filepath_mtl,mtl_filename,flip_v)->int:
        abs_filepath_obj=pathlib.Path(filepath_obj).resolve().__str__()
        abs_filepath_mtl=pathlib.Path(filepath_mtl).resolve().__str__()

        return self.entry_point.saveAsOBJ_BD1Manipulator(
            abs_filepath_obj,abs_filepath_mtl,mtl_filename,flip_v
        )
