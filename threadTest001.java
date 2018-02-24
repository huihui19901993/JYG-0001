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
  
//   -------end------   //
}

