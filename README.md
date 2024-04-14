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


TCP Congestion Control
Initialization: cwnd=1, ssthresh=32, max_cwnd=50, una=0, next=1
if( AckIn < una)
{ignore duplicate Ack}
else if (cwnd < ssthresh)
{
//slow start
cwnd = cwnd + 1; //exponential increase
else if (cwnd < max_cwnd)
{
//congestion avoidance
cwnd = cwnd + 1/cwnd ; //linear increase
}
una=AckIn +1;
Timeout and Recovery
If timeout timer expires
Retransmit lost packet
ssthresh= max (cwnd/2, 2)
cwnd=1
enter slow start
Timeout timer = current time + backoff * ( EstimatedRTT + 4*DevRTT+1)
backoff=1 initially then doubles every time timeout timer expires
TCP Tahoe (Fast Retransmit)
3 duplicate Acks means missing packet
if( AckIn < una)
dupack++;
if (dupack==3)
{
dupack=0;
ssthresh =cwnd/2;
cwnd=1;
old_next=next;
next=una;
send the packet;
next=old_next;
}
else {dupack=0;
.......
Reno TCP (Fast recovery)
Retransmit packet
ssthresh=cwnd/2;
cwnd =ssthresh; //enter congestion avoidance
New-Reno TCP
Increment cwnd for each duplicate Ack until a new Ack (Ack with a value higher than the highest seen so
far) exit fast recovery
