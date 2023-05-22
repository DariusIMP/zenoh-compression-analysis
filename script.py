import subprocess

KB = 1024

SIZES = [8, 16, 32, 64, 128, 256, 512, KB, 2*KB, 4*KB, 8*KB, 16*KB, 24*KB, 32*KB, 40*KB, 48*KB, 56*KB, 64*KB]

def run_compression():
    rcv_cmds = ["./target/release/examples/z_sub_thr", "-m", "peer", "--no-multicast-scouting", "-l", "tcp/127.0.0.1:7447", "-n", "10000", "-s", "1000"]
    for size in SIZES:
        send_cmds = ["./target/release/examples/z_pub_thr", str(size), "-m", "peer", "--no-multicast-scouting", "-e", "tcp/127.0.0.1:7447"]
        log_file = "compression_logs/compression_" + str(size) + ".txt"
        f = open(log_file, "w")
        sender = subprocess.Popen(send_cmds)
        receiver = subprocess.Popen(rcv_cmds, stdout=f)
        receiver.wait()
        sender.terminate()

run_compression()
