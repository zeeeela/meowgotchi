import sys
import subprocess

from meowgotchi.app import main
def main():
    #auto-start Ollama
    try:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("Ollama not found. Please install it or run 'ollama serve' manually.")
        sys.exit(1)
    
    from meowgotchi.app import main as app_main
    app_main()

    
if __name__ == "__main__":
    main()
