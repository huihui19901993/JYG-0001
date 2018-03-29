#############-----module_info.py-----#################
#入口#
#------1----#
from flask import Blueprint
from flask import request,render_template.jsonify
mi = Blueprint('module',__name__,static_folder="static")
@mi.route('/cov')
def coverage_view():
  return render_template('cov.html',title=u'覆盖率统计')
#------覆盖率统计首页------#

#-------2-----#
@mi.route('/api/cov/dump/<hostname>',methods = ['POST'])
def cov_trigger_dump(hostname):
  '''
  :param hostname
  '''
  result = dump_data(hostname)
#---------触发生成模块覆盖率统计原始文件-----------#

#-------3、module.py------#
#----3-1、module_info----#
#在之前的表结构上加一个字段cov_port，用于dump时端口指定#
from datetime import datetime
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc, ForeignKey, DateTime
#注：在代码里添加之后，需手动在项目运行的数据库对应表中添加字段#
class ModuleInfo(db.Model): 
  __tablename__ = 'moduleinfo'
  query_class = ModuleInfoQuery
  id =db.Column(db.Integer, primary_key=True,autoincrement=True)
  #------这里的module是table的名字，不是class的名字，另外不需要声明db.relationship的变量----#
  module_id =db.Column(db.Integer, ForeignKey('module.id'))
  module_name = db.Column(db.String(64))
  port = db.Column(db.Integer)
  dubbo_port = db.Column(db.Integer)
  cov_port = db.Column(db.Integer)
  host = db.Column(db.String(32))
  valid = db.Column(db.Integer,default=1)
  jvm_option = db.Column(db.String(8),default='M')
  http_monitor = db.Column(db.Boolean, defalut = False)
  dubbo_monitor = db.Column(db.Boolean, default = False)
  cov_monitor = db.Column(db.Boolean, default = False)
  pin_monitor = db.Column(db.Boolean, default = False)
    
#------------3-2、CovReport-----------#
class CovReport(db.Model):
    __tablename__ = 'covreport'
    query_class = CovReportQuery
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    host = db.Column(db.String(64))
    name = db.Column(db.String(64))
    valid = db.Column(db.Integer,default = 1)
    
#-------------------------------------#
#------查询结果不同格式返回-------#  
class ModuleInfoQuery(BaseQuery):
    def getHostCovModules(self, host):
        result = self.filter_by(host=host,valid=1,cov_monitor=1).all()
        return result
    def getProjectPathByModule(self,module_name):
        return self.with_entities(Project.path).filter(Project.id == Modules.project_id).filter(Modules.name == module_name).filter(Modules.valid==1).first()
    
#-----------相关数据库操作-------#

#---------4、生成dump文件且产生报告-----------#
import os
import subprocess
import datetime
from lxml import tree
#-----------dump_data-------#
def dump_data(host):
    '''
    :param host
    :return
    '''
    result = ""
    modules = ModuleInfo.query.getHostCoverModules(host)
    host_suffix = host.split('.')[-1]
    # ~/RyDeploy/static/report/224-20170818-180754，rpt_folder的目录形式
    rpt_name = host_suffix + '-' + datatime.datatime.now().strftime('%Y%m%d-%H%M%S')
    REPORT_BASE_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../static/report')
    JACOCO_CLI = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../ext','jacococli.jar')
    rpt_folder = os.path.join(REPORT_BASE_FOLDER, rpt_name)
    cov_rpt = CovReport(host=host,name = rpt_name)
    db.session.add(cov_rpt)
    total_data = {}
    
    for module in modules:
        #dump出来的文件名字
        #---dump---#
        #/Users/huihui/RyDeploy/services/../static/report/192.168.1.216-ryoms.exec
        cov_name = os.path.join(REPORT_BASE_FOLDER,host + "-" + module.module_name + ".exec" )
        dump_line = 'java -jar {} dump --address {} --port {} --retry 1 --destfile {}'.format(JACOCO_CLI,host,module.cov_port,cov_name)
        print 'dump_line','-'*10,dump_line
        p = subprocess.Popen(dump_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdoutdata, stderrdata) = p.communicate()
        if(stderrdata.find('Connection refused')>=0):
          result += "Can not connect to the module {} on {},check the catalina.sh file.".format(module.module_name, host)
          continue
          
          
        #----report----#
        project_name = Modules.query.getProjectPathByModule(module.module_name)[0]
        module_rpt_folder = os.path.join(rpt_folder, module.module_name)     
        # /home/rongyi/.jenkins/workspace/BUILD-easy-trade-162/easy-trade/easy-rpb/src/main/java
        # /home/rongyi/.jenkins/workspace/BUILD-easy-trade-162/easy-trade/easy-rpb/target/easy-rpb-5.7.2-SNAPSHOT/WEB-INF/classes
        # /home/rongyi/.jenkins/workspace/BUILD-easy-trade-162/easy-trade/easy-rpb/src/main/java
        # /home/rongyi/.jenkins/workspace/BUILD-trade-center-224/trade-checkout/build/classes/main
        # /home/rongyi/.jenkins/workspace/BUILD-trade-center-224/trade-checkout/src/main/java
        # easy-trade项目代码层级不一样，需要单独处理
        
        tmp_project_name = ""
        if(project_name == "easy-trade" or project_name == "easy-market"):
            tmp_project_name = project_name
        src_folder = os.path.join(JENKINS-WORKSPACE, 'BUILD-{}-{}'.format(project_name, host_suffix),tmp_project_name,
                                  module.module_name,"src/main/java")
        #gradle编译的class文件要特殊处理
        if(project_name == "trade-center"):
            cls_folder = os.path.join(JENKINS_WORKSPACE,'BUILD-{}-{}'.format(project_name,host_suffix),tmp_project_name,
                                      module.module_name,"build/classes/main")
        else:
            cls_folder = os.path.join(JENKINS_WORKSPACE,'BUILD-{}-{}'.format(project_name,host_suffix),tmp_project_name,
                                     module.module_name,"target",module.module_name + "*","WEB-INF/classes")
        
        report_line = 'java -jar {} report {} --sourcefiles {} --classfiles {} --html {}'.format(JACOCO_CLI, cov_name,
                                     src_folder, cls_folder, module_rpt_folder)
        print 'report_line','-'*10,report_line
        
        p = subprocess.Popen(report_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdoutdata,stderrdata) = p.communicate()
        print stderrdata
        if(stderrdata.find('No such file or directory') >= 0):
            result += 'Can not find source or class of the module {}.'.format(module.module_name)
            continue
            
        #------解析原始报告-------#
        
     #######################################   
        
        
 #------5、解析HTML报告------------#
from lxml import etree
def get_ratio(part,total):
  '''
  计算覆盖率的比例，返回百分比格式
  :param part:
  :param total:
  :return:
  '''
  if(total == 0):
    return "0"
  else:
    return "{:.1%}".format(float(part)/total)

def parse_report_cov(file_name):
  '''
  解析默认的报告，获取分支，行等覆盖率信息
  ：param file_name：原始报告的名字
  ：return：
  '''
  result = {}
  with open(file_name,'r') as f:
      total = etree.HTML(f.read())[1].xpath('//tfoot/tr/td')
      branch = total[3].text.replace(',','')
      result['branch_all'] = int(branch.split('of')[1])
      result['branch_cov'] = result['branch_all'] - int(branch.split('of')[0])
      result['line_all'] = int(total[8].text.replace(',',''))
      result['line_cov'] = result['line_all'] - int(total[7].text.replace(',',''))
      result['function_all'] = int(total[10].text.replace(',',''))
      result['function_cov'] = redult['function_all'] - int(total[9].text.replace(',',''))
      result['branch_ratio'] = get_ratio(result['branch_cov'],result['branch_all'])
      result['line_ratio'] = get_ratio(result['line_cov'],result['line_all'])
      result['function_ratio'] = get_ratio(result['function_cov'],result['function_all'])
      return result
#---------------------------------#
        
        
