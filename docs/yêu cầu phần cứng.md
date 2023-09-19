# Hardware requirements

From @Xyene:

1. You'll need more hosts for a contest where correct solutions can take several minutes to judge (e.g. IOI (The International Olympiad of Informatics) - style hundreds of test cases).
2. What DMOJ is doing:

- they run dmoj on a baremental host for most of the year:
  6-core (12-thread) AMD Ryzen 5 3600X @ 3.8GHz, with 16 GB 3200 MHz CL16 dual-channel RAM.
- Each judgeruns in a QEMU instance allocated 2GB RAM and 1 physical core (2 threads).
- When they need to run a contest that requireds more judges, they have some scripts to spin some up in the cloud.
- The cloud judges just mount all problem data over NFS (Network File System).
- So, just mount the NFS volume, start docker, and the judge connects.
- If you're planning on running a contest, one thing to keep in mind is that the most load you'll face be at the start of the contest, as everyone rushes to hit the "Join contest" button at the same time. That'll be frontend load more than it will be database load. ton at the same time. That'll be frontend load more than it will be database load. The frontend can render ~ 4 requests/second/core (conservatively, but you should lower bound it at 100ms/req). You can tell how long things take on your setup by reading uwsgi logs.
