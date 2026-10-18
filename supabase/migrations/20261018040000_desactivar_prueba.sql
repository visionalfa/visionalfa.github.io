-- La compra de prueba ya no hace falta: el flujo de pago se verificó con una venta real.
update public.productos set activo = false where id = 'prueba-e09ef813';
