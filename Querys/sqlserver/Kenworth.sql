use master;
go

If ((select count(*) from sys.databases db where db.name = 'Kenworth') <> 0)
Drop database Kenworth;

Create database Kenworth;
go

use Kenworth;
go

If ((select count(*) from sys.tables db where db.name = 'Transactions') = 0)
create table Transactions(
id int primary key not null identity(1, 1),
transactionDate date,
transactionTime time,
transactionId int not null,
product varchar(30)
);
go

If ((select count(*) from sys.tables db where db.name = 'Producto') = 0)
create table Producto(
Idproducto int identity(1,1) primary key not null,
Codigo nvarchar(20) not null,
Nombre nvarchar(30) not null)
go
alter table Producto add Precio float;
go

If ((select count(*) from sys.tables db where db.name = 'Material') = 0)
create table Material(
IdDescripcion int primary key not null identity (1,1),
Material nvarchar(20) not null)
go

If ((select count(*) from sys.tables db where db.name = 'Descripcion_Producto') = 0)
create table Descripcion_Producto(
Idproducto int not null,
IdDescripcion int not null
)
go
alter table Descripcion_Producto add foreign key(Idproducto) references Producto(Idproducto);
go
alter table Descripcion_Producto add foreign key(IdDescripcion) references Material(IdDescripcion)
go

If ((select count(*) from sys.tables db where db.name = 'Factura') = 0)
Create table Factura (
idFactura int primary key not null,
fecha_transacciín date,
hora_transacciín time
)
go

If ((select count(*) from sys.tables db where db.name = 'Detalle_Factura') = 0)
create table Detalle_Factura(
idFactura int not null,
Idproducto int not null,
cantidad int not null,
foreign key(idFactura) references Factura(idFactura),
foreign key(Idproducto) references Producto(Idproducto)
)
go

--If ((select count(*) from sys.procedures db where db.name = 'sp_insertTransaction') = 0)
Create procedure sp_insertTransaction
@transactionDate date,
@transactionTime time,
@transactionId int ,
@product varchar(30)
as 
insert into Transactions values (@transactionDate, @transactionTime, @transactionId, @product);
commit transaction
go

Create function fn_createCode(@id int, @name varchar(30))
RETURNS varchar(10)
as
begin
	declare @code varchar(10) = concat(substring(@name, 0, 2), trim(str(@id)))
	return @code
end
go

