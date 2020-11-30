import pygame
import os
import base64
from ast import literal_eval

class Initialize:
	class Save:
		def __init__(self,filename):
			with open(filename,'r') as f:
				self.content=self.decode(f.readlines())
				flag_Info_isloading,flag_Entities_isloading,flag_Map_isloading=False,False,False
				self.tags={'<Info>':flag_Info_isloading,
							'<Entities>':flag_Entities_isloading,
							'<Map>':flag_Map_isloading
						   }

		def decode(self,textList):
			plaintext_list,temp=[],[]
			if textList[0]=='##TEST##\n':
				plaintext_list=textList[1:]

			else:
				for line in textList:
					temp.append(base64.b64decode(line).decode("utf-8"))
				for l in temp:
					l=l[:-1]
					if l:
						plaintext_list.append(l)
				del temp
			return plaintext_list

		def next(self):
			for line in self.content:
				yield line

		def load(self):
			line=self.next()
			cur=next(line)
			pre=''
			for tag,flag in self.tags.items():
				while cur==tag or flag==True:
					exec(f'Initialize.{tag}.handler(line)')
					pre=cur
					cur=next(line)
					flag=True
					if cur==tag:
						flag=False	
						pre=cur
						cur=next(line)
	
		def save():
			pass


	class Info():
		def __init__(self,line):
			pass

	class Entities():
		def __init__(self,line):
			d=literal_eval(line) #每一行都是一个字典
			self.id=0
			self.name=d['name']
			self.pic=d['pic']
			self.action=d['action']
			for attr in dir(self):
				print(attr)
			try:
				self.id=d['id']
				self.name=d['name']
				self.pic=d['pic']
				self.action=d['action']
			except KeyError:
				pass

		def handler(self,line):
			pass

	class Map:
		pass

if __name__=="__main__":
	print(os.path.abspath(__file__))
	sourcedir = os.path.dirname(os.path.abspath(__file__))
	rootdir = os.path.dirname(sourcedir)
	savedir = rootdir+'\\Save'
	filename='\\test.txt'
	i=Initialize.Save(savedir+filename)
	i.load()
	print(i.content)
