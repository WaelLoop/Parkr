# Parkr
A smart parking project for ConUHacks V

## Database
___
### Connecting to the databases
```
url=database-1.cxcpannskwu9.us-east-2.rds.amazonaws.com
user=parkr
pw=Conu2k19
database=parkr_db
```
From command line, with `psql` installed, you can run 

`psql -U parkr -d parkr_db -h database-1.cxcpannskwu9.us-east-2.rds.amazonaws.com`
### Database schemas
#### parking_spots
____
| Attribute  | Type | Extra 
|---|---|---
| id  | INT | PK
| license | CHAR(6)  | FK to vehicles
|  address |  VARCHAR(255) |
| urban | BOOLEAN |

#### person
____
| Attribute  | Type | Extra 
|---|---|---
| id  | INT | PK
| vehicle | CHAR(6)  | FK to vehicles through license
| gender |  VARCHAR(255)  |
| dob | date |
| insurance_num | INT |
| insurance_provider | INT | FK to insurance id

#### vehicles
____
| Attribute  | Type | Extra 
|---|---|---
| license | CHAR(6) | PK UNIQUE
| type | VARCHAR(128) |
| rental | BOOLEAN |
| model | VARCHAR(128) |
| model_year | INTEGER | 
| private | BOOLEAN | 
| owner | INTEGER | FK to person

#### parking_sessions
____
| Attribute  | Type | Extra 
|---|---|---
| id | INTEGER | SERIAL PK
| license | CHAR(6) | FK to vehicles
| parking_id | INTEGER | FK to parking_spots
| start | datetime |
| end  | datetime | 

#### insurance
____
| Attribute  | Type | Extra 
|---|---|---
| id | INTEGER | PK UNIQUE
| name | VARCHAR(255) |

