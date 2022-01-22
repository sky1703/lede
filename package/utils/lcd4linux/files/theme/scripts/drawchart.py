#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image
from ImageDraw import Draw


def main():
	#停用
	"""
	try:
		fh=open('/mnt/lcd4linux/data/aqilast','r')
		try:
			AqiTime=fh.readline()
			AqiTime=int(AqiTime)
		except:
			AqiTime=0
		finally:
			fh.close()
	except:
		AqiTime=0
	AqiTime=AqiTime+1
	if (AqiTime>9):
		AqiTime=0
	fh=open('/mnt/lcd4linux/data/aqilast','w')
	fh.write('%d\n'%AqiTime)
	fh.close()
	"""
	fh=open('/mnt/lcd4linux/data/aqi')
	#前三行不予处�?
	AqiMain=fh.readline()
	AqiValue=fh.readline()
	aLevel=fh.readline()
	AQIc={}
	AQI={}
	for i in range(0,24):
		AQI[i]=fh.readline()
	for i in range(0,24):
		AQIc[i]=fh.readline()
		AQIc[i]=AQIc[i].split(',')
	fh.close()
	#获取极�?
	aMax,aMin = 0,500
	for i in range(0,24):
		v=int(AQI[i])
		aMax=max(aMax,v)
		aMin=min(aMin,v)
	aMax=min(aMax,500)
	aCross=aMax-aMin
	#开始绘�?
	img=Image.new('RGBA',(74,16),(0,0,0,0))
	r,g,b=int(AQIc[23][0]),int(AQIc[23][1]),int(AQIc[23][2])
	Draw(img).rectangle((0,0,73,15), fill=(255,255,255,0),outline=(r,g,b,255))
	for i in range(0,24):
		#先绘制一个透明的全区域图片
		r,g,b,v=int(AQIc[i][0]),int(AQIc[i][1]),int(AQIc[i][2]),int(AQI[i])
		Draw(img).rectangle((i*3+1,1,i*3+3,14), fill=(r,g,b,120))
		#绘制实际实心区域
		y=0
		if (v<aMax):
			y=(aCross-v+aMin)*10/aCross
		y=y+2
		#print "%d,r:%d,g:%d,b:%d,v:%d"%(int(y),r,g,b,v)
		Draw(img).rectangle((i*3+1,y,i*3+3,14), fill=(r,g,b,255))
		#画一个标记点
		Draw(img).point((i*3+1,y),fill=(255,255,255,210))
		Draw(img).point((i*3+3,y),fill=(255,255,255,210))
		Draw(img).point((i*3+2,y),fill=(255,255,255,255))
	#绘制完成
	img.save('/mnt/lcd4linux/data/aqi.png','PNG')

if __name__ == '__main__':
  main()
