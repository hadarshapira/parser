# parser
[NVIDA] Senior Data Engineer – Home Assignment

# Build parser application

Run the following docker commands to build the "parser" image:

`cd <project folder>`

`docker build parser .`

Create container:

`docker create --name my-parser parser`

Copy the executable from the container to you host.


* For Unix/Linux systems copy main.py file: 

  `docker cp my-parser:/app/dist/main ../main`

  Add execute permission to main.py `chmod +x ./main.py`

  Now you can run the executable on your host:

  CML for example:

  `main.py -i <input file> -o <output folder>`



* For Windows copy .bat file: `docker cp my-parser:/app/main.bat ..\main.bat`

  Now you can run the executable on your host:

  CML for example:

  `main.bat -i <input file> -o <output folder>`