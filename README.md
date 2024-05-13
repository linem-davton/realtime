# Real-Time Linux

- clock_res.sh : Measure the resolution of the system clock and monotonic clock
- high_res_timer.c : Shows the current system and monotonic time in resolution of nanoseconds

## Linux Kernel Configuration

[PREEMPT_RT](https://wiki.linuxfoundation.org/realtime/start) patch is applied to the kernel to make it real-time. The following options are enabled in the kernel configuration.

CONFIG_PREEMPT_RT_FULL: Enables the full Preempt-RT patch set, including real-time scheduling and priority inheritance.
CONFIG_HIGH_RES_TIMERS: Enables high-resolution timers for precise timekeeping.
CONFIG_NO_HZ_FULL: Disables the kernel's tick-based timer to reduce latency.
CONFIG_CPUSETS: Allows CPU affinity and isolation for real-time tasks.
CONFIG_IRQ_FORCED_THREADING: Forces interrupt handling to be threaded, improving determinism.
CONFIG_PREEMPT: Enables kernel preemption for better responsiveness.
CONFIG_PREEMPT_VOLUNTARY: Allows voluntary kernel preemption to reduce latency.
CONFIG_LOCKUP_DETECTOR: Detects kernel lockups and panics the system, runs at 99 priority.
CONFIG_DEBUG_* - Expensive debugging options are disabled to reduce overhead.
CONFIG_FTRACE, CONFIG_KPROBES, CONFIG_UPROBES: Tracing options to allow debugging and profiling.

## Checklists

- CPU Affinity
- Real-Time Scheduling - SCHED_FIFO, SCHED_RR
- Avoid Signals like SIGKILL, SIGSTOP

## Measuring Wakeup Latency

```bash
sudo cyclictest -m -t1 -p 90 -i 200 -l 10000
```

-m: Lock all memory to prevent swapping.
-t1: One thread.
-p 90: Set thread priority to 90.
-i 200: Interval of 200 microseconds between wake-ups.
-l 10000: Run 10,000 intervals (loops)

## LinuxPTP

Diable the NTP on the slave nodes. Master node can have NTP enabled.

```bash
timedatectl set-ntp 0
```

Setting one Grand Master and multiple Slave nodes.

```bash
ethtool -T eth0 # check the time stamping capabilities

ptp4l -i eth0 -H -2 # starts with hardware time stamping and ethernet trasnport, on interface eth0
ptp4l -i eth0 -H -2 -s # starts as a slave
```

ptp sync messages are exchanged between the master and slave nodes every second.
To sync the system clock with ptp hardware clock in nic, use the following command.

```bash
phy2sys -a -r # sync system clock to ptp hardware clock
phy2sys -a -r -r # sync ptp hardware clock to system clock
```

### Using SystemD to start LinuxPTP


SystemD services:
- nt2ptp.service
- ptp-master.service
- ptp-slave.service
- phc2sys-master.service
- phc2sys-slave.service

slave-setup.sh : Setups the slave node including setting up the services and dowloading LinuxPTP.

The script creates a file /etc/systemd/system/ptp-slave.service  on slave nodes.

Note - Target is set as network-online.target to make sure the network is up before starting the service and not network.target

Likewise also creates /etc/systemd/system/phc2sys-slave.service on slave node.
When system boots, we first sync time using NTP and then swicth to PTP. ntp2ptp.service is used for this purpose.
- Create file /etc/systemd/system/ntp2ptp.service
- Create file /usr/local/bin/ntp2ptp.sh 
 
Setting up services 

```BASH
sudo systemctl disable ptp-slave.service
sudo systemctl enable ntp2ptp.service
sudo systemctl enable phc2sys-slave.service
```
Note - slave-setup.sh does this automatically.

master-setup.sh : Setups the master node including setting up the services and dowloading LinuxPTP.

### Monitoring the services

```BASH
sudo journalctl -u ptp-slave.service -u phc2sys.service # check the logs
sudo journalctl -u ptp-slave.service -f # follow the logs
sudo journalctl -u ptp-slave.service -b # logs from the boot
```

system_monitor.py : Monitors the system and logs the data to influxdb, and can be visualized using Grafana.
                    Change the configuration variables in the python script.

grafana-dashboard.json : Import this dashboard to Grafana to visualize the data.

## References

1. [Real-Time Linux Wiki](https://wiki.linuxfoundation.org/realtime/start)
2. [Checklist for Writing Linux Real-Time Applications](https://www.youtube.com/watch?v=NrjXEaTSyrw)
