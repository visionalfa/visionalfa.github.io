-- Pedidos hechos con el botón de arrepentimiento (Resolución 424/2020).
create table if not exists public.arrepentimientos (
  id         bigint generated always as identity primary key,
  codigo     text not null unique,
  nombre     text not null,
  email      text not null,
  operacion  text,
  detalle    text,
  estado     text not null default 'pendiente' check (estado in ('pendiente', 'resuelto')),
  creado     timestamptz not null default now()
);
alter table public.arrepentimientos enable row level security;
-- Sin políticas: solo el servidor puede leer o escribir.
