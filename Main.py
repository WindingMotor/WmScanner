import threading
import UI  # Import your UI class
from Scanner import Scanner  # Import your Scanner class

# Create an instance of the UI class
ui = UI.App()

# Create an instance of the Scanner class
scanner = Scanner()

# Create a function to start the scanner as a separate thread
def start_scanner():
    scanner.run()

# Create a thread for the scanner and start it
scanner_thread = threading.Thread(target=start_scanner)
scanner_thread.daemon = True
scanner_thread.start()

# Start the UI application
ui.mainloop()
