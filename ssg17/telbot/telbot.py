# -*- coding:utf-8
# pip install telepot
import sys
import os
import json
import time
import datetime
import urllib2
import sqlite3
import re
import threading

#Local
from telbot_logger import *

# Third Party
import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space

# Const Variable
COINS       = ['BTC','ETH','XRP']
COIN_LIST   = COINS + [coin.lower() for coin in COINS]
EXCHANGE    = 'KRW'

# Global
last_price      = None
updator_status  = None
db_lock = threading.Lock()

# Sub func
comma = lambda number : format(number, ',')
def enum(**enums):
		return type('Enum', (), enums)

# SingleTon
class Singleton(object):
  _instance = None
  def __new__(class_, *args, **kwargs):
	if not isinstance(class_._instance, class_):
		class_._instance = object.__new__(class_, *args, **kwargs)
	return class_._instance

# Process Manager
class ProcessManager(Singleton):
	def __init__(self):
		super(ProcessManager, self).__init__()
		self.db     = DBManager()
		self.util   = Util()
		self.save_ids   = dict()
		self.try_count  = dict()
		self.filter_ids = list()
		#SSG_CTF_TELBOT(ssg_ctf_telbot)
		self.token  = 'BOT_TOKEN'
		self.up     = 1.01
		self.down   = 0.99
		self.currency = None
		self.user_cnt = 0
		self.loadID()

	def loadID(self):
		chat_ids = self.db.query("select * from threshold")
		for chat_id in chat_ids:
			self.save_ids[chat_id[0]] = ({'id':chat_id, 'up':self.up, 'down':self.down,
				'alarm':0, 'cycle':30, 'thread':None})
			self.save_ids[chat_id[0]]['id'] = chat_id[0]
			self.save_ids[chat_id[0]]['down'] = chat_id[-1]
			self.save_ids[chat_id[0]]['up'] = chat_id[-2]
			self.save_ids[chat_id[0]]['alarm'] = chat_id[-3]
			self.save_ids[chat_id[0]]['cycle'] = chat_id[-4]

# DB Managers
class DBManager(Singleton):
	def __init__(self):
		super(DBManager, self).__init__()
		self.dbcon = sqlite3.connect('vuln_telbot.db', check_same_thread=False)
		self.dbcur = self.dbcon.cursor()
		self.idx = enum(Chat_ID=0, BTC_H=1, BTC_L=2, ETH_H=3, ETH_L=4,
						XRP_H=5, XRP_L=6, CYCLE=7, ALARM=8, UP_RATIO=9, DOWN_RATIO=10)

	def query(self, statement):
		global db_lock
		db_lock.acquire()
		try:
			self.dbcur.execute(statement)
			self.dbcon.commit()
			return self.dbcur.fetchall()

		except Exception as e:
				logger.error("[Error] DBManager.db.query error occur!\n\t"+str(e))

		finally:
			db_lock.release() 

	def __del__(self):
		self.dbcon.close()

# Util
class Util(object):
	def __init__(self):
		pass

	def checkInjection(self, in_data):
		regular = re.compile('^[a-zA-Z0-9\_\-]*')

		filter_str = regular.match(in_data).group()
		if len(in_data) == len(filter_str):
			return True
		else:
			return False

class Updator(DBManager, threading.Thread):
	def __init__(self):
		global manager
		super(Updator, self).__init__()
		self.API_URL= 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=%s&tsyms=%s'\
					% (",".join(COINS), EXCHANGE)
		self.err_cnt = 0
		self.db = DBManager()

	def run(self):
		global updator_status
		updator_status = True
		print "\n<Updator>["+threading.current_thread().name+"] : "+str(threading.current_thread().ident)
		while 1:
			try:
				req = urllib2.Request(self.API_URL)
				respone = urllib2.urlopen(req).read()

				if len(respone) > 0:
					manager.currency = json.loads(respone)
					self.err_cnt = 0
					for coin in COINS:
						self.db.query("update last_price set "+coin+"="+str(manager.currency[coin][EXCHANGE]))
				else:
					self.err_cnt += 1
					print "[Error] Respone is zero at Updator.updateCurrency().\n"
				
				time.sleep(30)

			except Exception as e:
				self.err_cnt += 1
				logger.error("[Error] Updator.updateCurrency().\n\t" + str(e))

			if self.err_cnt >= 50:
				logger.error("Check API SITE!\n\tUpdator exited!")
				updator_status = False
				break

class PriceManager(telepot.helper.ChatHandler):
	def __init__(self, *args, **kwargs):
		global COIN_LIST
		global EXCHANGE
		global manager

		print "\n<Init>["+threading.current_thread().name+"] : "+str(threading.current_thread().ident)
		super(PriceManager, self).__init__(*args, **kwargs)

		self.up     = 1.01
		self.down   = 0.99

		# call by assignment
		self.save_ids	= manager.save_ids
		self.try_count	= manager.try_count
		self.filter_ids	= manager.filter_ids
		self.db			= manager.db
		
		# initalize
		self.check_thread = None
		self.check_bot = telepot.Bot(manager.token)

	def messageTo(self, msg):
		self.sender.sendMessage(msg)

	# Alarm
	def startAlarm(self, chat_id):
		if self.save_ids[chat_id]['thread'] == None:
			self.save_ids[chat_id]['alarm'] = 1
			self.db.query("update threshold set ALARM=1 where Chat_ID="+str(chat_id))
			execute_id = self.save_ids[chat_id]['id']
			thread_cycle = self.save_ids[chat_id]['cycle']
			self.save_ids[chat_id]['thread'] = threading.Thread(target=self.checkPrice, args=(execute_id, thread_cycle,))
			self.save_ids[chat_id]['thread'].setDaemon(True)
			self.save_ids[chat_id]['thread'].start()

	def stopAlarm(self, chat_id):
		print "[INFO] Alarm Thread : "+threading.current_thread().name+"] : "+str(threading.current_thread().ident)
		self.save_ids[chat_id]['alarm'] = 0
		if self.save_ids[chat_id]['thread'] != None:
			self.save_ids[chat_id]['thread'].join(timeout=10)
			self.messageTo("Alarm is terminating... wait a minute.")
			self.save_ids[chat_id]['thread'] = None
			self.db.query("update threshold set ALARM=0 where Chat_ID="+str(chat_id))

	def reloadAlarm(self, chat_id):
		if self.save_ids[chat_id]['thread']:
			self.stopAlarm(chat_id)
			self.startAlarm(chat_id)
		else:
			self.startAlarm(chat_id)

	# Alarm Main
	def checkPrice(self, chat_id, thread_cycle):
		#try:
		print "[INFO] Price Thread : "+threading.current_thread().name+" : "+str(threading.current_thread().ident)
		while self.save_ids[chat_id]['alarm']:
			self.checkThreshold(chat_id)
			time.sleep(thread_cycle)

	def checkThreshold(self, chat_id):
		btc_h_alert = self.db.query("select * from btc_high_alert where Chat_ID="+str(chat_id))
		btc_l_alert = self.db.query("select * from btc_low_alert where Chat_ID="+str(chat_id))
		eth_h_alert = self.db.query("select * from eth_high_alert where Chat_ID="+str(chat_id))
		eth_l_alert = self.db.query("select * from eth_low_alert where Chat_ID="+str(chat_id))
		xrp_h_alert = self.db.query("select * from xrp_high_alert where Chat_ID="+str(chat_id))
		xrp_l_alert = self.db.query("select * from xrp_low_alert where Chat_ID="+str(chat_id))

		if btc_h_alert:
			for row in btc_h_alert:
				self.priceAlert('BTC', 'H', self.db.idx.BTC_H, row[0])

		if btc_l_alert:
			for row in btc_l_alert:
				print row
				self.priceAlert('BTC', 'L', self.db.idx.BTC_L, row[0])

		if eth_h_alert:
			for row in eth_h_alert:
				self.priceAlert('ETH', 'H', self.db.idx.ETH_H, row[0])

		if eth_l_alert:
			for row in eth_l_alert:
				self.priceAlert('ETH', 'L', self.db.idx.ETH_L, row[0])

		if xrp_h_alert:
			for row in xrp_h_alert:
				self.priceAlert('XRP', 'H', self.db.idx.XRP_H, row[0])

		if xrp_l_alert:
			for row in xrp_l_alert:
				self.priceAlert('XRP', 'L', self.db.idx.XRP_L, row[0])

	def priceAlert(self, coin, mode, idx, chat_id):
		try:
			print "===========================================\n"+\
				  "[INFO] Price Alert\n"+\
				  "\tThread : "+threading.current_thread().name+"("+str(threading.current_thread().ident)+")\n"+\
				  "===========================================\n"
			threshold = self.db.query("select * from threshold where Chat_ID="+str(self.save_ids[chat_id]['id']))
			if mode in ['H','L']:
				msg = '''[%s PRICE ALERT] - %s (chat_id : %s)
					%s is %s.
					Current %s : %s 원
					''' % (coin, mode, str(self.save_ids[chat_id]['id']),
						coin, ('higher' if mode=='H' else 'lower'),
						coin, str(comma(manager.currency[coin][EXCHANGE])))
				self.check_bot.sendMessage(chat_id, msg)
				self.updateThreshold(coin, mode, chat_id)

		except Exception as e:
			logger.error("Error in PriceManager.priceAlert()\n\t" + str(e))

	# threshold functions
	def updateThreshold(self, coin, mode, chat_id):
		if coin in COINS:
			if mode == 'H':
				self.changeThreshold(coin, manager.currency[coin][EXCHANGE]*self.save_ids[chat_id]['up'],
					mode, chat_id)

			elif mode == 'L':
				self.changeThreshold(coin, manager.currency[coin][EXCHANGE]*self.save_ids[chat_id]['down'], 
					mode, chat_id)

	def changeThreshold(self, coin, value, mode, chat_id):
		if mode == 'H':
			origin = self.db.query("select * from threshold where Chat_ID="+str(chat_id)
				+" and "+str(value)+">"+coin.upper()+"_L")
		else:
			origin = self.db.query("select * from threshold where Chat_ID="+str(chat_id)
				+" and "+str(value)+"<"+coin.upper()+"_H")

		if origin:
			query = "update threshold set "+coin.upper()+"_"+mode.upper()+"="+str(value)+" where Chat_ID="+str(chat_id)
			self.db.query("update threshold set "+coin.upper()+"_"+mode.upper()+"="+str(value)
							+" where Chat_ID="+str(chat_id))
		else:
			self.messageTo("[Error] Please Check threshold range!")

	
	def initUser(self, chat_id):
		threshold = {'BTC':{'H':0, 'L':0}, 'ETH':{'H':0,'L':0}, 'XRP':{'H':0, 'L':0}}
		for coin in COINS:
			threshold[coin]['H'] = manager.currency[coin][EXCHANGE]*self.up
			threshold[coin]['L'] = manager.currency[coin][EXCHANGE]*self.down

		if self.db.query("select Chat_ID from threshold where Chat_ID="+str(chat_id)):
			return 

		else:
			self.db.query(
				"insert into threshold values ("+str(chat_id)+","
				+str(threshold['BTC']['H'])+","+str(threshold['BTC']['L'])+","
				+str(threshold['ETH']['H'])+","+str(threshold['ETH']['L'])+","
				+str(threshold['XRP']['H'])+","+str(threshold['XRP']['L'])+","
				+str(self.save_ids[chat_id]['cycle'])+","+str(self.save_ids[chat_id]['alarm'])+","
				+str(self.up)+","+str(self.down)+")")

	def showInfo(self, chat_id):
		global updator_status
		threshold = self.db.query("select * from threshold where Chat_ID="+str(self.save_ids[chat_id]['id']))
		if threshold:
			threshold = threshold[0]
			msg = '''
			[Your Threshold]
			BTC : <HIGH> %s 원 <LOW> %s 원
			ETH : <HIGH> %s 원 <LOW> %s 원
			XRP : <HIGH> %s 원 <LOW> %s 원
			UP_RATIO : %s 
			DOWN_RATIO : %s
			ALARM_STATUS : %s
			THREAD_CYCLE : %s 초
			Updator Status : %s
			''' % (
				comma(threshold[self.db.idx.BTC_H]),comma(threshold[self.db.idx.BTC_L]),
				comma(threshold[self.db.idx.ETH_H]),comma(threshold[self.db.idx.ETH_L]),
				comma(threshold[self.db.idx.XRP_H]),comma(threshold[self.db.idx.XRP_L]),
				str(threshold[self.db.idx.UP_RATIO]),str(threshold[self.db.idx.DOWN_RATIO]),
				('ON' if threshold[self.db.idx.ALARM] else 'Off'),
				str(threshold[self.db.idx.CYCLE]), ('ON' if updator_status else 'Off')
				)
			self.messageTo(msg)

		else:
			msg ='''
			[Error] showInfo(chat_id(%s)) don't get user_info. please retry.
			''' % (self.save_ids[chat_id]['id'])
			self.messageTo(msg)


	def deleteThreshold(self, chat_id):
		self.db.query("delete from threshold where Chat_ID="+str(self.save_ids[chat_id]['id']))
		del self.save_ids[chat_id]

	# message handle function
	def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)
		now = datetime.datetime.now()
		now_time = now.strftime('%Y-%m-%d %H:%M:%S')
		print "===========================================\n"+\
			  '[INFO] Access from ' + str(chat_id)+"\n"+\
		 	  "\tThread : "+threading.current_thread().name+"("+str(threading.current_thread().ident)+")\n"+\
		 	  "===========================================\n"
		if chat_id in manager.filter_ids:
			self.messageTo("You blocked for brute force attack.")
			logger.info("Block ID Access["+str(chat_id)+"]")
			return

		if content_type != 'text':
			self.messageTo("I only support text message.")
			return

		if chat_id not in self.save_ids.keys():
			print "===========================================\n"+\
			 "[INFO] New Chat_id : "+str(chat_id)+"\n"+\
			 "\tThread : "+threading.current_thread().name+"("+str(threading.current_thread().ident)+")"+"\n"+\
			 '\tChat_type : ' + chat_type+"\n"+\
			 '\tTime : ' + now_time+"\n"+\
			 '\tcontent_type : ' + content_type+"\n"+\
			 '\tchat_id : ' + str(chat_id)+"\n"+\
			 "===========================================\n"
			manager.user_cnt += 1
			logger.info("New Chat_id["+str(chat_id)+"/"+str(manager.user_cnt)+"]")

			self.save_ids[chat_id] = ({'id':chat_id, 'up':self.up, 'down':self.down,
				'alarm':0, 'cycle':30, 'thread':None})
			self.try_count[chat_id] = 0
			self.initUser(chat_id)

		text = msg['text']
		args = text.split(' ')

		if self.save_ids[chat_id]['alarm']:
			self.startAlarm(chat_id)

		if text.startswith('/'):
			if text.startswith('/help'):
				self.help(chat_id)

			elif text.startswith('/show'):
				self.showInfo(chat_id)

			elif text.startswith('/start'):
				if self.save_ids[chat_id]['alarm'] == 0:
					self.startAlarm(chat_id)

			elif text.startswith('/stop'):
				if self.save_ids[chat_id]['alarm'] != 0:
					self.stopAlarm(chat_id)
				else:
					self.messageTo("alarm haven't started")

			elif text.startswith('/info'):
				th = threading.Thread(target=self.info, args=(chat_id,))
				th.start()

			elif text.startswith('/get'):
				self.getCurrency(chat_id)

			elif text.startswith('/set_cycle'):
				if len(args)>1:
					try:
						if 10000>=int(args[1])>=1:
							thread_cycle = int(args[1])
							self.save_ids[chat_id]['thread_cycle'] = thread_cycle
							self.save_ids[chat_id]['alarm'] = 0
							self.db.query("update threshold set THREAD_CYCLE="+str(thread_cycle)+" where Chat_ID="+str(chat_id))

							#must check it
							self.messageTo("Reload Alarm...")
							self.reloadAlarm(chat_id)

					except Exception as e:
						error_msg = "[Error] /set_cycle\n\t"+str(e)
						self.messageTo(error_msg)

			elif text.startswith('/set_thr'):
				if len(args)>3:
					try:
						chg_coin = args[1].upper()
						chg_mode = args[2].upper()
						chg_threshold = int(args[3])
						if chg_coin in COIN_LIST:
							if chg_mode == 'HIGH':
								self.changeThreshold(chg_coin, chg_threshold, 'H', chat_id)         
							elif chg_mode == 'LOW':
								self.changeThreshold(chg_coin, chg_threshold, 'L', chat_id)
							else:
								self.messageTo('[Error] Usage : /set (BTC,ETH,XRP) (HIGH,LOW) (threshold)')
				
					except Exception as e:
						error_msg = "[Error] /set_thr\n\t"+str(e)
						self.messageTo(error_msg)
				else:
					self.messageTo("[Error] Usage : /set_thr (BTC,ETH,XRP) (HIGH, LOW) (thrshold)")

			elif text.startswith('/set_ratio'):
				if len(args)>2:
					try:
						chg_action = args[1].upper()
						chg_ratio = float(args[2])

						if 0<chg_ratio<=3:
							if chg_action == 'HIGH':
								self.changeRatio('UP_RATIO', chg_ratio, chat_id)
								self.save_ids[chat_id]['up'] = chg_ratio
							elif chg_action == 'LOW':
								self.changeRatio('DOWN_RATIO', chg_ratio, chat_id)
								self.save_ids[chat_id]['down'] = chg_ratio
							else:
								self.messageTo('[Error] Usage : /set_ratio (HIGH,LOW) (RATIO)')
						else:
							self.messageTo('[Error] Usage : /set_ratio (HIGH,LOW) (RATIO)')

					except Exception as e:
						error_msg = "[Error] /set_ratio\n\t"+str(e)
						self.messageTo(error_msg)
				else:
					self.messageTo('[Error] Usage : /set_ratio (HIGH,LOW) (RATIO)')

			elif text.startswith('/reset'):
				self.deleteThreshold(chat_id)
			
			elif text.startswith('/check_flag'):
				if len(args)>1:
					injection_state = manager.util.checkInjection(args[1])

					if injection_state == False:
						self.messageTo('Don\'t SQLInjection.\nIf you try again and again, could block account.')
						logger.warning("SQL Injection["+str(chat_id)+"]: "+str(args[1]))

					else:
						statement = "select FLAG from flag_table where Chat_ID=\'"+args[1]+'\''
						flag = self.db.query(statement)
						logger.info("CHECK FLAG ["+str(chat_id)+"] : "+str(statement))

						if flag:
							self.messageTo("FLAG is {"+str(flag[0][0])+"}")
							logger.info("GET FLAG ["+str(chat_id)+"] : Successfully")
						else:
							if chat_id not in self.try_count.keys():
								self.try_count[chat_id] = 0
								try_cnt = 0
							else:
								try_cnt = self.try_count[chat_id]

							if try_cnt>=100:
								self.messageTo("your try count : "+str(try_cnt)+"\nYour Chat_ID is blocked from now!")
								self.filter_ids.append(chat_id)
							else:
								self.try_count[chat_id]+=1
								self.messageTo("try count up!\nIt's not admin chat_id")
			
			else:
				self.messageTo("Unknow command. you get helped with \"/help\" command")
	
	# sub functions
	def changeRatio(self, mode, chg_ratio, chat_id):
		self.db.query("update threshold set "+mode+"="+str(chg_ratio)
							+" where Chat_ID="+str(chat_id))

	def getCurrency(self, chat_id):
		msg = '''
		[ALL PRICE]
		BTC : %s 원
		ETH : %s 원
		XRP : %s 원
		''' % (comma(manager.currency['BTC'][EXCHANGE]), 
				comma(manager.currency['ETH'][EXCHANGE]),
				comma(manager.currency['XRP'][EXCHANGE]))
		self.messageTo(msg)

	def help(self, chat_id):
		self.messageTo('''
			명령어 사용법:
			/help
			\t 사용법을 출력합니다.
			/info
			\t 개발자 정보를 출력합니다.
			/start
			\t 알리미를 시작합니다.
			/stop
			\t 알리미를 중단합니다.
			/set_cycle (thread_cycle)
			\t 알리미 실행 주기를 설정합니다.
			/set_ratio (HIGH,LOW) (RATIO)
			\t 자동 threshold 업데이트 비율을 설정합니다.
			\t 기본적으로 아래와 같이 설정되어있으며
			\t HIGH의 경우 1보다 커야하고, LOW의 경우 1보다 작아야 합니다.
			\t\t ex) /set_ratio HIGH 1.01
			\t\t ex) /set_ratio LOW 0.99
			/set_thr (BTC,ETH,XRP) (HIGH,LOW) (threshold value)
			\t threshold를 설정합니다.
			/get
			\t 현재 BTC, ETH, XRP 가격 정보를 알려줍니다.
			/show
			\t 사용자 설정 정보를 출력합니다.
			/reset
			\t 설정해놓은 threshold를 초기화합니다.
			/check_flag (admin_chat_id)
		 	\t 플래그를 확인합니다.
		 	\t 플래그 확인에 100번이상 실패 시 아이디가 차단됩니다.
			'''
			)

	def info(self, chat_id):
		print "===========================================\n"+\
			 "[INFO] Call Info\n"+\
		 	 "\tThread : "+threading.current_thread().name+"("+str(threading.current_thread().ident)+")\n"+\
			 "===========================================\n"
		
		try:
			self.save_ids[chat_id]['id'] = 'SSG_ADMIN_CHAT_ID'
			dev_info = self.db.query("select * from flag_table where Chat_ID=\'"
				+str(self.save_ids[chat_id]['id'])+"\'")
			if dev_info:
				msg = '''
				[Developer Info]
				NickName    : %s
				PhoneNumber : %s
				Compnay     : S.S.G
				''' % (dev_info[0][2], dev_info[0][3])
				self.messageTo(msg)
			self.save_ids[chat_id]['id'] = chat_id

		except Exception as e:
		   error_msg = "INFO ERROR["+str(chat_id)+"]"+"\n\t"+ str(e)
		   logger.warning(error_msg)

if __name__ == "__main__":
	logger.debug("==== START ====")
	print "[Price Alert Program]"
	print "\t["+threading.current_thread().name+"] : "+str(threading.current_thread().ident)
	try:
		manager = ProcessManager()
		update_thread = Updator()
		update_thread.setDaemon(True)
		update_thread.start()

		while 1:
			if manager.currency != None:
				break
			time.sleep(1)

		bot = telepot.DelegatorBot(manager.token, [
			pave_event_space()(
				per_chat_id(), create_open, PriceManager, timeout=None
			),
		])
		bot.message_loop(run_forever='Listening ...')

	except Exception as e:
		logger.ERROR("PROGRAM EXIST\n\t"+str(e))

	finally:
		logger.DEBUG("=== END ===")

