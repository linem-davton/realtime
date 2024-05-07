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
phy2sys -a -r
```

### Using SystemD to start LinuxPTP

Create a file /etc/systemd/system/ptp4l.service 

```BASH
[Unit]
Description=Precision Time Protocol (PTP) daemon
After=network.target

[Service]
Type=simple
ExecStart=/usr/sbin/ptp4l -i eth0 -H -s -2 # Slave
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

/etc/systemd/system/phc2sys.service 

```BASH
[Unit]
Description=Synchronize system clock to PHC
After=ptp4l.service network.target

[Service]
Type=simple
ExecStart=/usr/sbin/phc2sys -a -r
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enabling and starting the services

```BASH
sudo systemctl daemon-reload
systemctl enable ptp4l.service
systemctl enable phc2sys.service
```

Checking Logs

```BASH
sudo journalctl -u ptp4l.service -u phc2sys.service # check the logs
sudo journalctl -u ptp4l.service -f # follow the logs
sudo journalctl -u ptp4l.service -b # logs from the boot
```

## References

1. [Real-Time Linux Wiki](https://wiki.linuxfoundation.org/realtime/start)
2. [Checklist for Writing Linux Real-Time Applications](https://www.youtube.com/watch?v=NrjXEaTSyrw)
