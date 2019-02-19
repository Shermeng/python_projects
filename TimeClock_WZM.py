import time
import tkinter

class TimeGUI(tkinter.Frame):
	def __init__(self, strTime = r'00:00:00'):
		self.stringTime = strTime
		self.deltaTime = 0
		self.intervalTime = 0
		self.initGUI(False)

		pass

	#画出初始主界面的函数
	def initGUI(self, buttonState = False):
		
		self.buttonState = False

		self.mygui = tkinter.Tk(className = '时钟')
		self.mygui.geometry('480x240+400+200')
				
		#声明self.strTime为变量
		self.strTime = tkinter.StringVar()
		self.strTime.set(self.stringTime)

		self.label = tkinter.Label(self.mygui, textvariable = self.strTime, width = 30, height = 3, bg = 'gray', font = ('Arial', 30))
		self.label.pack()

		self.btn1 = tkinter.Button()
		self.btn1.configure(text = '【开始】', width = 30, height = 5, font = ('msyh', 10), command = self.callback)
		self.btn1.pack(side = tkinter.LEFT)
			
		self.btn2 = tkinter.Button()
		self.btn2.configure(text = '【重置】', width = 30, height = 5, font = ('msyh', 10), command = self.restart)
		self.btn2.pack(side = tkinter.RIGHT)
		
		global TC
		TC = TimeClock()
		tkinter.mainloop()

		pass

	#点击事件，切换开始/暂停
	def callback(self):
		if(self.buttonState == False):
			#点击了【开始】按钮
			#1.调用时间开始函数；2.将开始换成暂停
			TC.start_time()
			self.btn1['text'] = '【暂停】' 
			self.buttonState = True
			#调用循环显示函数
			self.dynamic()
							
		else:
			#点击了【暂停】按钮
			#1.调用时间结束函数；2.将暂停换成继续
			TC.end_time()
			#暂停实时显示
			self.label.after_cancel(self.updating)
			self.btn1['text'] = '【继续】' 
			self.buttonState = False
		pass

	#点击了【重置】按钮
	def restart(self):
		self.strTime.set(r'00:00:00')
		self.label.after_cancel(self.updating)
		TC.intervalTime = 0.0
		self.btn1['text'] = '【开始】' 
		self.buttonState = False
		pass

	#用于实时显示计时	
	def dynamic(self):
		TC.time_running()
		self.deltaTime = TC.deltaTime
		#输出实时格式化后的时间
		self.deltaTimeStd = TC.set_time(self.deltaTime)
		#每16ms更新一次，约60帧
		self.updating = self.label.after(16, self.dynamic)
		#设置实时显示值
		self.strTime.set(str(self.deltaTimeStd))
		pass

class TimeClock:
	def __init__(self):
		self.startTimeClock = time.time()
		self.endTimeClock = time.time()
		self.intervalTime = 0.0
		self.deltaTime = 0
		pass

	def start_time(self):
		self.startTimeClock = time.time()
		pass
	
	def end_time(self):
		self.endTimeClock = time.time()
		self.intervalTime += self.endTimeClock - self.startTimeClock 
		pass

	#时间运行函数，返回实时显示时间差
	def time_running(self):
		self.deltaTime = time.time() - self.startTimeClock + self.intervalTime
		pass

	#格式化输出
	def set_time(self, deltaTime):
		minutes = int(deltaTime//60)
		seconds = int(deltaTime - minutes*60.0)
		hseconds = int((deltaTime - minutes*60.0 - seconds)*100)
		#溢出错误，即99分钟
		if minutes > 99:
			self.deltaTime = 0
			self.intervalTime = 0
		return '%02d:%02d:%02d' % (minutes,seconds,hseconds)

if __name__ == '__main__':
	win = TimeGUI()

