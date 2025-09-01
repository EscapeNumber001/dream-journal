# Dream Journal Application
![A screenshot of the application homepage](readme_screenshot.png)

## What it is
This is a Django web application designed for a single user to keep a log of their dreams. This application was created due to a dissatisfaction with most available journaling apps: whether that be lack of import/export support, poor search functionality, or questionable privacy, most dream journal apps simply did not meet my needs. This app was designed with the goals of privacy and simplicity in mind. Both exporting and importing of JSON files are supported.

⚠️ **This application should not be run on an Internet-facing server!** It is recommended to use a personal VPN such as [Tailscale](tailscale.com) to securely access your journal from remote networks.

## Running the application
### Dependencies
All of the following packages can be installed below using `pip`:
- Django
- markdown
- markdownify
- bleach

### Execution
```bash
cd <project_dir>
python3 ./manage.py runserver 0.0.0.0:8000
```
*0.0.0.0:8000 can be replaced with any listening IP/port combination.*

## Notes
Although this application supports multiple user accounts for administration and security purposes, it is intended to be treated as a single-user application. The app contains basic access control between accounts, but entry contents are *not* encrypted and can still be viewed by anyone with access to the Django database file or admin page on the server.