-- Quién puede ver el panel de ventas. Privado: sin políticas, solo lo leen las funciones.
create table if not exists public.admins (
  email text primary key
);
alter table public.admins enable row level security;
