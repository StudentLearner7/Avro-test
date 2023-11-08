-- Create the Department table
CREATE TABLE Department (
    department_id serial PRIMARY KEY,
    department_name varchar(255) NOT NULL
);

-- Create the Employee table with a foreign key reference to Department
CREATE TABLE Employee (
    employee_id serial PRIMARY KEY,
    employee_name varchar(255) NOT NULL,
    department_id integer REFERENCES Department(department_id)
);

-- Create the Address table
CREATE TABLE Address (
    address_id serial PRIMARY KEY,
    employee_id integer REFERENCES Employee(employee_id),
    address_line1 varchar(255) NOT NULL,
    address_line2 varchar(255),
    city varchar(255) NOT NULL,
    state varchar(255) NOT NULL,
    postal_code varchar(20) NOT NULL
);

CREATE OR REPLACE FUNCTION UpdateEmployeeNamesToChris() RETURNS void AS $$
BEGIN
    UPDATE Employee
    SET employee_name = 'Chris';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION UpdateEmployeeAndDepartmentNames() RETURNS void AS $$
BEGIN
    UPDATE Employee
    SET employee_name = 'Chris';

    UPDATE Department
    SET department_name = 'Finance';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION UpdateEmployeeDepartmentAndAddress() RETURNS void AS $$
BEGIN
    UPDATE Employee
    SET employee_name = 'Chris';

    UPDATE Department
    SET department_name = 'Finance';

    UPDATE Address
    SET address_line1 = 'New York';
END;
$$ LANGUAGE plpgsql;