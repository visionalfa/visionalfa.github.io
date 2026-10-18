-- Claves de acceso directo al panel (solo se guarda el hash SHA-256, nunca la clave).
create table if not exists public.panel_claves (
  hash   text primary key,
  creada timestamptz not null default now()
);
alter table public.panel_claves enable row level security;
