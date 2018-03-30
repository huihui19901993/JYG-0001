#目前有很多xml,html文档的parser，如标准库的xml.etree,beautifulsoup,还有lxml
#使用和比较之后选择了lxml
#围绕三个问题：
#1、有一个xml或html文件，如何解析
#2、解析后，如何查找、定位某个标签
#3、定位后如何操作标签，比如访问属性、文本内容等

#！/usr/bin/python
#coding=utf-8
'''
Element是XML处理的核心类
Element对象可以直观的理解为xml的节点，大部分xml节点的处理都是围绕该类进行的
这部分包括三个内容：节点的操作，节点属性的操作、节点内文本的操作
'''
from lxml import etree

#1、创建element
root = etree.Element('root')
print root,root.tag

#2、添加子节点
child1 = etree.SubElement(root,'child1')
child2 = etree.SubElement(root,'child2')

#3、删除子节点
#root.remoove(child2)
#4、删除所有子节点
#root.clear()

#5、以列表的方式操作子节点
print (len(root))
print root.index(child1) #索引号
root.insert(0,etree.Element('child3')) #按位置插入
root.append(etree.Element('child4'))   #尾部添加

#6、获取父节点
print (child1.getparent().tag)

'''以上都是节点操作'''

#7、创建属性
#root.set('hello','dahu') #set(属性名，属性值)
#root.set('hi','qing')

#8、获取属性
# print（root.get('hello')）  #get方法
# print root.keys(),root.values(),root.items()   #参考字典的操作
# print root.attrib  #直接拿到属性存放的字典，节点的attrib，就是该节点的属性

'''以上是属性的操作'''

# 9、text和tail属性
# root.text = 'hello,world'
# print root.text

#10、tail和text的结合
html = etree.Element('html')
html.text = 'html-text'
body = etree.SubElement(html,'body')
body.text = 'wo ai ni'
child = etree.SubElement(body,'child')
child.text = 'child-text'  #一般情况下，如果一个节点的text没有内容,就只有</>符号,如果有内容,才会<>,</>都有
child.tail = 'tails' #tail是在标签后面追加文本
print (etree.tostring(html))
# print (etree.tostring(html,method='text'))  #只输出text和tail这种文本文档，输出内容连在一起，不实用

#11.Xpath方式
# print(html.xpath('string()'))   #这个和上面的方法一样,只返回文本的text和tail
print(html.xpath('//text()'))   #这个比较好,按各个文本值存放在列表里面
tt=html.xpath('//text()')
print tt[0].getparent().tag     #这个可以,首先我可以找到存放每个节点的text的列表,然后我再根据text找相应的节点
# for i in tt:
#     print i,i.getparent().tag,'\t',

#12.判断文本类型
print tt[0].is_text,tt[-1].is_tail  #判断是普通text文本,还是tail文本
'''以上都是文本的操作'''

#13.字符串解析,fromstring方式
xml_data = '<html>html.text<body>wo ai ni<child>child.text</child>tails</body></html>'
root1=etree.fromstring(xml_data)    #fromstring,字面意思,直接来源字符串
# print root1.tag
# print etree.tostring(root1)

#14.xml方式
root2 = etree.XML(xml_data)     #和fromstring基本一样,
print etree.tostring(root2)

#15.文件类型解析
tree =etree.parse('text')   #文件解析成元素树
root3 = tree.getroot()      #获取元素树的根节点
print etree.tostring(root3,pretty_print=True)

parser= etree.XMLParser(remove_blank_text=True) #去除xml文件里的空行
root = etree.XML("<root>  <a/>   <b>  </b>     </root>",parser)
print etree.tostring(root)

#16.html方式
xml_data1='<root>data</root>'
root4 = etree.HTML(xml_data1)
print(etree.tostring(root4))#HTML方法，如果没有<html>和<body>标签，会自动补上
#注意,如果是需要补全的html格式:这样处理哦
with open("quotes-1.html",'r')as f:
    a=H.document_fromstring(f.read().decode("utf-8"))

for i in  a.xpath('//div[@class="quote"]/span[@class="text"]/text()'):
    print i

#17.输出内容,输出xml格式
print etree.tostring(root)
print(etree.tostring(root, xml_declaration=True,pretty_print=True,encoding='utf-8'))#指定xml声明和编码
'''以上是文件IO操作'''

#18.findall方法
root = etree.XML("<root><a x='123'>aText<b/><c/><b/></a></root>")
print(root.findall('a')[0].text)#findall操作返回列表
print(root.find('.//a').text)   #find操作就相当与找到了这个元素节点,返回匹配到的第一个元素
print(root.find('a').text)
print [ b.text for b in root.findall('.//a') ]    #配合列表解析,相当帅气!
print(root.findall('.//a[@x]')[0].tag)  #根据属性查询
'''以上是搜索和定位操作'''
print(etree.iselement(root))
print root[0] is root[1].getprevious()  #子节点之间的顺序
print root[1] is root[0].getnext()
'''其他技能'''
# 遍历元素数
root = etree.Element("root")
etree.SubElement(root, "child").text = "Child 1"
etree.SubElement(root, "child").text = "Child 2"
etree.SubElement(root, "another").text = "Child 3"
etree.SubElement(root[0], "childson").text = "son 1"
# for i in root.iter():   #深度遍历
# for i in root.iter('child'):    #只迭代目标值
#     print i.tag,i.text
# print etree.tostring(root,pretty_print=True)















