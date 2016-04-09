CREATE TABLE user
  (uid SERIAL,
   username VARCHAR(25) NOT NULL,
   password VARCHAR(25) NOT NULL,
   firstname VARCHAR(255),
   lastname VARCHAR(255),
   email VARCHAR(255) NOT NULL,
   creationDate TIMESTAMPTZ NOT NULL,

   PRIMARY KEY(uid),
   UNIQUE(username),
   UNIQUE(email)
  );

create table bike
  (
    bid serial,
    uid integer not null,
    model varchar(255) not null,
    status boolean default true,
    price numeric,
    location varchar(255),
    details text,

    primary key(bid),
    foreign key(uid) references user
  )