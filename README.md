# Magentrack test

### Installation

Requires docker (https://www.docker.com/get-started), run:

```sh
docker-compose build
docker-compose up
```

### Endpoints
| Description | Endpoint |
| ------ | ------ |
| Admin: 
username: ```admin``` password: ```admin``` | [/admin][Admin] |
| Datasets | [/api/v1/datasets?page=\<page\>][Data] |
| Row | [/api/v1/rows/?dataset_id=<dataset_id>&name=<client_name>&point=<Point(Longitude,Latitude)>][Row] |
| Log | [/log][Log] |


   [Admin]: <http://localhost:8000/admin/>
   [Data]: <http://localhost:8000/api/v1/datasets/>
   [Row]: <http://localhost:8000/api/v1/rows/>
   [Log]: <http://localhost:8000/log/>
