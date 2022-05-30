import os
import socket
import select
import random
import shutil

from Config import HOST, PORT, MAX_WAITING
from KeyAgreement import keyAgreementServer, sendNewAesKey

STORE_PATH = os.getcwd() + '\\Store\\'


class NetDiskServer():
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.listen(MAX_WAITING)
        self.server.setblocking(False)

        self.inputs = []
        self.outputs = []

        self.pipe_info = {}

        self.inputs.append(self.server)

    def runServer(self):
        while True:
            readable, writable, exceptional = select.select(
                self.inputs, self.outputs, self.inputs)

            for reader in readable:
                if reader == self.server:
                    conn, addr = reader.accept()
                    print(f'Connected with: {addr}')
                    self.inputs.append(conn)
                    conn.setblocking(True)
                    aesPipeIN, aesPipeOUT = keyAgreementServer(conn)
                    self.pipe_info[conn] = {}
                    self.pipe_info[conn]['type'] = 'CMD pipe'
                    self.pipe_info[conn]['aesPipeIN'] = aesPipeIN
                    self.pipe_info[conn]['aesPipeOUT'] = aesPipeOUT
                    self.pipe_info[conn]['usrId'] = None
                    self.pipe_info[conn]['usrPwd'] = None
                    aes_key = sendNewAesKey(aesPipeOUT)
                    conn.setblocking(False)
                    ftt = FileTransferTasks()
                    ftt.channelSetup(aes_key)
                    # test
                    ftt.pipe.setblocking(True)
                    self.pipe_info[conn]['ftt'] = ftt
                    self.pipe_info[ftt.pipe] = {}
                    self.pipe_info[ftt.pipe]['type'] = 'FTT pipe'
                    self.pipe_info[ftt.pipe]['ftt'] = ftt
                    self.pipe_info[ftt.pipe]['aesPipeIN'] = aesPipeIN
                    self.pipe_info[ftt.pipe]['aesPipeOUT'] = aesPipeOUT
                    ftt.usr_id = None
                    ftt.usr_pwd = None
                    self.inputs.append(ftt.pipe)
                    # SECTION only for test
                    # print(ftt.in_pipe())
                    ftt.pipe.setblocking(False)
                    # !SECTION

                # FIXME
                elif self.pipe_info[reader]['type'] == 'CMD pipe':
                    aesPipeIN = self.pipe_info[reader]['aesPipeIN']
                    msg = aesPipeIN()
                    # if msg == '', so the client is closed
                    if msg == '':
                        print('Closing', reader.getpeername())
                        self.inputs.remove(reader)
                        if reader in self.outputs:
                            self.outputs.remove(reader)
                        reader.close()
                        continue
                    cmd = msg[:8].strip('@')

                    if cmd == 'Show':
                        print(msg)

                    elif cmd == 'Download':  # means Download
                        print('got download req')
                        ftt = self.pipe_info[reader]['ftt']
                        usr_pwd = self.pipe_info[reader]['usrPwd']
                        req_cmd = ftt.downloadReqResponse(
                            msg, usr_pwd.encode())
                        aesPipeOUT = self.pipe_info[ftt.pipe]['aesPipeOUT']
                        aesPipeOUT(req_cmd)

                    elif cmd == 'FileIn':
                        ack_cmd = msg
                        ftt = self.pipe_info[reader]['ftt']
                        ftt.awakeOutTask(ack_cmd[8:8 + 32])
                        self.outputs.append(ftt.pipe)

                    elif cmd == 'FileOut':  # means Upload
                        print('got fileout cmd')
                        ftt = self.pipe_info[reader]['ftt']
                        idx = 8
                        task_id = msg[idx:idx + 32]
                        idx += 32
                        file_sz = int(msg[idx:idx + FILE_SZ_WIDTH], 16)
                        idx += FILE_SZ_WIDTH
                        path_len = int(msg[idx:idx + PATH_LEN_WIDTH], 16)
                        idx += PATH_LEN_WIDTH
                        sav_path = STORE_PATH + ftt.usr_id + \
                            msg[idx:idx + path_len]

                        if os.path.exists(sav_path):
                            aesPipeOUT = self.pipe_info[reader]['aesPipeOUT']
                            self.clientShowMsg(
                                'Upload: The file you want to upload has exist.', aesPipeOUT)
                            continue

                        result = self.usr_manager.addUsedSpace(
                            ftt.usr_id, ftt.usr_pwd, file_sz)
                        if result == -3:
                            self.clientShowMsg(
                                f'Upload: {result}', aesPipeOUT)
                            continue
                        usr_pwd = self.pipe_info[reader]['usrPwd']
                        ack_cmd = ftt.createInTask(
                            task_id, file_sz, sav_path, usr_pwd.encode())
                        aesPipeOUT(ack_cmd)

                    elif cmd == 'Whoami':
                        usr_id = self.pipe_info[reader]['usrId']
                        usr_pwd = self.pipe_info[reader]['usrPwd']
                        if usr_id == None:
                            self.clientShowMsg(
                                f"Whoami: You haven't Login in ", aesPipeOUT)
                            continue
                        total_space = self.usr_manager.getTotalSpace(
                            usr_id, usr_pwd)
                        used_space = self.usr_manager.getUsedSpace(
                            usr_id, usr_pwd)
                        aesPipeOUT = self.pipe_info[reader]['aesPipeOUT']
                        self.clientShowMsg(
                            f'Whoami: "{usr_id}" "{usr_pwd}" {total_space} {used_space}', aesPipeOUT)

                    elif cmd == 'Mkdir':
                        usr_id = self.pipe_info[reader]['usrId']
                        aesPipeOUT = self.pipe_info[reader]['aesPipeOUT']
                        new_dir = STORE_PATH + usr_id + msg[8:]
                        os.mkdir(new_dir)
                        self.clientShowMsg('Mkdir: 0', aesPipeOUT)

                    elif cmd == 'Move':
                        usr_id = self.pipe_info[reader]['usrId']
                        idx = 8
                        sav_path_len = int(msg[idx:idx + PATH_LEN_WIDTH], 16)
                        idx += PATH_LEN_WIDTH
                        sav_path = STORE_PATH + usr_id + \
                            msg[idx:idx + sav_path_len]
                        idx += sav_path_len
                        des_path_len = int(msg[idx:idx + PATH_LEN_WIDTH], 16)
                        idx += PATH_LEN_WIDTH
                        des_path = STORE_PATH + usr_id + \
                            msg[idx:idx + des_path_len]
                        shutil.move(sav_path, des_path)

                    elif cmd == 'Remove':
                        usr_id = self.pipe_info[reader]['usrId']
                        usr_pwd = self.pipe_info[reader]['usrPwd']
                        sav_path = STORE_PATH + usr_id + '\\' + msg[8:]
                        file_sz = os.path.getsize(sav_path)
                        os.remove(sav_path)
                        self.usr_manager.decUsedSpace(
                            usr_id, usr_pwd, file_sz)
                        aesPipeOUT = self.pipe_info[reader]['aesPipeOUT']
                        self.clientShowMsg('Remove: 0', aesPipeOUT)

                    elif cmd == 'List':
                        usr_id = self.pipe_info[reader]['usrId']
                        sav_path = STORE_PATH + usr_id + msg[8:]
                        self.clientShowMsg('ListDir:', aesPipeOUT)
                        for info in os.listdir(sav_path):
                            self.clientShowMsg(f'\t{info}', aesPipeOUT)
                        self.clientShowMsg('ListDir End', aesPipeOUT)

                    elif cmd == 'Search':
                        usr_id = self.pipe_info[reader]['usrId']
                        usr_pwd = self.pipe_info[reader]['usrPwd']
                        idx = 8
                        search_path_len = int(
                            msg[idx:idx + PATH_LEN_WIDTH], 16)
                        idx += PATH_LEN_WIDTH
                        search_path = STORE_PATH + usr_id + \
                            msg[idx:idx + search_path_len]
                        idx += search_path_len
                        pattern_str = msg[idx:]
                        file_path_list = self.getFileList(search_path)
                        pattern_file_list = self.checkpattern(
                            file_path_list, pattern_str.encode(), usr_pwd.encode())
                        self.clientShowMsg('Search:', aesPipeOUT)
                        for path in pattern_file_list:
                            rel_path = path[path.find(
                                usr_id) + len(usr_id) + 1:]
                            self.clientShowMsg(f'\t{rel_path}', aesPipeOUT)
                        self.clientShowMsg('Search End', aesPipeOUT)

                elif self.pipe_info[reader]['type'] == 'FTT pipe':
                    ftt = self.pipe_info[reader]['ftt']
                    if not ftt.inTaskAssigner():
                        print('FTT pipeline closed')
                        self.inputs.remove(ftt.pipe)
                        if ftt.pipe in self.outputs:
                            self.outputs.remove(ftt.pipe)
                        ftt.pipe.close()

            for writer in writable:
                if self.pipe_info[writer]['type'] == 'FTT pipe':
                    ftt = self.pipe_info[writer]['ftt']
                    if not ftt.pending_tasks:
                        #print('remove fft pipe from output[]')
                        self.outputs.remove(writer)
                        continue
                    task_id = random.choice(ftt.pending_tasks)
                    next(ftt.out_tasks[task_id]['out_task'])

            for s in exceptional:
                print('Occured error on', s.getpeername())
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()

    def clientShowMsg(self, msg, aesPipeOUT):
        cmd_data = 'Show'.ljust(8, '@')
        cmd_data += msg
        aesPipeOUT(cmd_data)

    @staticmethod
    def getFileList(path_to_dir):
        file_path_list = []
        path_list = []
        path_list.extend(
            [f'{path_to_dir}\\{file_name}' for file_name in os.listdir(path_to_dir)])
        for path in path_list:
            if os.path.isfile(path):
                file_path_list.append(path)
                continue
            path_list.extend(
                [f'{path}\\{file_name}' for file_name in os.listdir(path)])
        return file_path_list

    def checkpattern(self, file_path_list, pattern, key):
        pattern_file_list = []
        for path in file_path_list:
            with open(path, 'rb') as file:
                data = file.read()
                data = self.encrypt(data, key)
                if pattern in data:
                    pattern_file_list.append(path)
        return pattern_file_list

    @staticmethod
    def encrypt(bytes_input, key):
        bytes_output = []
        idx = 0
        for ch in bytes_input:
            bytes_output.append(ch ^ key[idx])
            idx += 1
            idx %= len(key)
        return bytes(bytes_output)


if __name__ == "__main__":
    server = NetDiskServer()
    server.runServer()
