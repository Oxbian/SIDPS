CREATE DATABASE sidps DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'sidps'@'localhost' IDENTIFIED BY 'SUPERPASSWORD';
GRANT ALL PRIVILEGES ON sidps.* TO 'sidps'@'localhost';
FLUSH PRIVILEGES;
use sidps;
