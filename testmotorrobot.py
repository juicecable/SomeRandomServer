#Copyright (c) 2020 Derek Frombach

from PIL import Image
import cv2
import io
import time
import socket

ip="0.0.0.0" #Don't Change This
#remhost='192.168.0.2'
remhost='localhost'
remport=8082
port=8081 #Hosting Port, Don't Change This
buff=1400 #Also Don't Change This

#Initalisation of TCP Socket Server
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP/IP Socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Unbind when Done
s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero-Latency TCP

s.bind((ip,port)) #Starting Connect Back Server
s.listen(1) #Listen for Connections

#Function Call Speedups
#tc=time.clock
tc=time.perf_counter
tt=time.time
ts=time.sleep
cvt=cv2.cvtColor
bgr=cv2.COLOR_BGR2RGB
ifa=Image.fromarray
bio=io.BytesIO
st=s.settimeout
ste=socket.timeout
rdwr=socket.SHUT_RDWR
se=socket.error

print('Accepting Clients')
ip=False
while True:
    try:
        conn,addr=s.accept()
    except KeyboardInterrupt:
        exit()
    ct=conn.settimeout
    ct(0.1)
    #Header Communication with Client
    cs=conn.sendall #Connection Speedup
    ts(0.1)
    #Client Timeout Handler
    try:
        data=conn.recv(buff)
    except ste:
        print("BOT!")
        conn.shutdown(rdwr)
        conn.close()
        continue
    except se:
        conn.shutdown(rdwr)
        conn.close()
        continue
    if len(data)>1:
        dstr=data.decode('utf-8')
        data=dstr.find('Passwd: ')
        if data>=0:
            try:
                q=int(dstr[data+8:data+12])
            except:
                print("BOT!")
                conn.shutdown(rdwr)
                conn.close()
                continue
            r=int(input('Enter the Key: '))
            if q==r:
                print('Keys Match!')
                try:
                    cs(('Match: '+str(r)).encode('utf-8'))
                except:
                    print('Early Disconnect!')
                    continue
                ip=addr[0]
                try:
                    conn.shutdown(rdwr)
                    conn.close()
                except:
                    pass
                break
        else:
            print("BOT!")
            conn.shutdown(rdwr)
            conn.close()
            continue
    else:
        print("BOT!")
        conn.shutdown(rdwr)
        conn.close()
        continue
#Recieving Pairing Request was successful, now off to pairing land
ts(2.0)
s.close()

#Initalisation of Camera
cap = cv2.VideoCapture(0)

#Initalisation of Log File
f = open('vidDebug.log','a') #Don't Change This

#Mandatory HTTP Headers (Required for Functionality)
iostr="\r\n--R2lpaXUgU3dmYW5iY2o0\r\nContent-Type: image/jpeg\r\nContent-Length: ".encode("utf-8")
estr="\r\n\r\n".encode("utf-8")

#Initalisation of Address
print("READY!")
addr=(ip,port)

#Function Call Speedups
cr=cap.read
fw=f.write
ff=f.flush

#Continuity Loop
while True:
    conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP/IP Socket
    conn.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero-Latency TCP
    ct=conn.settimeout
    
    #Do Not Change Anything Below, All of this is Security
    print("Disconnected")
    print(tt())
    print(addr)
    fw("Disconnected\n")
    fw(str(tt())+"\n")
    fw(str(addr[0])+", ")
    fw(str(addr[1])+"\n")
    ff()
    
    #Ctrl-C Handler
    try:
        conn.connect(addr)
    except KeyboardInterrupt:
        break
    except ste:
        conn.close()
        continue
    except se:
        conn.close()
        continue
    ct(0.1)
    
    print("Connected")
    print(tt())
    print(addr)
    fw("Connected\n")
    fw(str(tt())+"\n")
    fw(str(addr[0])+", ")
    fw(str(addr[1])+"\n")
    ff()
    ct(0.1)
    #Do Not Change Anything Above
    
    
    #Header Communication with Client
    cs=conn.sendall #Connection Speedup
    cv=conn.recv #Connection Speed
    #Client Timeout Handler
    try:
        data=cv(buff)
    except ste:
        print("BOT!")
        fw("BOT!\n")
        conn.shutdown(rdwr)
        conn.close()
        continue
    except se:
        conn.shutdown(rdwr)
        conn.close()
        continue
    
    #Also Mandatory HTTP Headers
    ostr="HTTP/1.1 200 OK\r\nConnection: close\r\nServer: PyVidStreamServer MJPEG SERVER\r\nCache-Control: no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0\r\nPragma: no-cache\r\nExpires: -1\r\nAccess-Control-Allow-Origin: *\r\nContent-Type: multipart/x-mixed-replace;boundary=R2lpaXUgU3dmYW5iY2o0\r\n\r\n"

    o=ostr.encode("utf-8")
    #Server Connection Failure Handler
    try:
        cs(o) #Sending Header
    except ste:
        print("BOT!")
        fw("BOT!\n")
        conn.shutdown(rdwr)
        conn.close()
        continue
    except se:
        conn.shutdown(rdwr)
        conn.close()
        continue
    
    
    #grab initial image here
    ret, frame = cr()
    frame = cvt(frame, bgr)
    img=ifa(frame)

    #Connecting to Serial Here
    #Initalisation of TCP Socket Server
    rs=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP/IP Socket
    rs.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1) #Zero-Latency TCP
    #connect with robot
    rs.settimeout(0.1)
    rs.connect((remhost,remport))
    rss=rs.sendall
    
    #Capture Loop
    while True:
        
        a=tc()#Start Time for Frame Limiting

        #Client Timeout Handler
        try:
            data=cv(buff)
        except ste:
            print("LATENCY!")
            fw("LATENCY!\n")
            conn.shutdown(rdwr)
            conn.close()
            break
        except se:
            print("SOCKET ERROR!")
            fw("SOCKET ERROR!\n")
            conn.shutdown(rdwr)
            conn.close()
            break

        #Data Interpreter
        if len(data)>=12:
            rss(data)
        
        #img grabbing goes here
        ret, frame = cr()
        frame = cvt(frame, bgr)
        img=ifa(frame)
        
        #Converting Raw Image into Compressed JPEG Bytes
        with bio() as output:
            img.save(output,format="JPEG",quality=35)
            contents=output.getvalue()
            
        #Concatenating Contents and Headers
        o=iostr
        o+=str(len(contents)).encode("utf-8")
        o+=estr
        o+=contents
        
        #Sending Contents to Client
        try:
            cs(o)
        except:
            break
            
        #frame rate limiter
        b=tc() #End Time for Frame Limiting
        c=b-a
        t=1/30 #seconds per frame
        if t-c>0.0:
            ts(t-c) #delay remaining seconds
        elif c>t:
            #pass
            print(c)
            
#End of Program (when Ctrl-C)
f.close()
cap.release()
s.close()
conn.close()
