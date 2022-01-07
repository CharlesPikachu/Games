'''
Function:
    定义工具函数
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import math


'''定义速度向量'''
class VelocityVector():
    def __init__(self, magnitude=0, angle=math.radians(0)):
        self.angle = angle
        self.magnitude = magnitude


'''向量相加'''
def VectorAddition(vector1, vector2):
    x = math.sin(vector1.angle) * vector1.magnitude + math.sin(vector2.angle) * vector2.magnitude
    y = math.cos(vector1.angle) * vector1.magnitude + math.cos(vector2.angle) * vector2.magnitude
    angle = 0.5 * math.pi - math.atan2(y, x)
    magnitude = math.hypot(x, y)
    return VelocityVector(magnitude, angle)