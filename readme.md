# Dream Journal Application
![A screenshot of the application homepage](readme_screenshot.png)

## What it is
This is a Django web application designed for a single user to keep a log of their dreams. This app was designed with the goals of privacy and simplicity in mind. Has proper multi-user support, and both exporting and importing of JSON files are supported.

⚠️ **This application is not designed to be run on an Internet-facing server!** It is recommended to use a personal VPN such as [Tailscale](https://tailscale.com) to securely access your journal from remote networks.

## Running the application
### Dependencies
All of the following packages can be installed below using `pip`:
- Django
- markdown
- markdownify
- bleach
`pip install django markdown markdownify bleach`

### Execution
```bash
cd <project_dir>
python3 ./manage.py runserver 0.0.0.0:8000
```
*0.0.0.0:8000 can be replaced with any listening IP/port combination.*
