import os
import subprocess
import psutil
import shutil
import time

class ProcessManager:

    def __init__(self) -> None:
        pass

    #untested may need updating
    def clone(self, process_name: str) -> bool:
        '''
        Clones a process loaded in memory.

        Params: 
        - process_name: Name of the process to clone (string).

        Returns:
        - True if successful, False otherwise.
        '''
        try:
            # find the process by name ;p (untested)
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                if proc.info['name'] == process_name:
                    # Start the process executable
                    if proc.info['exe']:
                        new_process = subprocess.Popen(proc.info['exe'])
                        return new_process is not None
                    else:
                        print(f"Executable path for {process_name} not found.")
                        return False
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    #untested may need updating
    def create(self, process_name: str, runs_forever=False, code_to_run=None) -> bool:
        '''
        Creates a new process that is empty and can either execute code via shellcode
        or do nothing and run forever.

        Params:
        - process_name: Name of the process to create (string).
        - runs_forever: If True, the process will run indefinitely (boolean).
        - code_to_run: Optional shellcode or code to execute (str).

        Returns:
        - True if successful, False otherwise.
        '''
        try:
            if runs_forever:
                # Start a dummy process that runs indefinitely
                new_process = subprocess.Popen(['python', '-c', 'import time; time.sleep(99999)'])
                return new_process is not None

            if code_to_run:
                if isinstance(code_to_run, str):
                    # Execute the provided code
                    new_process = subprocess.Popen(['python', '-c', code_to_run])
                    return new_process is not None

            # If neither runs_forever nor code_to_run is provided, create a dummy process
            if not code_to_run and not runs_forever:
                new_process = subprocess.Popen(['python', '-c', 'print("New process created.")'])
                return new_process is not None

            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    
    def terminate(self, process_name: str) -> bool:
        '''
        Terminates a process by name.

        Params:
        - process_name: Name of the process to terminate (string).

        Returns:
        - True if successful, False otherwise.
        '''
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == process_name:
                    proc.terminate()
                    proc.wait()  # Wait for the process to be terminated
                    return True
            print(f"Process {process_name} not found.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False


