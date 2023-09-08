import requests
import time
from plyer import notification
import csv
import os

class WebsiteMonitor:
    def __init__(self):
        self.monitored_websites = {}
        self.interval = 60  # Default monitoring interval in seconds
        self.status_history = {}
        self.notification_rules = {}
        self.load_websites_from_file()

    def add_website(self, name, url, interval=None):
        if interval is None:
            interval = self.interval
        self.monitored_websites[name] = {'url': url, 'interval': interval}
        self.status_history[name] = []
        self.notification_rules[name] = {'notify_on_success': True, 'notify_on_failure': True}
        self.save_websites_to_file()

    def remove_website(self, name):
        if name in self.monitored_websites:
            del self.monitored_websites[name]
            del self.status_history[name]
            del self.notification_rules[name]
            self.save_websites_to_file()
            print(f"The website '{name}' has been removed.")
        else:
            print(f"The website '{name}' is not in the monitoring list.")

    def load_websites_from_file(self):
        if os.path.exists('websites.csv'):
            with open('websites.csv', 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    if len(row) == 3:
                        name, url, interval = row
                        self.add_website(name, url, int(interval))

    def save_websites_to_file(self):
        with open('websites.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for name, data in self.monitored_websites.items():
                csv_writer.writerow([name, data['url'], data['interval']])

    def check_website(self, name, url, interval):
        while True:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    status = f"{name} is reachable."
                    if self.notification_rules[name]['notify_on_success']:
                        notification_title = "Website Monitoring"
                        notification_text = f"{name} is reachable!"
                        notification.notify(
                            title=notification_title,
                            message=notification_text,
                            timeout=10
                        )
                else:
                    status = f"{name} is not reachable. Status code: {response.status_code}"
                    if self.notification_rules[name]['notify_on_failure']:
                        notification_title = "Website Monitoring"
                        notification_text = f"{name} is not reachable (Status code {response.status_code})!"
                        notification.notify(
                            title=notification_title,
                            message=notification_text,
                            timeout=10
                        )
                print(status)
                self.status_history[name].append((time.strftime("%Y-%m-%d %H:%M:%S"), status))
                if len(self.status_history[name]) > 10:
                    self.status_history[name].pop(0)
            except requests.exceptions.MissingSchema:
                status = f"Invalid URL for {name}. Please ensure the URL includes the scheme (e.g., http://)."
                print(status)
                self.status_history[name].append((time.strftime("%Y-%m-%d %H:%M:%S"), status))
            except requests.ConnectionError:
                status = f"{name} is not reachable. No connection."
                if self.notification_rules[name]['notify_on_failure']:
                    notification_title = "Website Monitoring"
                    notification_text = f"{name} is not reachable (No connection)!"
                    notification.notify(
                        title=notification_title,
                        message=notification_text,
                        timeout=10
                    )
                print(status)
                self.status_history[name].append((time.strftime("%Y-%m-%d %H:%M:%S"), status))
                time.sleep(60)  # Wait for 1 minute and retry
                continue
            time.sleep(interval)

    def list_websites(self):
        print("\nMonitored Websites:")
        for name, data in self.monitored_websites.items():
            print(f"{name} - {data['url']} - Interval: {data['interval']} seconds")

    def change_interval(self, name, new_interval):
        if name in self.monitored_websites:
            self.monitored_websites[name]['interval'] = new_interval
            self.save_websites_to_file()
            print(f"The monitoring interval for {name} has been changed to {new_interval} seconds.")
        else:
            print(f"The website '{name}' is not in the monitoring list.")

    def view_status_history(self, name):
        if name in self.status_history:
            print(f"\nStatus History for {name}:")
            for timestamp, status in self.status_history[name]:
                print(f"{timestamp}: {status}")
        else:
            print(f"The website '{name}' is not in the monitoring list.")

    def export_status_history(self, name, filename):
        if name in self.status_history:
            with open(filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Timestamp', 'Status'])
                for timestamp, status in self.status_history[name]:
                    csv_writer.writerow([timestamp, status])
            print(f"The status history for {name} has been exported to '{filename}'.")
        else:
            print(f"The website '{name}' is not in the monitoring list.")

    def import_websites_from_csv(self, filename):
        try:
            with open(filename, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    if len(row) == 3:
                        name, url, interval = row
                        self.add_website(name, url, int(interval))
            print(f"Websites have been imported from '{filename}'.")
        except FileNotFoundError:
            print(f"The file '{filename}' was not found.")

    def clear_status_history(self, name):
        if name in self.status_history:
            self.status_history[name] = []
            print(f"The status history for {name} has been cleared.")
        else:
            print(f"The website '{name}' is not in the monitoring list.")

    def start_monitoring(self):
        for name, data in self.monitored_websites.items():
            print(f"Starting monitoring of {name} ({data['url']}) at an interval of {data['interval']} seconds.")
            self.check_website(name, data['url'], data['interval'])

    def set_notification_rules(self, name, notify_on_success=True, notify_on_failure=True):
        if name in self.notification_rules:
            self.notification_rules[name]['notify_on_success'] = notify_on_success
            self.notification_rules[name]['notify_on_failure'] = notify_on_failure
            print(f"Notification rules for {name} have been updated.")
        else:
            print(f"The website '{name}' is not in the monitoring list.")

def main():
    monitor = WebsiteMonitor()

    while True:
        print("\nWebsite Monitoring - Main Menu")
        print("1. Add Website")
        print("2. Remove Website")
        print("3. Start Monitoring")
        print("4. List Monitored Websites")
        print("5. Change Monitoring Interval")
        print("6. View Status History")
        print("7. Export Status History")
        print("8. Import Websites from CSV")
        print("9. Clear Status History")
        print("10. Set Notification Rules")
        print("11. Exit")
        
        choice = input("Select an option (1/2/3/4/5/6/7/8/9/10/11): ")
        
        if choice == '1':
            name = input("Enter the name of the website: ")
            url = input("Enter the URL of the website (including scheme): ")
            interval = int(input("Enter the monitoring interval in seconds (optional, default: 60 seconds): "))
            monitor.add_website(name, url, interval)
        
        elif choice == '2':
            name = input("Enter the name of the website to remove: ")
            monitor.remove_website(name)
        
        elif choice == '3':
            monitor.start_monitoring()
        
        elif choice == '4':
            monitor.list_websites()
        
        elif choice == '5':
            name = input("Enter the name of the website to change the monitoring interval for: ")
            new_interval = int(input("Enter the new monitoring interval in seconds: "))
            monitor.change_interval(name, new_interval)
        
        elif choice == '6':
            name = input("Enter the name of the website to view its status history: ")
            monitor.view_status_history(name)
        
        elif choice == '7':
            name = input("Enter the name of the website to export its status history: ")
            filename = input("Enter the filename for export (e.g., status.csv): ")
            monitor.export_status_history(name, filename)
        
        elif choice == '8':
            filename = input("Enter the filename of the CSV file to import websites from: ")
            monitor.import_websites_from_csv(filename)
        
        elif choice == '9':
            name = input("Enter the name of the website to clear its status history: ")
            monitor.clear_status_history(name)
        
        elif choice == '10':
            name = input("Enter the name of the website to set notification rules for: ")
            notify_on_success = input("Notify on successful connection? (yes/no): ").lower() == 'yes'
            notify_on_failure = input("Notify on failed connection? (yes/no): ").lower() == 'yes'
            monitor.set_notification_rules(name, notify_on_success, notify_on_failure)
        
        elif choice == '11':
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please select one of the available options.")

if __name__ == "__main__":
    main()
