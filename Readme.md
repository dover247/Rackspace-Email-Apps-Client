# Setup
- [1. Configuration](#1-configuration)
- [2. Example Usage](#2-example-usage)

## 1. Configuration

    Create a text file called "config.txt" in the current directory, copy and paste the following contents.

```json
    {
 
        "user_key": "",
        "secret_key": ""

    }
```
    Enter your user and secret keys inbetween quotations and Fire away!

## 2. Example Usage

```python
import emailandapps
emailandapps = emailandapps.EmailandApps('config.txt')
domains = emailandapps.get_domains(['1213514'])
print(domains)
```