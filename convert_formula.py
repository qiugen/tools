#/usr/bin/python
#coding=utf8
import sys

#读取post_file
def load_post_file(md_file):
	_post_str = ''
	with open(md_file) as f1:
		for eachline in f1:
			_post_str += eachline;
	return _post_str

#寻找$-$对或者$$-$$对
def find_next_dollar_pair(md_str):

	if len(md_str) == 0:
		return False, None
	head=-1
	end=-1
	
	for inx in range(len(md_str)):
		if md_str[inx] == u'$' and head==-1:
			head = inx
			break
			
	if head == -1:
		return False, None
	#跳过连续的$
	jump_head = head + 1
	for inx in range(head+1, len(md_str)):
		if md_str[inx] == u'$':
			jump_head += 1
		else:
			break
	#判断寻找下一个有效$结尾			
	for inx in range(jump_head,len(md_str)):
		if md_str[inx] == u'$' and end == -1:
			end = inx
			break
	real_end = end + 1
	for inx in range(end+1, len(md_str)):
		if md_str[inx] == u'$':
			real_end += 1
		else:
			break
	return True, (head, real_end)

#写入新的post_file
def write_post_file(md_file,u_post_str):
	f = open(md_file, 'w')
	f.write(u_post_str.encode('utf8'))
	f.close()	
	return True

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print >>sys.stderr, 'usage: python %s md_file target_file' % sys.argv[0]
		sys.exit(-1)
	md_file = sys.argv[1]
	target_file = sys.argv[2]
	_post_str = load_post_file(md_file)
	u_post_str = _post_str.decode('utf8')
	#print u_post_str.encode('gb18030')

	new_post_str = ''
	ret = True
	while ret == True:
		ret, pos_pair = find_next_dollar_pair(u_post_str)
		if ret == True:
			start=pos_pair[0]
			end=pos_pair[1]
			new_post_str += u_post_str[:start] + u"{% raw %}"
			new_post_str += u_post_str[start:end] + u"{% endraw %}"
			u_post_str = u_post_str[end:]
		else:
			new_post_str += u_post_str
	write_post_file(target_file,new_post_str)
