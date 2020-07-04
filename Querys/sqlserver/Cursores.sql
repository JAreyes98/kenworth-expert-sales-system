use Kenworth;
go

-- *--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
--	CURSOR QUE REALIZA LA INSERCIíN EN LA TABLA DESCRIPCION_PRODUCTO, GENERANDO EL Material DE FORMA ALEATORIA, ESTO DADO LA ESCASES DE TIEMPO
declare  MyCursor cursor
	for select Idproducto from Producto;
go

open MyCursor;
go

declare @id int
FETCH NEXT FROM MyCursor into @id

WHILE @@FETCH_STATUS = 0  
    BEGIN
		insert into Descripcion_Producto values (@id, (SELECT FLOOR(RAND()*(29-1)+1)))
        FETCH NEXT FROM MyCursor into @id;  
    END;

go
close MyCursor
go
deallocate MyCursor
go

-- *--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
--	CURSOR QUE REALIZA LA ACTUALIZACIíN EN LA TABLA PRODUCTO, ESTABLECIENDO EL PRECIO DE LOS PRODUCTOS PORMEDIO DE LA TABLA goods, ESTO ALEATORIAMENTE.

declare  MyCursor cursor
	for select Idproducto from Producto;
go

open MyCursor;
go

declare @id int
FETCH NEXT FROM MyCursor into @id

WHILE @@FETCH_STATUS = 0  
    BEGIN
		update Producto set Precio = (select price from goods where id = (SELECT FLOOR(RAND()*49)) ) where idProducto = @id
        FETCH NEXT FROM MyCursor into @id;
    END;

go
close MyCursor
go
deallocate MyCursor
go

-- *--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
--	CURSOR QUE INSERTA LOS DETALLES DE LAS FACTURAS

declare  MyCursor cursor
	for select transactionId as IdFactura, product, count(product) [Vendido del producto] from Transactions group by product, transactionId order by transactionId
go

open MyCursor;
go

declare @idFactura int
declare @nombreProd varchar(30)
declare @cantidad int

FETCH NEXT FROM MyCursor into @idFactura, @nombreProd, @cantidad

WHILE @@FETCH_STATUS = 0  
    BEGIN
		declare @idProducto int = (select top 1 p.Idproducto from Producto p where p.Nombre = @nombreProd)
		insert into Detalle_Factura values (@idFactura, @idProducto, @cantidad)
        FETCH NEXT FROM MyCursor into @idFactura, @nombreProd, @cantidad
    END;
	
go
close MyCursor
go
deallocate MyCursor