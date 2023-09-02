fields_dict = [
    {
        "name": "part",
        "field_type": "String",
        "length": 20,
        "mandatory": True,
        "remarks": "The part number of the serial",
        "naming_conventions": [
            "product_id",
            "Product"
        ]
    },
    {
        "name": "part_des",
        "field_type": "String",
        "length": 64,
        "mandatory": False,
        "remarks": "Test part Description",
        "naming_conventions": [
            "product_name"
        ]
    },
    {
        "name": "serial_number",
        "field_type": "String",
        "length": 8,
        "mandatory": True,
        "remarks": "The serial number",
        "naming_conventions": [
            "sn",
            "SerialNumber"
        ]
    },
    {
        "name": "category",
        "field_type": "String",
        "length": 64,
        "mandatory": False,
        "remarks": "The category of the part",
        "naming_conventions": []
    },
    {
        "name": "vendor",
        "field_type": "String",
        "length": 24,
        "mandatory": True,
        "remarks": "The vendor of the product",
        "naming_conventions": [
            "manufacturer"
        ]
    },
    {
        "name": "test_type",
        "field_type": "String",
        "length": 24,
        "mandatory": True,
        "remarks": "The type of the test",
        "naming_conventions": [
            "TestType"
        ]
    },
    {
        "name": "result_code",
        "field_type": "Int",
        "length": 0,
        "mandatory": True,
        "remarks": "The test result code",
        "naming_conventions": [
            "test_result",
            "TestResult"
        ]
    },
    {
        "name": "result_description",
        "field_type": "String",
        "length": 64,
        "mandatory": False,
        "remarks": "The result description",
        "naming_conventions": [
            "test_result_description",
            "TestResultDesc"
        ]
    },
    {
        "name": "test_date",
        "field_type": "Datetime",
        "length": 0,
        "mandatory": True,
        "remarks": "The date of the test",
        "naming_conventions": [
            "Test Date"
        ]
    },
    {
        "name": "station",
        "field_type": "String",
        "length": 16,
        "mandatory": False,
        "remarks": "",
        "naming_conventions": [
            "station_name"
        ]
    },
    {
        "name": "source_type",
        "field_type": "String",
        "length": 16,
        "mandatory": True,
        "remarks": "The source file path: Json, csv , log etc.",
        "naming_conventions": []
    },
    {
        "name": "source_file",
        "field_type": "String",
        "length": 1000,
        "mandatory": True,
        "remarks": "",
        "naming_conventions": []
    }
]