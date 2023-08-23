-- public."columns" definition

-- Drop table

-- DROP TABLE public."columns";

CREATE TABLE public."columns" (
	id serial4 NOT NULL,
	"label" varchar NOT NULL,
	data_type varchar NOT NULL,
	"nullable" bool NULL DEFAULT false,
	table_id int4 NOT NULL,
	CONSTRAINT columns_pk PRIMARY KEY (id)
);


-- public."columns" foreign keys

ALTER TABLE public."columns" ADD CONSTRAINT columns_table_fk FOREIGN KEY (table_id) REFERENCES public."tables"(id) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED;