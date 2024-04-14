# TCP-Tahoe-Reno

Objective: Understand the inner workings of two TCP implementations.

Simulate two flavors of TCP (Tahoe and Reno).

To evaluate the performance of each implementation, you need to keep track of some data. (packets sent, packets received,....etc.)

Some examples of performance measures are throughput, goodput, average delay, delay jitter.

Throughput is defined as number of packets per second.

Goodput is an indication of network utilization. It can be defined as the number of "good" packets to the total number of packets including retransmitted packets.

What to turn in:

Your source code for Tahoe TCP and Reno TCP.
A shell script to prove that your code compiles and runs correctly.
A report that includes a comparison of the performance of TCP Tahoe vs. TCP Reno under different packet loss probabilities. Use at least two performance metrics. Graph your results and write your observations.
