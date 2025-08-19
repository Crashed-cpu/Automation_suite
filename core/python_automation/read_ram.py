import ctypes
import psutil

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010

def dump_memory(pid, output_file='memory_dump.txt'):
    print(f"[+] Attempting to open process PID {pid}")
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
    if not handle:
        print(f"[!] Failed to open process {pid}. You may need Administrator privileges.")
        return

    with open(output_file, 'w') as out:
        address = 0
        total_dumped = 0
        while address < 0x7FFFFFFF:  # 2GB limit
            buffer = ctypes.create_string_buffer(4096)
            bytes_read = ctypes.c_size_t()
            success = ctypes.windll.kernel32.ReadProcessMemory(handle, ctypes.c_void_p(address), buffer, 4096, ctypes.byref(bytes_read))
            if success and bytes_read.value > 0:
                hex_data = buffer.raw[:bytes_read.value].hex()
                out.write(f'Address {address:#010x}:\n{hex_data}\n\n')
                total_dumped += bytes_read.value
            address += 4096

    ctypes.windll.kernel32.CloseHandle(handle)
    print(f"[✓] Dumped {total_dumped} bytes from PID {pid} to {output_file}")

if __name__ == "__main__":
    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        name = proc.info['name']
        if name and 'notepad' in name.lower():
            print(f"[+] Found target process: {name} (PID {proc.info['pid']})")
            dump_memory(proc.info['pid'])
            found = True
            break
    if not found:
        print("[!] Notepad process not found. Please open Notepad and try again.")
