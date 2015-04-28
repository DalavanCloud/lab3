import sensor
import threading
import time
import os
import csv
import sys
sys.path.append("./")
import setting

#get ip information from setting file 
serveradd = setting.serveradd
localadd = setting.localadd[os.path.basename(__file__).split('.',1)[0]]
devNum = setting.devNum

class temperature (threading.Thread):
    def __init__(self,client):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.client = client

    def run(self):
        self.client.start_listen()


def main(): 
    def readTest(filename,col):
        ''' read testcase from file, col being the number of col interested'''
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            time=[]
            action=[]
            spamreader.next()
            for row in spamreader:
                time.append(row[0])
                action.append(row[col])     
            return time, action    



    def interaction(temp,timel,action):
        
        if action[0]!='Register':
            print "Error: register client first"
        temp.register_to_server()
        time.sleep(float(timel[1])+float(setting.start_time) - time.time())
        for index in range(1,len(timel)-1):
            temp.set_state(action[index])

            waitTime = float(timel[index+1])+float(setting.start_time) - time.time()
            if waitTime>0:
                time.sleep(waitTime)

        temp.set_state(action[len(timel)-1])
        
      
    def start_sync():
        '''sync time of different process before running'''
        current_time = int(time.time())
        waitT = setting.start_time - current_time
        time.sleep(waitT)

    temp = sensor.Sensor("temperature",serveradd,localadd,devNum)
    
    # create a thread to listen, deal with server pulls
    temp.leader_elect()
    temp.time_syn()
    listen_thread = temperature(temp)
    listen_thread.start()
    

    timel,action= readTest('test-input.csv',1)

    start_sync()
    interaction(temp,timel,action)  
    time.sleep(10)

if __name__ == "__main__":
    main()