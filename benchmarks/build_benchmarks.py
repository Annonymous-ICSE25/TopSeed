import os, argparse
from multiprocessing import Process

cur_path = os.path.abspath(os.getcwd())
num_cores = 50

bmks = [
    # "gawk-5.1.0",
    # "grep-3.6",
    # "diffutils-3.7",
    "patch-2.7.6",
    # "trueprint-5.4",
    # "combine-0.4.0",
    # "coreutils-8.31",
    # "gcal-4.1"
]

bmks_url = {
    'gawk-5.1.0' : 'https://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.gz', 
    'grep-3.6' : 'https://ftp.gnu.org/gnu/grep/grep-3.6.tar.gz', 
    'diffutils-3.7' : 'https://ftp.gnu.org/gnu/diffutils/diffutils-3.7.tar.xz',
    'patch-2.7.6' : 'https://ftp.gnu.org/gnu/patch/patch-2.7.6.tar.gz',
    'trueprint-5.4' : 'https://ftp.gnu.org/gnu/trueprint/trueprint-5.4.tar.gz',
    'combine-0.4.0' : 'https://ftp.gnu.org/gnu/combine/combine-0.4.0.tar.gz',
    'coreutils-8.31' : 'https://ftp.gnu.org/gnu/coreutils/coreutils-8.31.tar.xz',
    'gcal-4.1' : 'https://ftp.gnu.org/gnu/gcal/gcal-4.1.tar.gz'
}

bmks_dir = {
    'gawk-5.1.0' : '',
    'grep-3.6' : 'src',
    'diffutils-3.7' : 'src',
    'patch-2.7.6' : 'src',
    'trueprint-5.4' : 'src',
    'combine-0.4.0' : 'src',
    'coreutils-8.31' : 'src',
    'gcal-4.1' : 'src'
}

def build_gcov(benchmark, dirs, i):
    os.chdir("/".join([cur_path, benchmark]))

    dir_name = f"obj-gcov{i}"
    
    os.mkdir(dir_name)
    os.chdir("/".join([cur_path, benchmark, dir_name]))
    os.system("CFLAGS=\"-g -fprofile-arcs -ftest-coverage -g -O0\" ../configure --disable-nls --disable-largefile --disable-job-server --disable-load")
    os.system("make")
    os.chdir("/".join([cur_path, benchmark]))

def build_each(benchmark):
    # Download a benchmark
    url = bmks_url[benchmark]
    os.system("wget " + url)

    if "tar.xz" in url:
        tar_cmd = "tar -xf " + benchmark + ".tar.xz"
    elif "tar.gz" in url:
        tar_cmd = "tar -zxvf " + benchmark + ".tar.gz"

    os.system(tar_cmd)

    # Build a benchmark
    os.chdir("/".join([cur_path, benchmark]))
    dir_name = "obj-llvm"
    dirs = bmks_dir[benchmark]

    os.mkdir(dir_name)
    os.chdir("/".join([cur_path, benchmark, dir_name]))

    cmd = "CC=wllvm CFLAGS=\"-g -O1 -Xclang -disable-llvm-passes -D__NO_STRING_INLINES -D_FORTIFY_SOURCE=0 -U__OPTIMIZE__\" ../configure --disable-nls --disable-largefile --disable-job-server --disable-load"

    os.system(cmd)
    os.system("make")
    os.system("extract-bc make")
    
    if dirs != "":
        os.chdir(dirs)
    
    cmd2 = "find . -executable -type f | xargs -I \'{}\' extract-bc \'{}\'" 
    os.system(cmd2)    

    procs = []
    for i in range(1, num_cores + 1):
        proc = Process(target=build_gcov, args=(benchmark, dirs, i))
        procs.append(proc)
        proc.start()
    
    for proc in procs:
        proc.join()

    os.chdir(cur_path)
    # for key, value in bmks_url.items():
    file = url.split("/")[-1]
    if os.path.exists(file):
        os.system(f"rm -rf {file}")

def build_all():
    procs = []
    for each in bmks:
        proc = Process(target=build_each, args=(each,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()    
    parser.add_argument("--benchmark", required="", default="every")

    args = parser.parse_args()
    benchmark = args.benchmark

    if benchmark == "every":   
        build_all()
        os.system(f"sh sqlite_builder.sh {num_cores}")
    else:
        if benchmark not in bmks:
            print("===================== Error Occurred! =====================")
            print("The parsed benchmark does not exist in our benchmark suite")
            print("===================== Error Occurred! =====================")
        elif benchmark == "sqlite-3.33.0":
            os.system("sh sqlite_builder.sh")
        else:
            build_each(benchmark)