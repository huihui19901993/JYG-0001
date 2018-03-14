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
        
#-----------相关数据库操作-------#

#---------4、生成dump文件且产生报告-----------#
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
        #/Users/huihui/RyDeploy/services/../static/report/192.168.1.216-ryoms.exec
        cov_name = os.path.join(REPORT_BASE_FOLDER,host + "-" + module.module_name + ".exec" )
        dump_line = 'java -jar {} dump --address {} --port {} --retry 1 --destfile {}'.format(JACOCO_CLI,host,module.cov_port,cov_name)
        


#------------------#
