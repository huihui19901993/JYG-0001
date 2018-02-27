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

#-------3------#
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
#------查询结果不同格式返回-------#  
class ModuleInfoQuery(BaseQuery):
#-----------相关数据库操作-------#
