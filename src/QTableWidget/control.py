class Control(object):
	# 初始化信息表的分页栏
	def init_info_form_page_bar(self):
		# 当前页初始化
		self.info_form_cur_page_num = 1
		# 总页码初始初始化
		self.info_form_page_total = 7
		# 页码显示初始化
		self.info_form_page_num.setText('[%d/%d]页' %(self.info_form_cur_page_num, self.info_form_page_total))
		
		if self.info_form_cur_page_num == 1:
			if self.info_form_cur_page_num == 1 and self.info_form_page_total == 1:
				self.info_form_first_page.setDisabled(True)
				self.info_form_previous_page.setDisabled(True)
				self.info_form_next_page.setDisabled(True)
				self.info_form_last_page.setDisabled(True)
			else:
				self.info_form_first_page.setDisabled(True)
				self.info_form_previous_page.setDisabled(True)
				self.info_form_next_page.setDisabled(False)
				self.info_form_last_page.setDisabled(False)	
		elif self.info_form_cur_page_num == self.info_form_page_total:
			self.info_form_first_page.setDisabled(False)
			self.info_form_previous_page.setDisabled(False)
			self.info_form_next_page.setDisabled(True)
			self.info_form_last_page.setDisabled(True)
			
	# 信号连接
	def signal_connection(self):
		# 信息表分页栏信号连接
		self.info_form_first_page.clicked.connect(self.ctrl_info_form_page_bar)
		self.info_form_previous_page.clicked.connect(self.ctrl_info_form_page_bar)
		self.info_form_next_page.clicked.connect(self.ctrl_info_form_page_bar)
		self.info_form_last_page.clicked.connect(self.ctrl_info_form_page_bar)
	
	
	# 槽函数（信息表分页栏）
	def ctrl_info_form_page_bar(self):
		# 通过监测发送信号的对象名做相应处理
		obj_name = self.sender().objectName()
		if obj_name == 'info_form_first_page':
			self.info_form_cur_page_num = 1
			
			self.info_form_first_page.setDisabled(True)
			self.info_form_previous_page.setDisabled(True)
			self.info_form_next_page.setDisabled(False)
			self.info_form_last_page.setDisabled(False)
			
			self.info_form_page_num.setText('[1/%d]页' %self.info_form_page_total)
			
		elif obj_name == 'info_form_previous_page':
			if self.info_form_cur_page_num > 1:
				self.info_form_cur_page_num -= 1
				
				if self.info_form_cur_page_num == 1:
					self.info_form_first_page.setDisabled(True)
					self.info_form_previous_page.setDisabled(True)
					
				self.info_form_page_num.setText('[%d/%d]页' %(self.info_form_cur_page_num, self.info_form_page_total))
			else:
				self.info_form_first_page.setDisabled(True)
				self.info_form_previous_page.setDisabled(True)
			
			if self.info_form_cur_page_num == self.info_form_page_total:
				self.info_form_next_page.setDisabled(True)
				self.info_form_last_page.setDisabled(True)
			else:
				self.info_form_next_page.setDisabled(False)
				self.info_form_last_page.setDisabled(False)
			
			
		elif obj_name == 'info_form_next_page':
			if self.info_form_cur_page_num < self.info_form_page_total:
				self.info_form_cur_page_num += 1
				
				if self.info_form_cur_page_num == self.info_form_page_total:
					self.info_form_next_page.setDisabled(True)
					self.info_form_last_page.setDisabled(True)
					
				self.info_form_page_num.setText('[%d/%d]页' %(self.info_form_cur_page_num, self.info_form_page_total))
			else:
				self.info_form_next_page.setDisabled(True)
				self.info_form_last_page.setDisabled(True)
			
			if self.info_form_cur_page_num == 1:
				self.info_form_first_page.setDisabled(True)
				self.info_form_previous_page.setDisabled(True)
			else:
				self.info_form_first_page.setDisabled(False)
				self.info_form_previous_page.setDisabled(False)
			
		elif obj_name == 'info_form_last_page':
			self.info_form_cur_page_num = self.info_form_page_total
			
			self.info_form_first_page.setDisabled(False)
			self.info_form_previous_page.setDisabled(False)
			self.info_form_next_page.setDisabled(True)
			self.info_form_last_page.setDisabled(True)
			
			self.info_form_page_num.setText('[%d/%d]页' %(self.info_form_page_total, self.info_form_page_total))
