import Queue
import json
import requests
import telnetlib
import threading

def monitor_dubbo(hostname, name_port):
  ```
  检查dubbo的provider服务是否正常
  ：param  hostname
  ：param  name_port：字典格式  {'easy-roa':'29000','easy-mobile':'29100'}
  ：return 
  ```
  result = {}
  threads = {}
  #这里的q，如果申明为全局变量，会导致不同的请求过来，结果混乱，比如162环境的数据，返回到186的结果中
  q = Queue.Queue()
  for name,port in name_port.items():
    threads.append(threading.Thread(target = monitor_dubbo_service,args=(hostname, int(port),name,p)))
  for t in threads:
    t.start()
  for t in threads:
    t.join() 
  while not q.emlty():
    result.update(q.get)
  return result

def monitor_dubbo_service(hostname, port, name, p):
  msg = 'ERROR'
  try:
    tn = telnetlib.Telnet(hostname,port)
    tn.write('status \n')
    msg = tn.read_until('dubbo>',1)
  except:
    msg = 'ERROR'
  msg = msg.split('\r')[0]
  q.put({name:msg})
  return msg

if __name__=='__main__':
  hostname = '192.168.1.186'
  hostnames = ['192.168.1.216','192.168.1.186']
  for hostname in hostnames:
    a = requests.get('http://localhost:5000/api/module/dubboport' + hostname).text
    name_port = json.loads(a)
    monitor_dubbo(hostname,name_port)
