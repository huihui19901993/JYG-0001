##------------threading--------------##
#初步感受线程#
#---1--#
def testa():
  sleep(1)
  print 'a'
  
def testb():
  sleep(1)
  print 'b'
  
#执行顺序--testa---testb#
testa()
testb()
#---执行结果--#
#----先隔出一秒打印出a，再过一秒打印出b--#

#---以上程序用threading执行--#
#-----2---#
ta = threading.Thread(target=testa)
tb = threading.Thread(target=testb) 
for t in [ta,tb]:
  t.start()
  
for t in [ta,tb]:
  t.join()
print 'DONE'
#---执行结果---#
#---输出是ab或者ba（紧贴着的）然后空一行再来DONE的结果---#
####
    得到这样的结果是因为这样的，在start之后，ta先开始跑，但是主线程（脚本本身）没有等到其完成就继续开始下一轮循环，
然后tb开始，在之后的一段时间里，ta和tb两条线程（分别代表了testa和testb这两个过程）共同执行。相当于一个个迭代而言，
这样就大大提高了运行的速度
####
    Thread类为线程的抽象类，其构造方法的参数target指向一个函数对象，即该线程的具体操作。此外还有args=<tuple>来给
target函数传参数，需要注意的是当传任何一个序列进去的话，Thread会自动把它分解为单个单个的元素然后分解传给target函数。
    eg：threads.append(threading.Thread(target = monitor_service, args=(hostname, int(port),name, q)))
####
    join([timeout])方法阻塞了主线程，直到调用此方法的子线程完成之后主线程才继续往下运行。-------（执行我稀里糊涂的把
join紧紧接在start后面，如果这么写了的话那么多线程在速度上就毫无优势，和单线程一样了）。而像上面的例子一样，先一个遍
历把所有线程都启动起来，在用一个遍历把所有线程都join一般是比较通行的做法。

#-----3、线程锁--------#
#--------关于线程锁--------#
    多线程程序涉及到一个问题，那就是当不同线程要对同一个资源进行修改或利用时会出现混乱，所以有必要引入线程锁。
    可以通过 Thread.Lock 类来创建简单的线程锁。
    lock = threading.Lock()即可。
    在某线程start之前，让 lock.acquire(),且lock在acquire()之后不能再acquire，否则会报错。
    当线程结束后调用 lock.release()来释放锁。。
    一般而言，有锁的多线程场景可以提高一部分效率，但在写文件等时机下会有阻塞等待的情况
    相比之下，无锁多线程场景可以进一步提升效率，但是可能会引起读写冲突、资源等待等问题，一定要确认各个线程间没有公用的资源
之类的问题再实行无锁多线程。
    和Lock类类似的还有一个RLock类，与Lock类的区别在于RLock类锁可以嵌套地acquire和release。也就是说在同一个线程中acquire
之后再acquire也不会报错，而是将锁的层级加深一层。只有当每一层锁从下到上依次都release开这个锁才算是被解开。

#----------更强大的锁--Condition---------#
    上面提到的threading.Lock 类提供了最为简单的线程锁的功能，除此之外，threading还提供了一些其他的带有锁功能的类，其中
Condition为最为强大的类之一。
    在说Condition之前还需要明确一下线程的几个概念。
    线程的阻塞和挂起，线程的这两个状态乍一看都是线程暂停不再继续往前运行，但是引起的原因不太一样。
    阻塞是指线程间互相的制约，当一个线程获得了锁，其他的线程就被阻塞了，而挂起是出于统一调度的考虑。
    换句话说，挂起是一种主动的行为，在程序中我们主动挂起某个线程然后可以主动放下让线程继续运行；
    而阻塞更多时候是被动发生的，当有线程操作冲突了那么必然是有一方要被阻塞的。
    
    再来看看Condition类的一些方法。首先是acquire和release，Condition内部也维护了一把锁，默认是RLock类，所有关联了同一个
    Condition对象的线程也都会遵守这把锁规定的来进行运行。

　　Condition.wait([timeout])　　这个方法一定要在获取锁定之后调用，调用这个方法的Condition对象所在的线程会被挂起并且释放
这个线程获得着的所有锁，直到接到通知被唤醒或者超时（如果设置了Timeout的话），当被唤醒之后线程将重新获取锁定。
140
　　Condition.notify()　　notify就是上面所说的通知，调用这个方法之后会唤醒一个被挂起的线程。线程的选择尚不明确，似乎是随
机的。需要注意的是notify方法只进行挂起的唤醒而不涉及锁的释放

　　Condition.notify_all()　　唤醒所有挂起的线程
#---例子链接地址：https://www.cnblogs.com/franknihao/p/6627857.html-------#

#--------关于线程--------#

##--------------Queue-------------##
#--Queue用于建立和操作队列，常和threading类一起用来建立一个简单的线程队列--#
##-----首先队列有很多种，根据进出顺序分类，可以分成
##-----Queue.Queue(maxsize)         FIFO(先进先出队列) 
##-----Queue.LifoQueue(maxsize)     LIFO(先进后出队列)
##-----Queue.Priority(maxsize)      为优先度越低的越先出来
##-----如果设置的maxsize小于1，则表示队列的长度无限长
##---------------------------------------------------------------------##
##-----FIFO是常用的队列，其一些常用的方法有：
##-----Queue.qsize()     返回队列的大小
##-----Queue.empty()     判断队列是都为空
##-----Queue.full()      判断队列是否满了

