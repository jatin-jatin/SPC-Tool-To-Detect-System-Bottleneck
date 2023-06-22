#!/usr/bin/python3
import socket
from time import sleep
import json
import os
import subprocess
import tarfile
import shutil
from twisted.cred.checkers import AllowAnonymousAccess,InMemoryUsernamePasswordDatabaseDontUse
from twisted.cred.portal import Portal
from twisted.internet import reactor
from twisted.protocols.ftp import FTPFactory,FTPRealm

def FTPthread():
    if os.path.isdir("public") == False:
        os.makedirs("public")
    portal = Portal(FTPRealm("./public"),[AllowAnonymousAccess()])
    factory = FTPFactory(portal)
    reactor.listenTCP(5001,factory)
    reactor.run()
    reactor.stop()

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def extractLogs(testName,numExtract):
    # to extract logs based on locations from components.json
    if os.path.isdir("logs") == False:
        os.makedirs("logs")
    if os.path.isdir("logs/"+testName) == False:
        os.makedirs("logs/"+testName)
    json_file=open(componentsFileName,"r")
    components=json.load(json_file)
    json_file.close()
    direc="logs/"+testName+"/"
    print(components)
    for component in components:
        file_name=component["componentName"]+"-"+testName+".log"
        fd = open(direc+file_name,"w+")
        command = ["tail","-n",str(numExtract),component["logPath"]]
        grepCommand=["grep","-a",testName]
        tempfd=open(".temp","w+")
        proc1=subprocess.run(command,stdout=tempfd)
        tempfd.close()
        tempfd=open(".temp","r+")
        proc2=subprocess.run(grepCommand,stdin=tempfd,stdout=fd)
        tempfd.close()
        fd.close()
    os.chdir("logs")
    tarfileName=testName+".tar.gz"
    make_tarfile(tarfileName,testName)
    os.chdir("..")
    shutil.copy('logs/'+tarfileName,'public')
    data="ExtractionComplete"
    return data

def serverLogExtraction():
    host = "0.0.0.0"
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))

        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if data =="":
            print("received empty message from client")
            exit(1)
        msg_lst = data.split(",") 

        # Extract logs and fork an ftp-server
        if msg_lst[0] == "ExtractLogs":
            global childid
            childid=os.fork()
            if childid==0:
                FTPthread()
            print("TestName:",msg_lst[1])
            print("numLinesExtract:",msg_lst[2])
            data = extractLogs(msg_lst[1],msg_lst[2])
            print(data)
            conn.send(data.encode()) 

        # kill the ftp-server
        elif msg_lst[0]=="CloseFTPServer":
            killcommand=["kill","-9",str(childid)]
            subprocess.run(killcommand)
            sleep(2)
            data="FTPServerClosed"
            print(data + " procesesid:",childid)
            conn.send(data.encode()) 
            conn.close()  # close the connection
        endMessage="-----------------------------"
        print(endMessage)



if __name__ == '__main__':
    try:
        global componentsFileName
        componentsFileName="components.json"
        serverLogExtraction()
    except KeyboardInterrupt:
    
        print("")
        print("Exiting")
        

