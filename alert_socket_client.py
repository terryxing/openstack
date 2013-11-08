# this python code does the following 3 things
# 1: fectch the alert information from the unix domain socket.
# 2: parse the alert information and dump into the json message format
# 3: send the json message to the pox controller through port 8987

#!/usr/bin/env python
import pcap
import os
import sys
import socket
import struct
import string
import time
#import simplejson
import json
from pwd import getpwnam
from grp import getgrnam

# from src/decode.h
ALERTMSG_LENGTH=256
SNAPLEN=1500

protocols = {socket.IPPROTO_TCP:'tcp', socket.IPPROTO_UDP:'udp', socket.IPPROTO_ICMP:'icmp'}

def main():
	so = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
	sout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sout.connect(("127.0.0.1", 8987))

	
# This format does NOT include the 'Event' struct which is the last element
# of the _AlertPkt struct in src/output-plugins/spo_alert_unixsock.h
# Thus, we must truncate the messages ('datain[:fmt_size]') before passing
# them to struct.unpacket()
	fmt = "%ds9I%ds" % (ALERTMSG_LENGTH, SNAPLEN)
	fmt_size = struct.calcsize(fmt)

        # make sure the socket file does not exist before call os.bind()
	try:
  		os.remove("/var/log/snort/snort_alert")
  	except OSError:
		pass
        #create the socket file 
	so.bind("/var/log/snort/snort_alert")
	os.chown("/var/log/snort/snort_alert", getpwnam('snort')[2], getgrnam('snort')[2])
	while True:
  		try:
      			(datain, addr) = so.recvfrom(4096)
      			(msg, ts_sec, ts_usec, caplen, pktlen, dlthdr, nethdr, transhdr, data, val, pkt) = struct.unpack(fmt, datain[:fmt_size])
                        #print all debug info
			print "DEBUG---------------------%s.%f > %s" % (time.strftime('%H:%M', time.localtime(ts_sec)), ts_usec , msg)
			print " DEBUG------------------- caplen:%d, pktlen:%d, dlthdr:%d, nethdr:%d, transhdr:%d, data:%d, val:%d" % (caplen, pktlen, dlthdr, nethdr, transhdr, data, val)
			
			json_data = print_packet(pktlen, msg, ts_sec, ts_usec, pkt)
			json_data["msg_reason"] = "ICMP Test" #msg.rstrip()
			json_data["msg_type"] = "Alert"
            #		jsonData = simplejson.dumps(json_data, ensure_ascii=True)
			jsonData = json.dumps(json_data, ensure_ascii=True)
			print "JSON: ", jsonData
	    # send the jsonData to the pox controller over TCP socket.
			sout.send(jsonData)

# optionally, do something with the pcap pkthdr (ts_sec+ts_usec+caplen+pklen) and
# packet body (pkt)
		except struct.error, e:
  			print "bad message? (msglen=%d): %s" % (len(datain), e.message)

def decode_ip_packet(s):
	d = {}
	d['version']=(ord(s[0]) & 0xf0) >> 4
	d['header_len']=ord(s[0]) & 0x0f
	d['tos']=ord(s[1])
	d['total_len']=socket.ntohs(struct.unpack('H', s[2:4])[0])
	d['id']=socket.ntohs(struct.unpack('H', s[4:6])[0])
	d['flags']=(ord(s[6]) & 0xe0) >> 5
	d['fragment_offset']=socket.ntohs(struct.unpack('H', s[6:8])[0] & 0x1f)
	d['ttl']=ord(s[8])
	d['protocol']=ord(s[9])
	d['checksum']=socket.ntohs(struct.unpack('H', s[10:12])[0])
	d['source_address']=pcap.ntoa(struct.unpack('i', s[12:16])[0])
	d['destination_address']=pcap.ntoa(struct.unpack('i', s[16:20])[0])
	if d['header_len'] > 5:
		d['option']=s[20:4*(d['header_len']-5)]
	else:
		d['option']=None
	d['data']=s[4*d['header_len']:]
	return d

def dumphex(data):
	bytes = map(lambda x: '%.2x' % x, map(ord, data))
	for i in xrange(0, len(bytes)/16):
		print "    %s" % string.join(bytes[i*16:(i+1)*16],' ')
	print "    %s" % string.join(bytes[(i+1)*16:],' ')

def print_packet(pktlen, msg, ts_sec, ts_usec, data):
	if not data:
		return
	ret_data = {}
	ret_data["type"] = "pyswitch"

	print "\n%s.%f > %s" % (time.strftime('%H:%M', time.localtime(ts_sec)), ts_usec , msg)
	#ret_data['msg'] = msg
	if data[12:14] == '\x08\x00':
		bytes = map(lambda x: '%.2x' % x, map(ord, data))
		src_mac = string.join(bytes[6:12],':')
		dst_mac = string.join(bytes[0:6], ':')
		ret_data["src_mac"] = src_mac
		ret_data["dst_mac"] = dst_mac
		print "  src_mac: %s > dst_mac: %s" % (src_mac, dst_mac)
		decoded=decode_ip_packet(data[14:])
		src_ip = decoded['source_address']
		dst_ip = decoded['destination_address']
		ret_data["src_ip"] = src_ip
		ret_data["dst_ip"] = dst_ip
		print "  src_ip: %s > dst_ip: %s" % (src_ip, dst_ip)

		for key in ['version', 'header_len', 'tos', 'total_len', 'id', 
				'flags', 'fragment_offset', 'ttl']:
			print "  %s: %d" % (key, decoded[key])
		print "  protocol: %s" % protocols[decoded['protocol']]
		print "  header checksum: %d" % decoded['checksum']
		#print "  data:"
		#dumphex(decoded['data'])
		return ret_data
		
if __name__ == '__main__':
	main()

