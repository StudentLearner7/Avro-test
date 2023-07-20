-- Table: Department
CREATE TABLE department (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Table: Employee
CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    department_id INTEGER NOT NULL REFERENCES department(id) ON DELETE CASCADE
);
