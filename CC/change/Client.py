import socket
import time
import select
import random

from FileTransferTasks import FileTransferTasks, PATH_LEN_WIDTH, FILE_SZ_WIDTH
from NetDiskConfig import HOST, PORT
from KeyAgreement import keyAgreementClient, recvNewAesKey
from StdinHandler import getSdtinSock, getStdinReader


class NetDiskClient():
    def __init__(self, ip_addr):
        # get the stdin stream input
        self.stdin_sock = getSdtinSock()
        self.stdinReader = getStdinReader(self.stdin_sock)

        # Connect
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip_addr, PORT))
        print('Connect to the Server')
        self.inputs = []
        self.outputs = []

        self.inputs.append(self.client)
        self.inputs.append(self.stdin_sock)

        # SECTION setup CMD pipe and FTT pipe
        self.aesPipeIN, self.aesPipeOUT = keyAgreementClient(self.client)
        aes_key = recvNewAesKey(self.aesPipeIN)
        self.ftt = FileTransferTasks()
        self.ftt.channelConnect(ip_addr, aes_key)

        self.inputs.append(self.ftt.pipe)
        # !SECTION

        '''
        # SECTION behaviour test
        # test entrypoint
        self.__test_downloadFile()
        # !SECTION
        '''

        self.client.setblocking(False)
        self.ftt.pipe.setblocking(False)

    def __del__(self):
        self.ftt.pipe.close()
        self.client.close()

    def connServer(self):
        while True:
            readable, writable, exceptional = select.select(
                self.inputs, self.outputs, self.inputs)

            for reader in readable:
                if reader == self.stdin_sock:
                    self.stdinInputProcedure()

                if reader == self.client:
                    msg = self.aesPipeIN()
                    # if msg == '', so the server is closed
                    if msg == '':
                        print('Server Closing')
                        '''
                        self.inputs.remove(reader)
                        if reader in self.outputs:
                            self.outputs.remove(reader)
                        reader.close()
                        '''
                        return
                    cmd = msg[:8].strip('@')

                    if cmd == 'FileOut':  # means Download in here
                        print('got fileout cmd')
                        idx = 8
                        task_id = msg[idx:idx + 32]
                        idx += 32
                        file_sz = int(msg[idx:idx + FILE_SZ_WIDTH], 16)
                        idx += FILE_SZ_WIDTH
                        path_len = int(msg[idx:idx + PATH_LEN_WIDTH], 16)
                        idx += PATH_LEN_WIDTH
                        sav_path = msg[idx:idx + path_len]

                        ack_cmd = self.ftt.createInTask(
                            task_id, file_sz, sav_path)
                        self.aesPipeOUT(ack_cmd)

                    elif cmd == 'FileIn':
                        ack_cmd = msg
                        self.ftt.awakeOutTask(ack_cmd[8:8 + 32])
                        self.outputs.append(self.ftt.pipe)

                    elif cmd == 'Show':
                        print(msg[8:])

                elif reader == self.ftt.pipe:
                    self.ftt.inTaskAssigner()

            for writer in writable:
                if writer == self.ftt.pipe:
                    if not self.ftt.pending_tasks:
                        #print('remove fft pipe from output[]')
                        self.outputs.remove(self.ftt.pipe)
                        continue
                    task_id = random.choice(self.ftt.pending_tasks)
                    next(self.ftt.out_tasks[task_id]['out_task'])

    def __pauseDownload(self, task_id):
        # arg: id
        cmd_data = 'Pause'.ljust(8, '@')
        cmd_data += task_id
        self.aesPipeOUT(cmd_data)

    def __continueDownload(self, task_id):
        # arg: id
        cmd_data = 'Continue'.ljust(8, '@')
        cmd_data += task_id
        self.aesPipeOUT(cmd_data)

    def __pauseUpload(self, task_id):
        # arg: id
        self.ftt.pending_tasks.remove(task_id)

    def __continueUpload(self, task_id):
        # that not safe only for test
        # arg: id
        self.ftt.awakeOutTask(task_id)
        if self.ftt.pipe not in self.outputs:
            self.outputs.append(self.ftt.pipe)

    def __uploadFile(self, sav_path, des_path):
        # arg: sav_path, des_path
        # SECTION test arg
        # sav_path = 'C:\\Folder\\WorkSpace\\Program etc\\Python etc\\Python3 etc\\NetDisk\\Song.wav'
        # des_path = '.\\SongT-upload.wav'
        # !SECTION

        req_cmd = self.ftt.createOutTask(
            sav_path, des_path)
        self.aesPipeOUT(req_cmd)

    def __downloadFile(self, sav_path, des_path):
        # arg: sav_path, des_path
        # SECTION test arg
        # sav_path = 'C:\\Folder\\WorkSpace\\Program etc\\Python etc\\Python3 etc\\NetDisk\\Song.wav'
        # des_path = '.\\SongT-download.wav'
        # !SECTION

        req_cmd = 'Download'.ljust(8, '@')
        req_cmd += hex(len(sav_path))[2:].rjust(PATH_LEN_WIDTH, '0')
        req_cmd += sav_path
        req_cmd += hex(len(des_path))[2:].rjust(PATH_LEN_WIDTH, '0')
        req_cmd += des_path

        self.aesPipeOUT(req_cmd)

    def stdinInputProcedure(self):
        cmd_list = self.stdinReader()
        if cmd_list == False:
            print('Bad input')
            return
        if cmd_list == []:
            return
        cmd = cmd_list[0]
        if cmd == 'Upload':
            # 'Upload $UploadFilePath $DesFilePath'
            upload_file_path = cmd_list[1]
            des_file_path = cmd_list[2]
            self.__uploadFile(upload_file_path, des_file_path)

        elif cmd == 'Download':
            # 'Download $DownloadFilePath $DesFilePath'
            download_file_path = cmd_list[1]
            des_file_path = cmd_list[2]
            self.__downloadFile(download_file_path, des_file_path)

        elif cmd == 'PauseUpload':
            # 'PauseUpload $TaskId'
            task_id = cmd_list[1]
            self.__pauseUpload(task_id)

        elif cmd == 'PauseDownload':
            # 'PauseDownload $TaskId'
            task_id = cmd_list[1]
            self.__pauseDownload(task_id)

        elif cmd == 'ContinueUpload':
            # 'PauseUpload $TaskId'
            task_id = cmd_list[1]
            self.__continueUpload(task_id)

        elif cmd == 'ContinueDownload':
            # 'PauseUpload $TaskId'
            task_id = cmd_list[1]
            self.__continueDownload(task_id)

        elif cmd == 'ShowRunningTaskList':
            # 'ShowRunningTaskList'
            print('RunningTaskList:')
            for task_id in self.ftt.in_tasks:
                file_name = self.ftt.in_tasks[task_id]['path'].split('\\')[-1]
                file_sz = self.ftt.in_tasks[task_id]['file_sz']
                progress = self.ftt.in_tasks[task_id]['progress']
                progress /= file_sz
                progress_percent = progress * 100
                print(
                    f'DOWNLOAD\t{file_name}\t{progress_percent:.2f}%\t{task_id}')
            for task_id in self.ftt.out_tasks:
                file_name = self.ftt.out_tasks[task_id]['path'].split('\\')[-1]
                file_sz = self.ftt.out_tasks[task_id]['file_sz']
                progress = self.ftt.out_tasks[task_id]['progress']
                progress /= file_sz
                progress_percent = progress * 100
                print(
                    f'UPLOAD\t\t{file_name}\t{progress_percent:.2f}%\t{task_id}')

        elif cmd == 'ShowDoneTaskList':
            # ShowDoneTaskList
            print('DoneTaskList:')
            for task_id in self.ftt.done_in_tasks:
                file_name = self.ftt.done_in_tasks[task_id]['path'].split(
                    '\\')[-1]
                file_sz = self.ftt.done_in_tasks[task_id]['file_sz']
                print(
                    f'DOWNLOAD\t{file_name}\t{file_sz}B\t{task_id}')
            for task_id in self.ftt.done_out_tasks:
                file_name = self.ftt.done_out_tasks[task_id]['path'].split(
                    '\\')[-1]
                file_sz = self.ftt.done_out_tasks[task_id]['file_sz']
                print(
                    f'UPLOAD\t{file_name}\t{file_sz}B\t{task_id}')

        elif cmd == 'Login':
            # Login $UsrID $UsrPwd
            if len(cmd_list) != 3:
                print('Bad input')
                return
            cmd_data = 'Login'.ljust(8, '@')
            cmd_data += cmd_list[1].ljust(32, '\0')[:32]
            cmd_data += cmd_list[2].ljust(32, '\0')[:32]
            self.aesPipeOUT(cmd_data)

        elif cmd == 'Register':
            # Register $UsrID $UsrPwd
            if len(cmd_list) != 3:
                print('Bad input')
                return
            cmd_data = 'Register'.ljust(8, '@')
            cmd_data += cmd_list[1].ljust(32, '\0')[:32]
            cmd_data += cmd_list[2].ljust(32, '\0')[:32]
            self.aesPipeOUT(cmd_data)

        elif cmd == 'ChangePassword':
            # ChangePassword $UsrID $UsrOldPwd $UsrNewPwd
            if len(cmd_list) != 4:
                print('Bad input')
                return
            cmd_data = 'ChanPwd'.ljust(8, '@')
            cmd_data += cmd_list[1].ljust(32, '\0')[:32]
            cmd_data += cmd_list[2].ljust(32, '\0')[:32]
            cmd_data += cmd_list[3].ljust(32, '\0')[:32]
            self.aesPipeOUT(cmd_data)

        elif cmd == 'Whoami':
            # Whoami
            cmd_data = 'Whoami'.ljust(8, '@')
            self.aesPipeOUT(cmd_data)

        elif cmd == 'Mkdir':
            # Mkdir $PathToDir
            cmd_data = 'Mkdir'.ljust(8, '@')
            cmd_data += cmd_list[1]
            self.aesPipeOUT(cmd_data)

        elif cmd == 'Move':
            # Move $SavPath $DesPath
            cmd_data = 'Move'.ljust(8, '@')
            cmd_data += hex(len(cmd_list[1]))[2:].rjust(PATH_LEN_WIDTH, '0')
            cmd_data += cmd_list[1]
            cmd_data += hex(len(cmd_list[2]))[2:].rjust(PATH_LEN_WIDTH, '0')
            cmd_data += cmd_list[2]
            self.aesPipeOUT(cmd_data)

        elif cmd == 'Remove':
            # Remove $SavPath
            cmd_data = 'Remove'.ljust(8, '@')
            cmd_data += cmd_list[1]
            self.aesPipeOUT(cmd_data)

        elif cmd == 'List':
            # List $Dir
            cmd_data = 'List'.ljust(8, '@')
            cmd_data += cmd_list[1]
            self.aesPipeOUT(cmd_data)

        elif cmd == 'SearchPatternInFiles':
            # SearchPatternInFiles $SearchPath $PatternStr
            cmd_data = 'Search'.ljust(8, '@')
            cmd_data += hex(len(cmd_list[1]))[2:].rjust(PATH_LEN_WIDTH, '0')
            cmd_data += cmd_list[1]
            cmd_data += cmd_list[2]
            self.aesPipeOUT(cmd_data)


if __name__ == "__main__":
    client = NetDiskClient(HOST)
    client.connServer()
