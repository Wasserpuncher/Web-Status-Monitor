# Website Monitoring Tool

This is a Python program for monitoring websites and notifying you of their status changes. It allows you to add websites to a monitoring list, check their availability at specified intervals, and view the status history. Notifications are sent when a website becomes reachable or unreachable.

## Features

- Add and remove websites to/from the monitoring list.
- Set custom monitoring intervals for each website.
- Receive notifications on successful or failed connections.
- View status history for monitored websites.
- Export status history to a CSV file.
- Import websites from a CSV file.
- Clear status history for specific websites.
- Start and stop monitoring for all websites.

## Usage

1. Clone this repository to your local machine.

2. Install the required Python packages using pip:

"pip install requests plyer"


3. Run the program:


python WebsiteMonitor.py


4. Follow the on-screen instructions to perform various actions such as adding websites, starting monitoring, and more.

## Configuration

You can configure the default monitoring interval in the `WebsiteMonitor.py` file by modifying the `self.interval` variable.

## Dependencies

- [Requests](https://pypi.org/project/requests/): HTTP library for sending HTTP requests.
- [Plyer](https://pypi.org/project/plyer/): Cross-platform Python library for accessing features commonly found on various operating systems.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


