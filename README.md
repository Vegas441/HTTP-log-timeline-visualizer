# HTTP Log timeline Visualizer

Task:
Develop a web application, which will fetch log data, group requests and responses by ip and port, visualize them on timelines and order them by date and time.

# Authors

David Svatý
Lukáš Kaprál

## Usage

```
$ Run web application by typing python3 manage.py runserver.
$ Upload file containing log using file upload/Upload link to jenkins server using Generate from URL.
$ Filter requests and reponses by using dateTime filtration on the right.
$ Click on timeline ip to view all requests and reponses with more details.
$ Click on specific request/response dot to view all details about it.
$ Click on specific request/response dateTime to get a tooltip containing details about it.
$ Upload new file/link to generate new timeline.
$ Click on Delete log to clear database.
```
