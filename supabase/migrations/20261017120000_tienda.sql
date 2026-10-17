-- Tienda de Visión Alfa: productos, accesos de cada cliente y registro de pagos.

create table if not exists public.productos (
  id        text primary key,
  nombre    text not null,
  tipo      text not null check (tipo in ('ebook', 'membresia', 'vitalicio')),
  precio    numeric(12, 2) not null check (precio > 0),
  archivo   text,                        -- ruta del ebook dentro del bucket privado "ebooks"
  orden     int  not null default 0,
  activo    boolean not null default true
);

insert into public.productos (id, nombre, tipo, precio, archivo, orden) values
  ('ia-para-vender-mas', 'IA para vender más',     'ebook',     25000, 'ia-para-vender-mas.html', 1),
  ('membresia',          'Membresía Visión Alfa',  'membresia', 15000, null, 10),
  ('vitalicio',          'Acceso de por vida',     'vitalicio', 90000, null, 11)
on conflict (id) do nothing;

-- Un acceso por compra o suscripción. mp_referencia evita duplicados cuando Mercado Pago avisa dos veces.
create table if not exists public.accesos (
  id             bigint generated always as identity primary key,
  user_id        uuid not null references auth.users (id) on delete cascade,
  producto_id    text not null references public.productos (id),
  estado         text not null default 'activo' check (estado in ('activo', 'inactivo')),
  mp_referencia  text not null unique,
  creado         timestamptz not null default now(),
  actualizado    timestamptz not null default now()
);
create index if not exists accesos_user_id_idx on public.accesos (user_id);

-- Registro de todo lo que informa Mercado Pago (solo lo lee el sistema).
create table if not exists public.pagos (
  id           text primary key,
  user_id      uuid,
  producto_id  text,
  estado       text,
  monto        numeric(12, 2),
  detalle      jsonb,
  creado       timestamptz not null default now(),
  actualizado  timestamptz not null default now()
);

alter table public.productos enable row level security;
alter table public.accesos   enable row level security;
alter table public.pagos     enable row level security;

drop policy if exists "Productos visibles" on public.productos;
create policy "Productos visibles" on public.productos
  for select to anon, authenticated using (activo);

drop policy if exists "Cada cliente ve sus accesos" on public.accesos;
create policy "Cada cliente ve sus accesos" on public.accesos
  for select to authenticated using ((select auth.uid()) = user_id);

-- Los pagos no tienen políticas: solo el servidor puede leerlos o escribirlos.

-- Bucket privado para los ebooks: sin políticas, así que solo el servidor puede leerlos.
insert into storage.buckets (id, name, public)
values ('ebooks', 'ebooks', false)
on conflict (id) do nothing;
