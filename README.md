# Parser - NVIDA Senior Data Engineer Home Assignment

## Assumptions

The parser operates with several modes:

1. **Input Flag Only (-i):** The parser writes the results to a JSON file in the temporary output folder on the host.
2. **Input and Output Flags (-i + -o):** The parser writes the results to a JSON file at the specified location.
3. **Update Database Flag (-u):** The parser writes the results to a database file in the output folder.
4. **Config Flag (-c):** The parser uses the requested configuration if it exists (Note: There is no validation on the given config; user discretion is advised).
5. **Append Flag (-a):** The parser appends results to existing files (database/JSON) in the output folder if they exist.

**Additional Considerations:**

- Each item within the given file is parsed using a "Best Effort" strategy, which may result in some loss of information.
- Any other runtime errors will cause an exit status that is not equal to 0 (Error handling is application-dependent).
- The input file should be located on an "on-prem" file system and be known to the host; cloud file systems are not supported.
- When parsing log files, only 'INFO' level lines will be processed.
- When parsing XML files, only the 'product' element at the root will be parsed.

## Building the Parser Application

To build the "parser" image, execute the following Docker commands:

1. Navigate to the project folder:

  `cd <project folder>`

2. Build the "parser" image:

  `docker build -t parser .`


Once the image is created, follow these steps:

1. Create a container named 'my-parser' using the image:

  `docker create --name my-parser parser`


2. Copy the executable from the container to your host:

  * For Unix/Linux systems, copy the 'main.py' file:

    `docker cp my-parser:/app/dist/main ./main`

    You can now run the executable on your host, for example, in the command line interface (CLI):

    `main -i <input file> -o <output folder> -u`

    ! Alternatively you can use docker container as windows PSB


  * For Windows use docker container by the following command:

    `docker run -v <your_inputs_files_dir>:/working_dir parser -i /working_dir/<input_file> -o /working_dir/ -u`
