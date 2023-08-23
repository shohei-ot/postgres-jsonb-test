-- public."tables" definition

-- Drop table

-- DROP TABLE public."tables";

CREATE TABLE public."tables" (
	id serial4 NOT NULL,
	"label" varchar NOT NULL,
	CONSTRAINT tables_pk PRIMARY KEY (id)
);