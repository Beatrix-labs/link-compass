#!/usr/bin/env python3
import argparse
import sys
import time
import config

def print_banner():
    print(f"{config.INFO}")
    print("==================================================")
    print(f"   {config.NAME} {config.VERSION}")
    print(f"   Developed by {config.AUTHOR}")
    print("==================================================")
    print(f"{config.RESET}")

def main():
    parser = argparse.ArgumentParser(
        description=f"{config.NAME} - Lightweight Subdomain and Link Discovery Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("-d", "--domain", help="Target domain (e.g., example.com)", required=True)
    parser.add_argument("-s", "--status", help="Enable HTTP status code checking (200, 403, 404)", action="store_true")
    parser.add_argument("-o", "--output", help="Output file to save the results")
    parser.add_argument("-t", "--threads", help=f"Number of concurrent threads (Default: {config.MAX_THREADS})", type=int, default=config.MAX_THREADS)

    if len(sys.argv) == 1:
        parser.print_help(sys.argv[0])
        sys.exit(1)

    args = parser.parse_args()

    print_banner()

    print(f"{config.INFO}[*] Target Domain : {args.domain}{config.RESET}")
    print(f"{config.INFO}[*] Threads       : {args.threads}{config.RESET}")
    
    if args.status:
        print(f"{config.INFO}[*] Mode          : Advanced{config.RESET}")
    else:
        print(f"{config.INFO}[*] Mode          : Base Scan (Discovery Only){config.RESET}")

    if args.output:
        print(f"{config.INFO}[*] Output File   : {args.output}{config.RESET}")

    print(f"{config.INFO}--------------------------------------------------{config.RESET}")

    start_time = time.time()

    try:
        print(f"{config.INFO}[*] Initializing scan engine...{config.RESET}")
        
        import core.scanner as engine
        import modules.status_checker as checker
        import utils.reporter as reporter

        active_links = engine.run_base_scan(args.domain, args.threads)
        
        advanced_data = None 
        
        if args.status and active_links:
            advanced_data = checker.run(active_links, args.threads)
            
        if args.output and active_links:
            print(f"{config.INFO}[*] Generating report file...{config.RESET}")
            reporter.save_to_file(args.output, args.domain, active_links, advanced_data)

        print(f"{config.SUCCESS}[+] Scan completed successfully.{config.RESET}")
    except KeyboardInterrupt:
        print(f"\n{config.ERROR}[-] Scan interrupted by user (Ctrl+C). Exiting safely...{config.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{config.ERROR}[-] An unexpected error occurred: {e}{config.RESET}")
        sys.exit(1)
        
    elapsed_time = time.time() - start_time
    print(f"{config.INFO}--------------------------------------------------{config.RESET}")
    print(f"{config.INFO}[*] Total execution time: {elapsed_time:.2f} seconds{config.RESET}")

if __name__ == "__main__":
    main()
