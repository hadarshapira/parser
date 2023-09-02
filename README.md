# parser
[NVIDA] Senior Data Engineer – Home Assignment

# Assumptions

* Main executable can run in several mods:
  * Given Input flag only (-i): will write parser result to json file at temp output folder on the host
  * Given Input + Output flags (-i + -o): will write parser result to json file at the wanted location
  * Given Update_DB flag (-u): will write parser result to db file at the output folder
  * Given Config flag (-c): will use requested config if exists (There is no validation on the given config - user concoren)
  * Given Append flag (-a): will append results to existing files (db / json) at the output folder if it exists
* Each item within the given file will be parsed in "Best Effort" strategy - Can cause lost of information
* Any other runtime error will cause exit status != 0 (The error handling depend on the running application)
* Input file should be "on-prem" file system and known to the host (cloud file systems are not supported)
* In case the Parser working on log files, only 'INFO' level line will be parsed
* In case the Parser working on xml files, only 'product' element in root will be parsed

# Build parser application

Run the following docker commands to build the "parser" image:

`cd <project folder>`

`docker build parser .`

Create container:

`docker create --name my-parser parser`

Copy the executable from the container to you host.


* For Unix/Linux systems copy main.py file: 

  `docker cp my-parser:/app/dist/main ./main`

  Now you can run the executable on your host:

  CML for example:

  `main -i <input file> -o <output folder> -u`

  ! Alternatively you can use docker container as windows PSB


* For Windows use docker container by the following command:

  `docker run -v <your_inputs_files_dir>:/working_dir parser -i /working_dir/<input_file> -o /working_dir/ -u`
