//金阳光-2017-03-03
//人工智能-多线程模式

//有一个场景：一家人准备下班后去北京王府井吃饭。
//老爸离的最远要3小时到，老妈其次2小时到，我最近1小时到。那我们怎么写测试程序呢

//1、定义一个familyToRes，用休眠3秒、2秒、1秒来代替3、2、1小时

public class FamilyToRes {
  public static void fatherToRes(){
    Log.i("金阳光","--------->父亲去餐馆3小时");
    try {
      Thread.sleep(3000);
    } catch (InterruptedException e){
      e.printStackTrace();
    }
  }
  public static void motherToRes(){
    Log.i("金阳光","---------->母亲去餐馆2小时");
    try {
      Thread.sleep(2000);
    }catch(InterruptedException e){
      e.printStackTrace();    
    }
  }
  public static void myToRes(){
    Log.i("金阳光","------------->我去餐馆1小时");
    try(
      Thread.sleep(1000);
    )catch(InterruptedException e){
      e.printStackTrace();
    }
  }
//------------------//
//2、所有人到了，可以一起吃饭了
  public static void arriver(String name){
    Log.i("金阳光","---------->" + name + "已到达");
  }
  
  public static void togetherToEat(){
    Log.i("金阳光","------------->一家人到了一起吃饭！！");
  }
  
//main 测试
//3、写三个多线程测试下
  public static void main(String args[]){
    //--------------test1----------------//
    public static void test1(){
      //这是错误的程序，达不到想要的效果
      new Thread(){
        @override
        public void run(){
          fatherToRes();
        }
      }.start();
      new Thread(){
        @override
        public void run(){
          motherToRes();
        }
      }.start();
      new Thread(){
        @override
        public void run(){
          myToRes();
        }
      }.start();
      togetherToEat();
    }           // 结果为，三个线程随机执行，大家还没到一起就吃饭了
    //------------------test1----end-------------//
    
    //------------------------test2----------------//
    //那么正确的程序应该如何写呢？
    //我们定义一个计数器。当某个人到了计数器减一，再设置一个死循环来不断判断i是否等于0.
    private static volatile int i =3;
    public static void test2(){
      i = 3;
      new Thread(){
        @override
        public void run(){
          fatherToRes();
          i--;
          arriver("爸爸");
        }.start();  
      }
    
      new Thread(){
        @override
        public void run(){
          motherToRes();
          i--;
          arriver("妈妈");
        }.start();
      }
      
      new Thread(){
        @override
        public void run(){
          myToRes();
          i--;
          arriver("我");
        }.start();
      }
      
      while(true){
        Log.i("金阳光","-------------->" + i);
        if (i == 0){
          break;
        }
      }
      togetherToEat();
    }
    //运行结果为：
    /*
      妈妈去餐馆2小时
      我去餐馆1小时
      父亲去餐馆3小时
      我已到达
      妈妈已到达
      爸爸已到达
      一家人到了一起吃饭！
    */
    
    //-------------------test2--end----------------------//
    
    //------------------------test3----------------//
    /*
      测试发现，test2资源消耗甚大，一个死循环。是否有更好的方法呢，答案是有的
      设置一个同步线程助手类CountDownLatch,他可以不断监听多个线程，并在线程完成时做出响应
    */
    public static void test3(){
      //利用CountDownLatch类达到线程同步
      final CountDownLatch lath = new CountDownLatch(3);
      new Thread(){
        @override
        public void run(){
          fatherToRes();
          arriver("爸爸");
          lath.countDown();
        }
      }.start();
      
      new Thread(){
        @override
        public void run(){
          motherToRes();
          arriver("妈妈");
          lath.countDown();
        }
      }.start();
      
      new Thread(){
        @override
        public void run(){
          myToRes();
          arriver("我");
          lath.countDown(); // 当线程完毕，计数器减一
        }
      }.start();
      
      try{
        lath.await(); //等待所有线程完成
        togetherToEat();
      }catch(InterruptedException e){
        e.printStackTrace();
      }
    }
    /*  运行的结果如下：
        父亲去餐馆3小时
        妈妈去餐馆2小时
        我去餐馆1小时
        我已到达
        妈妈已到达
        爸爸已到达
        一家人到了一起吃饭！
    
    */
    //-------------------test3--end----------------------//
  }
  
//   -------end------   //
}

