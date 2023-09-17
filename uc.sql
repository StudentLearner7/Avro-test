CREATE TABLE Org (
    org_id SERIAL PRIMARY KEY,
    org_name VARCHAR(255) NOT NULL
);

-- Create the Department table with a foreign key to Org
CREATE TABLE Department (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(255) NOT NULL,
    org_id INT REFERENCES Org(org_id)
);

-- Create the Employees table with a foreign key to Department
CREATE TABLE Employees (
    emp_id SERIAL PRIMARY KEY,
    emp_name VARCHAR(255) NOT NULL,
    dept_id INT REFERENCES Department(dept_id)
);

-- Create the Address table with a foreign key to Employees (one-to-one)
CREATE TABLE Address (
    addr_id SERIAL PRIMARY KEY,
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    emp_id INT UNIQUE REFERENCES Employees(emp_id)
);

-- Create the Projects table
CREATE TABLE Projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL
);

-- Create the EmployeesProjects junction table (many-to-many)
CREATE TABLE EmployeesProjects (
    emp_id INT REFERENCES Employees(emp_id),
    project_id INT REFERENCES Projects(project_id),
    PRIMARY KEY (emp_id, project_id)
);