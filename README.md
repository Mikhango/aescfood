# Description
Aescfoodbot - бот, созданный для помощи в осуществлении доставки еды ученикам в школе сунц мгу.
Не хотите забирать заказ с кпп сунца? - Вы можете сделать заказ в этом боте, заплатить чаевые курьеру и получить доставку заказа прямо до комнаты!
t.me/aescfoodbot

# Database
## Tables
### Users
- id : INT
- status : INT
- number : TEXT
- room : TEXT
- earned : INT
## sqlitework description
### DataBase(file : str, namefile : str) - __ init __ -> None
- file is filepath (recommended: __ file __)
- namefile should be without file extension
### createtable(nametable : str, params : list) -> None
Creates table if not exists
- nametable - name of table you want to create
- params - list of tuples (paramname, paramvalue) for database
### Users table methods
#### adduser(params : list) -> None
Adds user with given userid in database (ValueError if already exists)
- params - list of params for database
#### deluser(userid : int) -> None
Delete user with given id (or ValueError if not exists)
- userid - id of user you'd like to delete
#### edituser(editname : str, editval, userid : int) -> None
Edit user with given userid (or ValueError if not exists)
- editname - name of param you want to edit
- editval - value of param you want to edit
- userid - id of user you'd like to edit
#### getuser(userid : int) -> None
RETURNS: one user with given id (or zero if not exists)
- userid - id of user you'd like to get
#### checkuser(userid : INT) -> bool
RETURNS: is user with given userid in database
- userid - id of user you'd like to check
