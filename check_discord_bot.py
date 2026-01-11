#!/usr/bin/env python3
import psutil

def check_discord_bot():
    discord_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'unified_discord_bot' in ' '.join(cmdline):
                discord_processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if discord_processes:
        print('✅ Discord bot is running:')
        for proc in discord_processes:
            print(f'   PID: {proc["pid"]}')
        return True
    else:
        print('❌ Discord bot process not found')
        return False

if __name__ == '__main__':
    check_discord_bot()