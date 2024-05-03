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

## References

1. [Real-Time Linux Wiki](https://wiki.linuxfoundation.org/realtime/start)
2. [Checklist for Writing Linux Real-Time Applications](https://www.youtube.com/watch?v=NrjXEaTSyrw)
