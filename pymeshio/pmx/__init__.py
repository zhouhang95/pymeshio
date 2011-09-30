#!/usr/bin/env python
# coding: utf-8
"""
pmx file io library.

pmx file format:
    PMDEditor's Lib/PMX仕様/PMX仕様.txt
"""
__author__="ousttrue"
__license__="zlib"
__versioon__="1.0.0"


import io
import os
import struct
from pymeshio import common



class Ik(object):
    """ik info
    """
    __slots__=[
            'target_index',
            'loop',
            'limit_radian',
            'link',
            ]
    def __init__(self, target_index, loop, limit_radian):
        self.target_index=target_index
        self.loop=loop
        self.limit_radian=limit_radian
        self.link=[]


class IkLink(object):
    """ik link info
    """
    __slots__=[
            'bone_index',
            'limit_angle',
            'limit_min',
            'limit_max',
            ]
    def __init__(self, bone_index, limit_angle):
        self.bone_index=bone_index
        self.limit_angle=limit_angle
        self.limit_min=None
        self.limit_max=None


class Bone(object):
    """material

    Bone: see __init__
    """
    __slots__=[
            'name',
            'english_name',
            'position',
            'parent_index',
            'layer',
            'flag',

            'tail_positoin',
            'tail_index',
            'effect_index',
            'effect_factor',
            'fixed_axis',
            'local_x_vector',
            'local_z_vector',
            'external_key',
            'ik',
            ]
    def __init__(self,
            name: str,
            english_name: str,
            position: common.Vector3,
            parent_index: int,
            layer: int,
            flag: int
            ):
        self.name=name,
        self.english_name=english_name
        self.position=position
        self.parent_index=parent_index
        self.layer=layer
        self.flag=flag

    def getConnectionFlag(self) -> int:
        return self.flag & 0x0001

    def getIkFlag(self) -> int:
        return (self.flag & 0x0020) >> 5

    def getRotationFlag(self) -> int:
        return (self.flag & 0x0100) >> 8

    def getTranslationFlag(self) -> int:
        return (self.flag & 0x0200) >> 9

    def getFixedAxisFlag(self) -> int:
        return (self.flag & 0x0400) >> 10

    def getLocalCoordinateFlag(self) -> int:
        return (self.flag &  0x0800) >> 11
    
    def getExternalParentDeformFlag(self) -> int:
        return (self.flag &  0x2000) >> 13

 
class Material(object):
    """material

    Attributes: see __init__
    """
    __slots__=[
            'name',
            'english_name',
            'diffuse_color',
            'diffuse_alpha',
            'specular_color',
            'specular_factor',
            'ambient_color',
            'flag',
            'edge_color',
            'edge_size',
            'texture_index',
            'sphia_texture_index',
            'sphia_mode',
            'toon_sharing_flag',
            'toon_texture_index',
            'comment',
            'index_count',
            ]
    def __init__(self,
            name: str,
            english_name: str,
            diffuse_color: common.RGB,
            diffuse_alpha: float,
            specular_color: common.RGB,
            specular_factor: float,
            ambient_color: common.RGB,
            flag: int,
            edge_color: common.RGBA,
            edge_size: float,
            texture_index: int,
            sphia_texture_index: int,
            sphia_mode: int,
            toon_sharing_flag: int
            ):
        self.name=name
        self.english_name=english_name
        self.diffuse_color=diffuse_color
        self.diffuse_alpha=diffuse_alpha
        self.specular_color=specular_color
        self.specular_factor=specular_factor
        self.ambient_color=ambient_color
        self.flag=flag
        self.edge_color=edge_color
        self.edge_size=edge_size
        self.texture_index=texture_index
        self.sphia_texture_index=sphia_texture_index
        self.sphia_mode=sphia_mode
        self.toon_sharing_flag=toon_sharing_flag
        #
        self.toon_texture_index=None
        self.comment=''
        self.index_count=0


class Deform(object):
    pass


class Bdef1(object):
    """bone deform. use a weight

    Attributes: see __init__
    """
    __slots__=[ 'bone_index']
    def __init__(self, bone_index: int):
        self.bone_index=bone_index


class Bdef2(object):
    """bone deform. use two weights

    Attributes: see __init__
    """
    __slots__=[ 'index0', 'index1', 'weight0']
    def __init__(self, 
            index0: int,
            index1: int,
            weight0: float):
        self.index0=index0
        self.index1=index1
        self.weight0=weight0


class Vertex(object):
    """pmx vertex

    Attributes: see __init__
    """
    __slots__=[ 'position', 'normal', 'uv', 'deform', 'edge_factor' ]
    def __init__(self, 
            position: common.Vector3, 
            normal: common.Vector3, 
            uv: common.Vector2, 
            deform: Deform, 
            edge_factor: float):
        self.position=position 
        self.normal=normal
        self.uv=uv
        self.deform=deform
        self.edge_factor=edge_factor


class Morph(object):
    """pmx morph

    Attributes:
        name: 
        english_name: 
        panel:
        morph_type:
        offsets:
    """
    __slots__=[
            'name',
            'english_name',
            'panel',
            'morph_type',
            'offsets',
            ]
    def __init__(self, name, english_name, panel, morph_type):
        self.name=name
        self.english_name=english_name
        self.panel=panel
        self.morph_type=morph_type
        self.offsets=[]


class VerexMorphOffset(object):
    """pmx vertex morph offset

    Attributes:
        vertex_index:
        position_offset: Vector3
    """
    __slots__=[
            'vertex_index',
            'position_offset',
            ]
    def __init__(self, vertex_index, position_offset):
        self.vertex_index=vertex_index
        self.position_offset=position_offset


class DisplaySlot(object):
    """pmx display slot

    Attributes:
        name: 
        english_name: 
        special_flag:
        refrences: list of (ref_type, ref_index)
    """
    __slots__=[
            'name',
            'english_name',
            'special_flag',
            'refrences',
            ]
    def __init__(self, name, english_name, special_flag):
        self.name=name
        self.english_name=english_name
        self.special_flag=special_flag
        self.refrences=[]


class Shape(object):
    pass


class SphereShape(Shape):
    __slots__=['radius']
    def __init__(self, radius):
        self.radius=radius


class CapsuleShape(Shape):
    __slots__=['short_radius', 'long_radius']
    def __init__(self, short_radius, long_radius): 
        self.short_radius=short_radius
        self.long_radius=long_radius


class BoxShape(Shape):
    __slots__=['x', 'y', 'z']
    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z


class RigidBodyParam(object):
    """pmx rigidbody param(for bullet)

    Attributes:
        mass:
        linear_damping:
        angular_damping:
        restitution:
        friction:
    """
    __slots__=[
            'mass',
            'linear_damping',
            'angular_damping',
            'restitution',
            'friction',
            ]
    def __init__(self, mass, 
            linear_damping, angular_damping, restitution, friction):
        self.mass=mass
        self.linear_damping=linear_damping
        self.angular_damping=angular_damping
        self.restitution=restitution
        self.friction=friction

class RigidBody(object):
    """pmx rigidbody

    Attributes:
        name: 
        english_name: 
        bone_index:
        collision_group:
        no_collision_flag:
        shape:
        param:
        mode:
    """
    __slots__=[
            'name',
            'english_name',
            'bone_index',
            'collision_group',
            'no_collision_flag',
            'shape',
            'param',
            'mode',
            ]
    def __init__(self,
            name,
            english_name,
            bone_index,
            collision_group,
            no_collision_flag,
            shape_type,
            shape_size,
            shape_position,
            shape_rotation,
            mass,
            linear_damping,
            angular_damping,
            restitution,
            friction,
            mode
            ):
        self.name=name
        self.english_name=english_name
        self.bone_index=bone_index
        self.collision_group=collision_group
        self.no_collision_flag=no_collision_flag
        if shape_type==0:
            self.shape=SphereShape(shape_size.x)
        elif shape_type==1:
            self.shape=BoxShape(shape_size.x, shape_size.y, shape_size.z)
        elif shape_type==2:
            self.shape=CapsuleShape(shape_size.x, shape_size.y)
        else:
            raise pymeshio.common.ParseException(
                    "unknown shape_type: {0}".format(shape_type))
        self.param=RigidBodyParam(mass,
                linear_damping, angular_damping,
                restitution, friction)
        self.mode=mode


class Model(object):
    """pmx data representation

    Attributes:
        version: pmx version(expected 2.0)
        name: 
        english_name: 
        comment: 
        english_comment: 
        vertices:
        textures:
        materials:
        bones:
        morph:
        display_slots:
        rigidbodies:
    """
    __slots__=[
            'version', # pmx version
            'name', # model name
            'english_name', # model name in english
            'comment', # model comment
            'english_comment', # model comment in english
            'vertices',
            'indices',
            'textures',
            'materials',
            'bones',
            'morphs',
            'display_slots',
            'rigidbodies',
            ]
    def __init__(self, version):
        self.version=version
        self.name=''
        self.english_name=''
        self.comment=''
        self.english_comment=''
        self.vertices=[]
        self.indices=[]
        self.textures=[]
        self.materials=[]
        self.bones=[]
        self.rigidbodies=[]

