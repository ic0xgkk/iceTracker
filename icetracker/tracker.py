import psutil
import time
import icetracker


def cmdline_merge(cmdline: list):
    text = ""
    for i in cmdline:
        text += i + " "
    return text


def get_parent_information(process) -> (str, str):
    if process is None:
        return "无", "无"
    pid = process.pid
    name = process.name()
    return str(pid), name


def gen_index():
    # 生成基础时间信息
    Information_time = icetracker.generate_table(
        ["时间戳", "本地时间"],
        [
            [str(time.time()), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
        ]
    )

    # 生成基础CPU信息
    cpu_times = psutil.cpu_times()
    Information_CPU = icetracker.generate_table(
        ["用户用时(s)", "系统用时(s)", "空闲用时(s)", "IO等待用时(s)", "1分钟平均负载",
         "5分钟平均负载", "15分钟平均负载"],
        [
            [cpu_times.user, cpu_times.system, cpu_times.idle, cpu_times.iowait,
             psutil.getloadavg()[0], psutil.getloadavg()[1], psutil.getloadavg()[2]]
        ]
    )

    # 生成基础物理内存信息
    phy_mem = psutil.virtual_memory()
    Information_phymem = icetracker.generate_table(
        ["属性", "Byte", "MByte"],
        [
            ["总计", str(phy_mem.total), str(int(phy_mem.total / 1048576.0))],
            ["实际可用（不含缓存）", str(phy_mem.available), str(int(phy_mem.available / 1048576.0))],
            ["已使用", str(phy_mem.used), str(int(phy_mem.used / 1048576.0))],
            ["Buffer使用", str(phy_mem.buffers), str(int(phy_mem.buffers / 1048576.0))],
            ["Cache使用", str(phy_mem.cached), str(int(phy_mem.cached / 1048576.0))],
            ["共享", str(phy_mem.shared), str(int(phy_mem.shared / 1048576.0))],
            ["空闲（含缓存）", str(phy_mem.free), str(int(phy_mem.free / 1048576.0))]
        ]
    )

    # 生成基础虚拟内存信息
    swap_mem = psutil.swap_memory()
    Information_swmem = icetracker.generate_table(
        ["属性", "Byte", "MByte"],
        [
            ["总计", str(swap_mem.total), str(int(swap_mem.total / 1048576.0))],
            ["已使用", str(swap_mem.used), str(int(swap_mem.used / 1048576.0))],
            ["空闲", str(swap_mem.free), str(int(swap_mem.free / 1048576.0))]
        ]
    )

    text = icetracker.generate_card("时间", Information_time)
    text += icetracker.generate_card("CPU信息", Information_CPU)
    text += icetracker.generate_card("物理内存信息", Information_phymem)
    text += icetracker.generate_card("虚拟内存信息", Information_swmem)

    return icetracker.generate_index(text)


def find_procs_by_name(process_name: str) -> list:
    processList = []
    for p in psutil.process_iter(attrs=['name']):
        if p.info['name'] == process_name:
            processList.append(p)
    return processList


def gen_procs(mon_process_list: list) -> str:
    stack_list = []
    for proc_name in mon_process_list:
        process_list = find_procs_by_name(proc_name)
        for proc_instance in process_list:
            title, content = gen_proc_stack(proc_instance)
            stack_list.append([title, content])
    return icetracker.generate_procs(
        icetracker.generate_stack(stack_list))


def gen_proc_stack(process: psutil.Process):
    # 生成stack标题
    proc_title = "%s - %s" % (process.pid, process.name())

    # 生成stack body
    # 生成进程基础信息
    parent_pid, parent_name = get_parent_information(process)
    Information_Proc_basic = icetracker.generate_table(
        ["属性", "详细"],
        [
            ["创建时间戳", str(process.create_time())],
            ["创建时间(本地)", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(process.create_time()))],
            ["控制台命令", cmdline_merge(process.cmdline())],
            ["父进程PID", parent_pid],
            ["父进程名", parent_name],
            ["所有者", process.username()],
            ["线程数", str(process.num_threads())]
        ]
    )

    # 生成进程CPU信息
    Information_Proc_CPU = icetracker.generate_table(
        ["用户用时(s)", "系统用时(s)", "IO等待用时(s)"],
        [
            [str(process.cpu_times().user),
             str(process.cpu_times().system),
             str(process.cpu_times().iowait)]
        ]
    )

    # 生成进程内存信息
    Information_Proc_mem = icetracker.generate_table(
        ["属性", "Byte", "MByte"],
        [
            ["物理内存使用", str(process.memory_full_info().rss), str(int(process.memory_full_info().rss / 1048576.0))],
            ["整体内存使用", str(process.memory_full_info().vms), str(int(process.memory_full_info().vms / 1048576.0))],
            ["共享内存使用", str(process.memory_full_info().shared),
             str(int(process.memory_full_info().shared / 1048576.0))],
            ["动态链接使用", str(process.memory_full_info().lib), str(int(process.memory_full_info().lib / 1048576.0))],
            ["虚拟内存使用", str(process.memory_full_info().swap), str(int(process.memory_full_info().swap / 1048576.0))]
        ]
    )

    # 生成进程地图
    mem_map = process.memory_maps()
    map_list = []
    for item in mem_map:
        path = item.path
        rss = item.rss
        total = item.size
        swap = item.swap
        map_list.append(
            [path,
             str(rss), str(int(rss/1048576.0)),
             str(total), str(int(total/1048576.0)),
             str(swap), str(int(swap/1048576.0))]
        )
    Information_Proc_map = icetracker.generate_table(
        ["文件名",
         "物理内存使用(Byte)", "物理内存使用(MByte)",
         "总计内存使用(Byte)", "总计内存使用(MByte)",
         "虚拟内存使用(Byte)", "虚拟内存使用(MByte)"],
        map_list
    )

    # 生成进程网络
    conn = process.connections()
    conn_list = []
    for item in conn:
        try:
            conn_type = str(item.type)
        except AttributeError:
            conn_type = "Unknown"

        try:
            local_addr = item.laddr.ip
        except AttributeError:
            local_addr = "Unknown"

        try:
            local_port = str(item.laddr.port)
        except AttributeError:
            local_port = "Unknown"

        try:
            remote_addr = item.raddr.ip
        except AttributeError:
            remote_addr = "Unknown"

        try:
            remote_port = str(item.raddr.port)
        except AttributeError:
            remote_port = "Unknown"

        try:
            status = item.status
        except AttributeError:
            status = "Unknown"

        conn_list.append(
            [conn_type,
             local_addr, local_port,
             remote_addr, remote_port,
             status]
        )
    Information_Proc_conn = icetracker.generate_table(
        ["协议类型", "本地地址", "本地端口", "远程地址", "远程端口", "连接状态"],
        conn_list
    )

    Card_Proc_basic = icetracker.generate_card("基础信息", Information_Proc_basic)
    Card_Proc_CPU = icetracker.generate_card("CPU信息", Information_Proc_CPU)
    Card_Proc_mem = icetracker.generate_card("内存信息", Information_Proc_mem)
    Card_Proc_map = icetracker.generate_card("进程地图", Information_Proc_map)
    Card_Proc_conn = icetracker.generate_card("进程连接", Information_Proc_conn)

    text = Card_Proc_basic + Card_Proc_CPU + Card_Proc_mem + Card_Proc_map + Card_Proc_conn
    return proc_title, text


if __name__ == '__main__':
    pass
