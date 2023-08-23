-- public.records definition

-- Drop table

-- DROP TABLE public.records;

CREATE TABLE public.records (
	id serial4 NOT NULL,
	"data" jsonb NOT NULL,
	table_id int4 NOT NULL,
	CONSTRAINT records_pk PRIMARY KEY (id)
);
CREATE INDEX records_table_id_idx ON public.records USING btree (table_id);


-- public.records foreign keys

ALTER TABLE public.records ADD CONSTRAINT records_table_fk FOREIGN KEY (table_id) REFERENCES public."tables"(id) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED;