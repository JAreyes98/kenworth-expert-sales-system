use master
go

select * from sys.databases;
if ((select count(*) from sys.databases db where db.name = 'Kenworth') <> 0)
	begin
		
		use Kenworth;
		begin transaction
		insert into Producto(Nombre, Codigo)
		select distinct t1.product, (select top 1 (select dbo.fn_createCode(t2.id, t2.product)) from Transactions t2 where t2.product = t1.product) as Codigo  from Transactions t1
		commit transaction
		
		begin transaction
		insert into Factura
		select distinct t.transactionId, t.transactionDate, t.transactionTime from Transactions t order by t.transactionDate
		commit transaction

		begin transaction
		insert into Material(Material)
		select distinct flavour from goods;
		commit transaction
		
	end
else 
	begin
	print 'Aun no ha creado la base de datos Kenworth'
	end