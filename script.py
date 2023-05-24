import subprocess
import os

KB = 1024

SIZES = [8, 16, 32, 64, 128, 256, 512, KB, 2*KB, 4*KB, 8*KB, 16*KB, 24*KB, 32*KB, 40*KB, 48*KB, 56*KB, 63*KB]

def run_compression(compression_enabled, with_high_entropy = False):
    rcv_cmds = ["../zenoh/target/release/examples/z_sub_thr", "-m", "peer", "--no-multicast-scouting", "-l", "tcp/127.0.0.1:7447", "-n", "10000", "-s", "1000"]
    if compression_enabled:
        rcv_cmds.insert(3, "-c")
        rcv_cmds.insert(4, "compression_enabled.json5")
    for size in SIZES:
        send_cmds = ["../zenoh/target/release/examples/z_pub_thr", str(size), "-m", "peer", "--no-multicast-scouting", "-e", "tcp/127.0.0.1:7447"]
        if compression_enabled:
            send_cmds.insert(4, "-c")
            send_cmds.insert(5, "compression_enabled.json5")
            
            if (with_high_entropy):
                send_cmds.insert(6, "--high-entropy")
        

        path = "output_64"
        if compression_enabled:
            path += "/compression_enabled"
            if with_high_entropy:
                path += "/high_entropy"
            else:
                path += "/low_entropy"
        else:
            path += "/compression_disabled"


        compression_logs_path = path + "/compression_logs"
        if not os.path.isdir(compression_logs_path):
            os.makedirs(compression_logs_path)

        batch_sizes_path = path + "/batch_sizes"
        if not os.path.isdir(batch_sizes_path):
            os.makedirs(batch_sizes_path)

        log_file = compression_logs_path + "/compression_" + str(size) + ".txt"
        batch_size_file = batch_sizes_path + "/batch_size_" + str(size) + ".txt"
        
        f1 = open(log_file, "w")
        f2 = open(batch_size_file, "w")

        print("Starting size " + str(size))
        print("Publisher:  " + " ".join(send_cmds))
        print("Received:  " + " ".join(rcv_cmds))

        receiver = subprocess.Popen(rcv_cmds, stdout=f1)
        sender = subprocess.Popen(send_cmds, stdout=f2)
        receiver.wait()
        sender.terminate()


run_compression(True, False)
run_compression(True, True)
run_compression(False)
