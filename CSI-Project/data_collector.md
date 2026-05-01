# CSI Data Collector

The `data_collector.py` script is a tool designed to collect Channel State Information (CSI) data from a UDP stream, process it, and save it into a CSV file for further analysis. This script is particularly useful for applications such as wireless sensing, activity recognition, and other scenarios that require CSI data collection.

---

## Features

- Listens for UDP packets on a specified IP and port.
- Extracts and processes CSI data from incoming packets.
- Computes amplitudes for 64 subcarriers from raw CSI data.
- Saves the processed data into a CSV file with a timestamped filename.
- Allows labeling of data for easy categorization.
- Automatically creates the output directory if it does not exist.
- Provides real-time feedback on the number of packets recorded.

---

## Requirements

- Python 3.x
- A UDP data source that sends CSI data in the expected format.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/CSI-Project.git
   cd CSI-Project
   ```

2. Install any required dependencies (if applicable). This script uses only standard Python libraries, so no additional installation is required.

---

## Usage

1. **Set the Label**:  
   Before running the script, set the `CURRENT_LABEL` variable to a meaningful label that describes the data being collected. For example:
   ```python
   CURRENT_LABEL = "walking"
   ```

2. **Run the Script**:  
   Execute the script using Python:
   ```bash
   python data_collector.py
   ```

3. **Stop the Script**:  
   To stop the recording, press `Ctrl+C`. The script will save all recorded data to the specified CSV file.

---

## Configuration

The following configuration options can be modified in the script:

- **UDP_IP**: The IP address to listen on. Default is `0.0.0.0` (all interfaces).
- **UDP_PORT**: The port to listen on. Default is `5500`.
- **CURRENT_LABEL**: The label for the data being recorded. Update this before starting the script.
- **FILENAME**: The output file path. By default, it saves the file in the `/app/data/` directory with a name format of `<label>_<timestamp>.csv`.

---

## Data Format

The collected data is saved in a CSV file with the following structure:

- **Header**: The first row contains column names:
  ```
  sub_0, sub_1, ..., sub_63, label
  ```
  - `sub_0` to `sub_63`: Amplitude values for 64 subcarriers.
  - `label`: The label assigned to the data (e.g., "walking").

- **Data Rows**: Each subsequent row contains:
  - 64 amplitude values calculated from the CSI data.
  - The label specified in the `CURRENT_LABEL` variable.

---

## Example Output

Example CSV file content:

```
sub_0,sub_1,sub_2,...,sub_63,label
1.23,2.34,3.45,...,4.56,walking
1.12,2.22,3.32,...,4.42,walking
...
```

---

## Notes

1. **Data Directory**: The script saves all CSV files to the `/app/data/` directory. Ensure this directory exists or let the script create it automatically.
2. **Data Format**: The script expects incoming UDP packets to contain CSI data in the format:
   ```
   CSI_DATA [value1,value2,value3,...]
   ```
   where `value1, value2, ...` are integers representing raw CSI data.
3. **Error Handling**: The script includes basic error handling to skip malformed packets.

---

## Troubleshooting

- **No Data Recorded**: Ensure the UDP source is sending data to the correct IP and port specified in the script.
- **Malformed Data**: Verify that the incoming data matches the expected format (`CSI_DATA [value1,value2,...]`).
- **Permission Issues**: Ensure the script has write permissions for the `/app/data/` directory.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss potential changes or improvements.

---

## Contact

For questions or support, please contact [Your Name/Team] at [your-email@example.com].