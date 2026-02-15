import subprocess
import time

def run_step(script_name):
    print(f"\n--- Running {script_name} ---")
    result = subprocess.run(["python", script_name], capture_output=False)
    if result.returncode != 0:
        print(f"❌ {script_name} failed!")
        exit()

if __name__ == "__main__":
    start_time = time.time()
    
    # 1. Get Data (scrape)
    run_step("extract.py")
    
    # 2. Load DB (deduplicate)
    run_step("ingest.py")
    
    # 3. AI Match (calculate vectors)
    run_step("match.py")
    
    # 4. Notify (email)
    run_step("notify.py")

    #5. Create daily plot
    run_step("visualize.py")
    
    print(f"\n✅ All done in {time.time() - start_time:.2f} seconds.")