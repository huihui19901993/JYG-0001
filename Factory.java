import android.util.Log;

#a、定义一个发送的类，一个发送的抽象方法
public interface Sender{
  void send();
}


# b、定义2个类（邮件发送和短信发送），实现2个发送方法
public class MailSend implements Sender {
  @override
  public void send(){
    Log.d("金阳光","------------>邮件发送")；
  }
}

public class SmsSend implements Sender {
  @override
  public void send(){
    Log.d("金阳光","------------>短信发送")；
  }
}

# c、定义一个发送工厂（传递String参数，来判断初始化哪个类）
public class SendFactory {
  public Sender produce(String s) {
    if(s.equals("mial")){
      return new MailSend();
    }else if (s.equals("sms")){
      return new SmsSender();
    }
    return null;
  }
}

#d、我们测试下（输入一个sms参数初始化短信构造器实例化发送短信对象）
  case R.id.button3:
    //设计模式-工厂模式
    //工厂模式
    SendFactory sendFactory = new SendFactory();
    Sender sender = sendFactory.product("sms");
    sender.send();
    break;
    
    
 //2、静态工厂
public class SendFactory{
  public Sender emailProduce(){
    return new MailSend();
  }

  public Sender smsProduce(){
    return new SmsSend();
  }
}
  case R.id.button2:
  //多工厂模式
  SendFactory sendFactory = new SendFactory();
  Sender sender = sendFactory.emailProduct();
  sender.send();
  break;
  
//普通工厂模式把实例化交给统一一个方法，用户只要传递不同对象名字就产生不同实例化；
//多工厂的静态工厂则是一个对象对应一个工厂方法，这样编写程序的人不容易写错，普通工厂模式那些不同对象名字太多，容易传错




