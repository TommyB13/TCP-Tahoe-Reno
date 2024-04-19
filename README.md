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

# How to run the code

If you are trying to run tahoe with separated receiver and sender, you will want to look in the tahoe-final/ directory.
In here, run the following commands:
```
python3 tahoe_receiver_only.py

and in another window:

python3 tahoe_sender_only.py ../inputs/lorem_ipsum.txt
```

lorem_ipsum.txt is a file that contains the text of the lorem ipsum. You can replace this with any file you want to send. This one in particular is 5kb. The sender will send this file to the receiver and once the receiver gets all of the packets, it will write the file to a new file called "output.html". You will find that the text is the same as the original file, demonstrating that TCP did its job of maintaining integrity of the data.

If you are trying to run reno with separated receiver and sender, you will want to look in the reno-final/ directory.

In here, run the following commands:
```
python3 reno_receiver_only.py

and in another window:

python3 reno_sender_only.py ../inputs/lorem_ipsum.txt
```

There are additional .sh files that run the sender and receiver together. These are the run_tahoe.sh and run_reno.sh files. You can run these by running the following commands:
```

./run_tahoe.sh
or
./run_reno.sh
```

These will run the sender and receiver together in the same window. The sender will send the file to the receiver and the receiver will write the file to a new file called "output.html". You will find that the text is the same as the original file, demonstrating that TCP did its job of maintaining integrity of the data.

# Performance Metrics

The performance metrics that we are using are throughput and goodput. Throughput is defined as the number of packets per second. Goodput is an indication of network utilization. It can be defined as the number of "good" packets to the total number of packets including retransmitted packets.

# Comparison of Tahoe and Reno

Tahoe and Reno are two different implementations of TCP. Tahoe is the older version of TCP and Reno is the newer version. Reno is an improvement over Tahoe. Reno has a faster recovery time and this is demonstrated through our data collection and graphs in our report.
