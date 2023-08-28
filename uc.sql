-- Create sequence for id columns
CREATE SEQUENCE org_id_seq;
CREATE SEQUENCE dept_id_seq;
CREATE SEQUENCE emp_id_seq;
CREATE SEQUENCE addr_id_seq;

-- Create sequence for cid in Org table
CREATE SEQUENCE org_cid_seq;

-- Create Org table
CREATE TABLE Org (
    id INTEGER DEFAULT nextval('org_id_seq') PRIMARY KEY,
    cid INTEGER DEFAULT nextval('org_cid_seq'),
    org_name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    CONSTRAINT unique_cid UNIQUE (cid)
);

-- Create Department table
CREATE TABLE Department (
    id INTEGER DEFAULT nextval('dept_id_seq') PRIMARY KEY,
    org_id INTEGER REFERENCES Org (id),
    cid INTEGER REFERENCES Org (cid),
    department_name VARCHAR(255) NOT NULL
);

-- Create Employee table
CREATE TABLE Employee (
    id INTEGER DEFAULT nextval('emp_id_seq') PRIMARY KEY,
    org_id INTEGER REFERENCES Org (id),
    cid INTEGER REFERENCES Org (cid),
    department_id INTEGER REFERENCES Department (id),
    employee_name VARCHAR(255) NOT NULL,
    position VARCHAR(255)
);

-- Create Address table
CREATE TABLE Address (
    id INTEGER DEFAULT nextval('addr_id_seq') PRIMARY KEY,
    org_id INTEGER REFERENCES Org (id),
    cid INTEGER REFERENCES Org (cid),
    employee_id INTEGER REFERENCES Employee (id) UNIQUE,
    street VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    postal_code VARCHAR(20)
);
