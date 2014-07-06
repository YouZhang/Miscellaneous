#!/usr/bin/python
#-*- coding: utf-8 -*-

class Table(object):
	#空闲分区表
	#0:开始地址 1:长度
	freeTable = []
	
	#占用分区表
	#0:程序名 1:开始地址 2:长度
	useTable = []
	
	def __init__(self):
		print '初始化内存使用情况'
		self.useTable.append(['os',0,10])
		self.freeTable.append([10,100])
	
	def WorkAdd(self):
		memoryName = raw_input('请输入进程名:')
		memoryName = memoryName.strip()
		memorySize = int(raw_input('请输入进程大小:'))
		if (memoryName != '' and memorySize > 0):
			self._WorkAdd(memoryName, memorySize)
		else:
			print '输入有问题'
			
		
	def _WorkAdd(self, memoryName, memorySize):
		minIndex = -1
		minMemory = 0
		for i in xrange(len(self.freeTable)):
			if (self.freeTable[i][1] > memorySize):
				if (minIndex == -1):
					minMemory = self.freeTable[i][1]
					minIndex = i
				else:
					if (self.freeTable[i][1] < minMemory):
						minMemory = self.freeTable[i][1]
						minIndex = i
		if (minIndex == -1):
			self.outOfMemory()
		else:
			start = self.freeTable[minIndex][0]
			length = self.freeTable[minIndex][1]
			self.freeTable.remove(self.freeTable[minIndex])
			self.useTable.append([memoryName,start,memorySize])
			self.freeTable.append([start + memorySize,length - memorySize])
			self.display()
	
	def display(self):
		print '已用分区表\n程序进程名\t开始地址\t长度'
		for i in xrange(len(self.useTable)):
			print self.useTable[i][0], '\t\t', self.useTable[i][1], '\t', self.useTable[i][2]
		print '空闲分区表\n开始地址\t长度'
		for i in xrange(len(self.freeTable)):
			print self.freeTable[i][0], '\t\t', self.freeTable[i][1]
	
	def outOfMemory(self):
		print '亲，内存不够了'
		self.display()
		
	def WorkDel(self):
		memoryName = raw_input('请输入进程名:')
		memoryName = memoryName.strip()
		if (memoryName == ''):
			print '没有输入'
		else:
			self._WorkDel(memoryName)
			
	def _WorkDel(self,memoryName):
		index = -1;
		for i in xrange(len(self.useTable)):
			if (self.useTable[i][0] == memoryName):
				index = i
				break
		if (index == -1):
			print '不存在此进程'
		else:
			start = self.useTable[index][1]
			length = self.useTable[index][2]
			end = start + length
			freeIndex1 = -1
			freeIndex2 = -1
			for i in xrange(len(self.freeTable)):
				iStart = self.freeTable[i][0]
				iLength = self.freeTable[i][1]
				if (start == iStart + iLength):
					freeIndex1 = i
					break
			for i in xrange(len(self.freeTable)):
				if (self.freeTable[i][0] == end):
					freeIndex2 = i
					break
			if (freeIndex1 != -1 and freeIndex2 != -1):
				iStart = self.freeTable[freeIndex1][0]
				iLength = self.freeTable[freeIndex1][1] + self.freeTable[freeIndex2][1] + length
				self.freeTable.append([iStart,iLength])
				self.freeTable.remove(self.freeTable[freeIndex1])
				self.freeTable.remove(self.freeTable[freeIndex2])
			elif (freeIndex1 != -1 and freeIndex2 == -1):
				iStart = self.freeTable[freeIndex1][0]
				iLength = self.freeTable[freeIndex1][1] + length
				self.freeTable.append([iStart,iLength])
				self.freeTable.remove(self.freeTable[freeIndex1])
			elif (freeIndex1 == -1 and freeIndex2 != -1):
				iStart = start
				iLength = self.freeTable[freeIndex2][1] + length
				self.freeTable.append([iStart,iLength])
				self.freeTable.remove(self.freeTable[freeIndex2])
			elif (freeIndex1 == -1 and freeIndex2 == -1):
				iStart = start
				iLength = length
				self.freeTable.append([iStart,iLength])
			else:
				print '系统崩溃'
			self.display()
			
	def run(self):
		while(True):
			print '动态分区存储管理'
			print '1,增加程序'
			print '2,结束程序'
			print '3,退出'
			print '请选择操作:(输入数字)'
			chose = raw_input('请选择操作:')
			chose = chose.strip()
			if (chose == '1'):
				self.WorkAdd()
			elif(chose == '2'):
				self.WorkDel()
			elif (chose == '3'):
				break
			else:
				print '输入有误'
			print '\n'
				
			
			
if __name__ == '__main__':
	table = Table()
	table.run()
	
					
					
				
			
				
			
			
						
						
					
					
			
		
		
