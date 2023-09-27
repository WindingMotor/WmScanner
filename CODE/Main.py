import threading
import UI 
from Scanner import Scanner 


ui = UI.App()
scanner = Scanner()

def start_scanner():
    scanner.run()
    

# Create a thread for the scanner and start it
scanner_thread = threading.Thread(target=start_scanner)
scanner_thread.daemon = True
scanner_thread.start()

# Start the UI
ui.mainloop()
