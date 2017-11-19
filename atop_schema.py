ATOP_SCHEMA = '''
CPU - CPU utilization
cpu_tot - total number of clock-ticks per second for this machine
processors - number of processors
cpu_sys - consumption for all CPUs in system mode (clock-ticks)
cpu_usr - consumption for all CPUs in user mode (clock-ticks)
cpu_niced - consumption for all CPUs in user mode for niced processes (clock-ticks)
cpu_idle - consumption for all CPUs in idle mode (clock-ticks)
cpu_wait - consumption for all CPUs in wait mode (clock-ticks)
cpu_irq - consumption for all CPUs in irq mode (clock-ticks)
cpu_softirq - consumption for all CPUs in softirq mode (clock-ticks)
cpu_steal - consumption for all CPUs in steal mode (clock-ticks)
cpu_guest - consumption for all CPUs in guest mode (clock-ticks) overlapping user mode
freq - frequency of all CPUs
freq_pct - frequency percentage of all CPUs

CPU_N - CPU utilization per processor (renamed from atop "cpu")
cpu_tot - total number of clock-ticks per second for this machine
proc_n - processor-number
cpu_sys - consumption of this CPUs in system mode (clock-ticks)
cpu_usr - consumption of this CPUs in user mode (clock-ticks)
cpu_niced - consumption of this CPUs in user mode for niced processes (clock-ticks)
cpu_idle - consumption of this CPUs in idle mode (clock-ticks)
cpu_wait - consumption of this CPUs in wait mode (clock-ticks)
cpu_irq - consumption of this CPUs in irq mode (clock-ticks)
cpu_softirq - consumption of this CPUs in softirq mode (clock-ticks)
cpu_steal - consumption of this CPUs in steal mode (clock-ticks)
cpu_guest - consumption of this CPUs in guest mode (clock-ticks) overlapping user mode
freq - frequency of this CPU
freq_prc - frequency percentage of this CPU

CPL - CPU load information
processors - number of processors
load_avg1 - load average for last minute
load_avg5 - load average for last five minutes
load_avg15 - load average for last fifteen minutes
ctx_switches - number of context-switches
interrupts - number of device interrupts.

MEM - memory occupation
page_size - page size for this machine (in bytes)
size_phys - size of physical memory (pages)
size_free - size of free memory (pages)
size_cache - size of page cache (pages)
size_buf - size of buffer cache (pages)
size_slab - size of slab (pages)
size_cache_dirty - dirty pages in cache (pages)
size_slab_recl - reclaimable part of slab (pages),
size_vmware_balloon - total size of vmware's balloon pages (pages)
size_shared_tot - total size of shared memory (pages)
size_shared_res - size of resident shared memory (pages)
size_shared_swp - size of swapped shared memory (pages)
page_size_huge - huge page size (in bytes)
size_huge_tot - total size of huge pages (huge pages)
size_huge_free - size of free huge pages (huge pages)

SWP - swap occupation and overcommit info
page_size - page size for this machine (in bytes)
size_swp - size of swap (pages)
size_free - size of free swap (pages)
NONE - 0 (future use)
size_committed - size of committed space (pages)
committed_limit - limit for committed space (pages)

PAG - paging frequency
page_size - page size for this machine (in bytes)
pg_scans - number of page scans
allocstalls - number of allocstalls
NONE - 0 (future use)
swapins - number of swapins
swapouts - number of swapouts.

LVM - logical volume utilization
name - name
ms_spent - number of milliseconds spent for I/O
reads - number of reads issued
reads_sectors - number of sectors transferred for reads
writes - number of writes issued
writes_sectors - number of sectors transferred for write

MDD - multiple device utilization
name - name
ms_spent - number of milliseconds spent for I/O
reads - number of reads issued
reads_sectors - number of sectors transferred for reads
writes - number of writes issued
writes_sectors - number of sectors transferred for write

DSK - disk utilization
name - name
ms_spent - number of milliseconds spent for I/O
reads - number of reads issued
reads_sectors - number of sectors transferred for reads
writes - number of writes issued
writes_sectors - number of sectors transferred for write

NFM - Network Filesystem (NFS) mount at the client side
name - mounted NFS filesystem
bytes_read - total number of bytes read
bytes_write - total number of bytes written
bytes_r_normal - number of bytes read by normal system calls
bytes_w_normal - number of bytes written by normal system calls
bytes_r_directio - number of bytes read by direct I/O
bytes_w_directio - number of bytes written by direct I/O
pages_read - number of pages read by memory-mapped I/O
pages_write - number of pages written by memory-mapped I/O

NFC - Network Filesystem (NFS) client side counters
rpcs - number of transmitted RPCs
rpcs_read - number of transmitted read RPCs
rpcs_write - number of transmitted write RPCs
rpcs_re - number of RPC retransmissions
auth_re - number of authorization refreshes.

NFS - Network Filesystem (NFS) server side counters
rpcs - number of handled RPCs
rpcs_r - number of received read RPCs
rpcs_w - number of received write RPCs
clientbytes_r - number of bytes read by clients
clientbytes_w - number of bytes written by clients
rpcs_bad_fmt - number of RPCs with bad format
rpcs_bad_auth - number of RPCs with bad authorization
rpcs_bad_client - number of RPCs from bad client
tot_rq - total number of handled network requests
rq_tcp - number of handled network requests via TCP
rq_udp - number of handled network requests via UDP
conn_tcp - number of handled TCP connections
repcache_hits - number of hits on reply cache
repcache_miss - number of misses on reply cache
uncashed_rq - number of uncached requests

NET - network utilization (TCP/IP)
NONE - the verb "upper"
tcp_rcv - number of packets received by TCP
tcp_snt - number of packets transmitted by TCP
udp_rcv - number of packets received by UDP
udp_snt - number of packets transmitted by UDP
ip_rcv - number of packets received by IP
ip_snt - number of packets transmitted by IP
ip_delivered - number of packets delivered to higher layers by IP
op_fwd - number of packets forwarded by IP

NET_IF - network utilization (TCP/IP) per interface (renamed from atop "NET" for per interface)
name - name of the interface
packets_rcv - number of packets received by the interface
bytes_rcv - number of bytes received by the interface
packets_snt - number of packets transmitted by the interface
bytes_snt - number of bytes transmitted by the interface
speed - interface speed
duplex - duplex mode (0=half 1=full)

PRG - per process general information
TID - TID (unique ID of task) (in `man atop` shown as PID)
name - name
state - state
uid_real - real uid
gid_real - real gid
TGID - TGID (group number of related tasks/threads)
threads - total number of threads
exit - exit code
start_epoch - start time (epoch)
cmd - full command line (between brackets)
PPID - PPID
threads_running - number of threads in state 'running' (R)
threads_sleeping - number of threads in state 'interruptible sleeping' (S)
threads_sleeping_d - number of threads in state 'uninterruptible sleeping' (D)
uid_effective - effective uid
gid_effective - effective gid
uid_saved - saved uid
gid_saved - saved gid
uid_fs - filesystem uid
gid_fs - filesystem gid
elapsed - elapsed time (hertz)
is_process - is_process (y/n)
VPID - OpenVZ virtual pid (VPID)
CTID - OpenVZ container id (CTID)
CID - Docker container id (CID)

PRC - per process CPU utilization
TID - TID (unique ID of task) (in `man atop` shown as PID)
name - name
state - state
cpu_tot - total number of clock-ticks per second for this machine
cpu_usr - CPU-consumption in user mode (clockticks)
cpu_sys - CPU-consumption in system mode (clockticks)
nice - nice value
priority - priority
priority_realtime - realtime priority
priority_sched - scheduling policy
CPU - current CPU
sleep_avg - sleep average
TGID - TGID (group number of related tasks/threads)
is_process - is_process (y/n)

PRM - per process memory occupation
TID - TID (unique ID of task) (in `man atop` shown as PID)
name - name
state - state
page_size - page size for this machine (in bytes)
mem_virt_size - virtual memory size (Kbytes)
mem_res_size - resident memory size (Kbytes)
mem_shared_size - shared text memory size (Kbytes)
mem_virt_growth - virtual memory growth (Kbytes)
mem_res_growth - resident memory growth (Kbytes)
pagefaults_minor - number of minor page faults
pagefaults_major - number of major page faults
vlib_exec_size - virtual library exec size (Kbytes)
vlib_data_size - virtual data size (Kbytes)
vlib_stack_size - virtual stack size (Kbytes)
swap - swap space used (Kbytes)
TGID - TGID (group number of related tasks/threads)
is_process - is_process (y/n)
prop_set_size - proportional set size (Kbytes) if in 'R' option is specified

PRD - per process disk utilization
TID - TID (unique ID of task) (in `man atop` shown as PID)
name - name
state - state
obsoleted_kernel_patch - obsoleted kernel patch installed ('n')
standard_io_stat - standard io statistics used ('y' or 'n')
reads - number of reads on disk
reads_sectors_cum - cumulative number of sectors read
writes - number of writes on disk
writes_sectors_cum - cumulative number of sectors written
cncl_sectors - cancelled number of written sectors
TGID - TGID (group number of related tasks/threads)
NONE - (author has no idea, all yield 'n' on this field)
is_process - is_process (y/n)

PRN - per process network utilization
TID - TID (unique ID of task) (in `man atop` shown as PID)
name - name
state - state
netatop - kernel module 'netatop' loaded ('y' or 'n')
tcp_snt - number of TCP-packets transmitted
tcp_snt_cum - cumulative size of TCP-packets transmitted
tcp_rcv - number of TCP-packets received
tcp_rcv_cum - cumulative size of TCP-packets received
udp_snt - number of UDP-packets transmitted
udp_snt_cum - cumulative size of UDP-packets transmitted
udp_rcv - number of UDP-packets received
udp_rcv_cum - cumulative size of UDP-packets transmitted
raw_snt - number of raw packets transmitted (obsolete always 0)
raw_rcv - number of raw packets received (obsolete always 0)
TGID - TGID (group number of related tasks/threads)
is_process - is_process (y/n)
'''
