import subprocess

KB = 1024

SIZES = [8, 16, 32, 64, 128, 256, 512, KB, 2*KB, 4*KB, 8*KB, 16*KB, 24*KB, 32*KB, 40*KB, 48*KB, 56*KB, 64*KB]

def run_compression():
    rcv_cmds = ["./target/release/examples/z_sub_thr", "-m", "peer", "--no-multicast-scouting", "-l", "tcp/127.0.0.1:7447", "-n", "10000", "-s", "1000"]
    for size in SIZES:
        send_cmds = ["./target/release/examples/z_pub_thr", str(size), "-m", "peer", "-c", "test.json5", "--no-multicast-scouting", "--high-entropy", "-e", "tcp/127.0.0.1:7447"]
        log_file = "compression_logs/compression_" + str(size) + ".txt"
        batch_size_file = "batch_sizes/batch_size_" + str(size) + ".txt"
        f1 = open(log_file, "w")
        f2 = open(batch_size_file, "w")
        receiver = subprocess.Popen(rcv_cmds, stdout=f1)
        sender = subprocess.Popen(send_cmds, stdout=f2)
        receiver.wait()
        sender.terminate()

run_compression()
