import cv2
import time
import pandas as pd
from pyzbar.pyzbar import decode

class Scanner:
    def __init__(self):
        # Initialize the attendance data DataFrame or create a new one if it doesn't exist
        try:
            self.attendance_data = pd.read_csv("attendance.csv")
        except FileNotFoundError:
            self.attendance_data = pd.DataFrame(columns=["Date", "First Name", "Last Name", "ID", "Login Time", "Logout Time", "Total Time"])

        # Dictionary to store user login times
        self.user_logins = {}

        # Dictionary to store user logout status
        self.user_logout_status = {}

    def scan_qr_code(self):
        cap = cv2.VideoCapture(3)
        qr_code_data = None

        while True:
            _, frame = cap.read()
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_code_data = obj.data.decode('utf-8')
                break  # Only process the first QR code found
            cv2.imshow("QR Code Scanner", frame)

            if qr_code_data:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return qr_code_data

    def calculate_total_time(self, login_time, logout_time):
        login_timestamp = time.mktime(time.strptime(login_time, "%H:%M:%S"))
        logout_timestamp = time.mktime(time.strptime(logout_time, "%H:%M:%S"))
        total_seconds = logout_timestamp - login_timestamp
        total_time = time.strftime("%H:%M:%S", time.gmtime(total_seconds))
        return total_time

    def log_attendance(self, user_data, login_time, logout_time):
        date = time.strftime("%Y-%m-%d")
        total_time = self.calculate_total_time(login_time, logout_time)
        self.attendance_data = self.attendance_data.append({
            "Date": date,
            "First Name": user_data[0],
            "Last Name": user_data[1],
            "ID": user_data[2],
            "Login Time": login_time,
            "Logout Time": logout_time,
            "Total Time": total_time
        }, ignore_index=True)
        self.attendance_data.to_csv("attendance.csv", index=False)

    def run(self):
        while True:
            print("Scan your QR code to log in or log out.")
            qr_code_data = self.scan_qr_code().split("_")
            if len(qr_code_data) != 3:
                print("Invalid QR code format. Please try again.")
                continue

            user_id = qr_code_data[2]
            timestamp = time.strftime("%H:%M:%S")

            if user_id not in self.user_logins:
                # Log in
                self.user_logins[user_id] = {
                    "name": f"{qr_code_data[0]} {qr_code_data[1]}",
                    "login_time": timestamp
                }
                self.user_logout_status[user_id] = False
                print(f"Logged in as {qr_code_data[0]} {qr_code_data[1]} ({user_id}) at {timestamp}")
            else:
                # Log out
                if not self.user_logout_status[user_id]:
                    self.user_logout_status[user_id] = True
                    print(f"Logged out as {qr_code_data[0]} {qr_code_data[1]} ({user_id}) at {timestamp}")
                    self.log_attendance([qr_code_data[0], qr_code_data[1], user_id], self.user_logins[user_id]["login_time"], timestamp)
                    del self.user_logins[user_id]
                else:
                    print(f"User {qr_code_data[0]} {qr_code_data[1]} ({user_id}) has already logged out.")

            time.sleep(2)

if __name__ == "__main__":
    attendance_system = Scanner()
    attendance_system.run()
